import streamlit as st

def dagit_verileri(df, osgb_orani, belge_orani):
    st.write("📌 Örnek veri (ilk 5 satır):")
    st.dataframe(df.head())

    st.write("🔢 Oranlara göre örnek dağıtım:")
    for i, row in df.iterrows():
        tutar = row.get("ANA DÖVİZ TUTAR", 0)
        osgb_pay = tutar * osgb_orani / 100
        belge_pay = tutar * belge_orani / 100
        st.write(f"{row.get('HESAP İSMİ')} → OSGB: {osgb_pay:.2f} TL | BELGE: {belge_pay:.2f} TL")
