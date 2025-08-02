import streamlit as st

def dagit_verileri(df, oran_df):
    st.write("📌 Örnek dağıtım (ilk 5 satır)")
    st.dataframe(df.head())
    st.write("📋 Girilen Oranlar")
    st.dataframe(oran_df)
