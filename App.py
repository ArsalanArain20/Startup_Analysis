import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# using streamlit we can also set page width and page Name
st.set_page_config(layout="wide",page_title="Startup Funding")
Data = pd.read_csv("Startup Clean.csv")

# Convert the 'date' column to datetime
Data["date"] = pd.to_datetime(Data["date"])
Data["year"] = Data["date"].dt.year
Data['month'] = Data['date'].dt.month_name()

def Load_Overall_Analysis():
    total = round(Data["amount"].sum())
    max = round(Data["amount"].max())
    # max_index = Data.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).index[0]
    avg = round(Data.groupby("startup")["amount"].sum().mean())
    startups = Data["startup"].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric("Total Amount", str(total) + "CR")
    with col2:
        st.metric("Average Amount", str(avg) + "CR")
    with col3:
        st.metric("Higgest Amount", str(max) + "CR")
    with col4:
        st.metric("Funded Startups", str(startups))

    col1,col2 = st.columns(2)
    with col1:
        st.header("MOM Graph")
        select_option = st.selectbox("Select One", ["Total", "Count"])
        if select_option == "Total":
            tem = Data.groupby(["year", "month"])["amount"].sum().reset_index()
        else:
            tem = Data.groupby(["year", "month"])["startup"].count().reset_index()

        tem["combined-Date"] = tem["month"].astype("str") + "-" + tem["year"].astype("str")
        fig11, axe = plt.subplots()
        axe.plot(tem["combined-Date"], tem["amount"] if select_option == "Total" else tem["startup"])
        axe.set_xlabel("Year")
        axe.set_ylabel("Investment Amount" if select_option == "Total" else "Count")
        axe.set_title("Yearly Month by Month")
        plt.xticks(rotation=90)
        st.pyplot(fig11)
    with col2:
        st.header("City vise Analysis")
        City = Data.groupby("city")["amount"].sum().sort_values(ascending=False).head(10)
        fig222, axxx = plt.subplots()
        axxx.pie(City, labels=City.index, autopct="%0.01f%%")
        axxx.set_title("Top 10 most Investment")
        st.pyplot(fig222)

    col3, col4 = st.columns(2)

    with col3:
        st.header("Sector Analysis")
        option = st.selectbox("Select One", ["Count", "Sum"])
        if option == 'Count':
            Most_Sector = Data.groupby("round")["amount"].count().sort_values(ascending=False).head(10)
            fig22, axx = plt.subplots()
            axx.pie(Most_Sector, labels=Most_Sector.index, autopct="%0.01f%%")
            st.pyplot(fig22)
        else:
            Most_Sectors = Data.groupby("round")["amount"].sum().sort_values(ascending=False).head(10)
            fig22, axx = plt.subplots()
            axx.pie(Most_Sectors, labels=Most_Sectors.index, autopct="%0.01f%%")
            st.pyplot(fig22)

        with col4:
            st.header('Startup Analysis')
            btn = st.selectbox("Select One", ["Overall", "Year Vise"])
            if btn == "Overall":
                New_DF = Data.groupby("startup")["amount"].sum().sort_values(ascending=False).head(10)
                New_DF = New_DF.reset_index()  # Reset the index to make it a DataFrame
            else:
                # Your existing code
                year_vise = Data.groupby(['year', 'startup'])["amount"].sum().reset_index()
                max_amount_indices = year_vise.groupby('year')['amount'].idxmax()
                max_amount_startups = year_vise.loc[max_amount_indices]
                New_DF = max_amount_startups.copy()  # Copy the DataFrame

            # Create a pie chart
            fig223, axxe = plt.subplots()
            axxe.pie(New_DF["amount"], labels=New_DF["startup"], autopct="%0.01f%%")
            axxe.set_title("Startup Overall" if btn == "Overall" else "Startup Yearvise")
            st.pyplot(fig223)

    st.header("Investor vise Analysis")
    Investor = Data.groupby("investors")["amount"].sum().sort_values(ascending=False).head(10)
    fig2222, axxxx = plt.subplots()
    axxxx.barh(Investor.index, Investor.values)  # Use barh for horizontal bars
    axxe.set_title("Top 10 Investors")
    plt.xlabel("Investment Amount")  # Label for the x-axis
    plt.ylabel("Investor")  # Label for the y-axis
    st.pyplot(fig2222)

def load_startup_detail(startup):
    st.title("Startup Analysis")
    #startup = st.text_input("Enter Startup Name :")
    DFe = Data[Data["startup"] == startup][["startup", "vertical", "subvertical", "city", "amount"]]
    st.dataframe(DFe)
    st.header("Funding round")
    Fund_round = Data.groupby(["year", "month", "investors", "startup"])["amount"].sum().reset_index().sort_values(by=["year", "month"])
    st.dataframe(Fund_round)

    st.title("Most Similar Companies")
    tmep = Data[Data["startup"].str.contains(startup)]
    li = tmep["vertical"].unique().tolist()
    vertical_dict = {vertical: 0 for vertical in li}
    T = tmep.groupby("vertical")["vertical"].count().to_dict()
    max_pair = max(T.items(), key=lambda x: x[1])
    Other = Data[Data["startup"] != startup]
    tme = Other[Other["vertical"] == max_pair[0]]
    Ye = tme.groupby("startup")["startup"].count().sort_values(ascending=False).head(5).index.tolist()
    Dfe = Data[Data['startup'].isin(Ye)]
    st.dataframe(Dfe)



def Load_Investor_Details(Name):
    st.title(Name)
    Most_Recent = Data[Data["investors"].str.contains(Name)].head(5)[["date","startup","vertical","city","investors","round","amount"]]
    st.subheader("Most Recent Investment")
    st.dataframe(Most_Recent)
    col1,col2 = st.columns(2)
    with col1:
        Most_Investment = Data[Data["investors"].str.contains(Name)].groupby("startup")["amount"].sum().sort_values(ascending=False).head(5)
        st.subheader("Higgest Investment")
        fig, ax = plt.subplots()
        ax.bar(Most_Investment.index, Most_Investment.values)
        st.pyplot(fig)
    with col2:
        Most_Invest_in_Secotrs = Data[Data["investors"].str.contains(Name)].groupby("vertical")["amount"].sum().sort_values(ascending=False).head(5)
        st.subheader("Most investment in Sector")
        fig1, ax = plt.subplots()
        ax.pie(Most_Invest_in_Secotrs,labels=Most_Invest_in_Secotrs.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    col3,col4 = st.columns(2)
    with col3:
        st.subheader("Investment in Cities")
        City = Data[Data["investors"].str.contains(Name)].groupby("city")["amount"].sum().sort_values(ascending=False)
        fig2, ax = plt.subplots()
        ax.pie(City, labels=City.index, autopct="%0.01f%%")
        st.pyplot(fig2)
    with col4:
        st.subheader("Investment in Sector area vise")
        Area_vise = Data[Data["investors"].str.contains(Name)].groupby("round")["amount"].sum().sort_values(ascending=False)
        fig3, ax = plt.subplots()
        ax.pie(Area_vise, labels=Area_vise.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    col5,col6 = st.columns(2)
    with col5:
        st.subheader("Year Wise Investment")
        Yearly_Investment = Data[Data["investors"].str.contains(Name)].groupby("year")["amount"].sum()
        fig, ax = plt.subplots()
        ax.plot(Yearly_Investment.index, Yearly_Investment.values)
        ax.set_xlabel("Year")
        ax.set_ylabel("Investment Amount")
        ax.set_title("Yearly Investment by Tiger Global Management")
        st.pyplot(fig)
    with col6:
        st.header("Similar Investors")
        temp = Data[Data['investors'].str.contains(Name)]
        Similar = temp["vertical"].tolist()
        Sube = [value for value in temp["subvertical"].tolist() if not pd.isna(value)]
        temp2 = Data[~Data['investors'].str.contains(Name)]

        def County(val):
            count = 0
            if val in Similar:
                count = count + 1
            return count

        temp2["Check Similiarty"] = temp2["vertical"].apply(County)

        def Sub(val):
            count = 0
            if val in Sube:
                count = count + 1
            return count

        temp2["Sub Similar"] = temp2['subvertical'].apply(Sub)

        top_10 = temp2.groupby("investors")["Check Similiarty"].sum().sort_values(ascending=False).head(10).index.tolist()
        top_100 = temp2.groupby("investors")["Sub Similar"].sum().sort_values(ascending=False).head(10).index.tolist()
        data_filter = Data[(Data["investors"].isin(top_10)) | (Data["investors"].isin(top_100))]
        Dataframe = data_filter.groupby(["investors", "vertical", "subvertical"])["amount"].sum().sort_values(ascending=False).head(5).reset_index()
        st.dataframe(Dataframe)





st.sidebar.header("Analysis Categoty")
select = st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])

if select == "Overall Analysis":
    st.title("Overall Analysis")
    Load_Overall_Analysis()
elif select == "Startup":
    startup = st.sidebar.selectbox("Select Startup",sorted(Data["startup"].unique().tolist()))
    btn = st.sidebar.button("Find Startup Detail")
    if btn:
        load_startup_detail(startup)
else:
    selected_investor = st.sidebar.selectbox("Select Investor",sorted(set(Data["investors"].str.split(",").sum())))
    btn = st.sidebar.button("Find Investor Detail")
    if btn:
        Load_Investor_Details(selected_investor)



