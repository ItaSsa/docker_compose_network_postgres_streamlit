import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from init_db import init_db 

# Run DB setup once
init_db()

DB_NAME = "churn_db"
DB_USER = "postgres"
DB_PASS = "Postgres2019!"
DB_HOST = "db"
DB_PORT = "5432"
TABLE_NAME = "customer_churn"

@st.cache_data
def load_data():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    df = pd.read_sql(f'SELECT * FROM {TABLE_NAME}', conn)
    conn.close()
    return df

df = load_data()

# Streamlit dashboard
st.title("📊 Customer Churn Dashboard")

st.subheader("Customer Data")
st.dataframe(df)

st.subheader("Churn Distribution")
churn_counts = df["Churn"].value_counts()
st.bar_chart(churn_counts)

# Clean your data first
df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
df["Tenure"] = pd.to_numeric(df["Tenure"], errors="coerce")

# Monthly Charges Boxplot
st.subheader("Monthly Charges by Churn")
fig, ax = plt.subplots()
df.boxplot(column="MonthlyCharges", by="Churn", ax=ax)
plt.title("Monthly Charges by Churn")
plt.suptitle("")
st.pyplot(fig)

# Average Tenure by Gender
st.subheader("Average Tenure by Gender")
avg_tenure = df.groupby("Gender")["Tenure"].mean()
st.bar_chart(avg_tenure)