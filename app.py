
import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="Gelir Gider Dağıtım", layout="wide")
st.title("📊 Gelir-Gider Dağıtım Uygulaması")

st.sidebar.header("Veri Yükle")

firma = st.sidebar.selectbox("Firma", ["OSGB", "BELGE"])
tur = st.sidebar.selectbox("Tür", ["Gider", "Gelir"])
yil = st.sidebar.selectbox("Yıl", list(range(2022, 2027)))
ay = st.sidebar.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"])
uploaded_file = st.sidebar.file_uploader("Excel Dosyası Yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Dosya başarıyla yüklendi. Aşağıda verileri inceleyebilirsiniz.")
    st.dataframe(df)

    if st.sidebar.button("Dağıtımı Başlat"):
        oran_girildi = st.sidebar.slider("OSGB Oranı (%)", 0, 100, 60)
        belge_oran = 100 - oran_girildi

        if firma == "BELGE":
            st.sidebar.markdown("**Alt Kırılım Oranları**")
            egitim = st.sidebar.number_input("Eğitim (%)", 0, 100, 25)
            ilk_yardim = st.sidebar.number_input("İlk Yardım (%)", 0, 100, 25)
            kalite = st.sidebar.number_input("Kalite (%)", 0, 100, 25)
            uzmanlik = st.sidebar.number_input("Uzmanlık (%)", 0, 100, 25)
            if egitim + ilk_yardim + kalite + uzmanlik != 100:
                st.error("Alt kırılım oranlarının toplamı %100 olmalıdır.")
            else:
                st.success("Dağıtım tamamlandı (simülasyon).")
                dagit_verileri(df, firma, oran_girildi, belge_oran, egitim, ilk_yardim, kalite, uzmanlik)
        else:
            st.success("Dağıtım tamamlandı (simülasyon).")
            dagit_verileri(df, firma, oran_girildi, belge_oran)
