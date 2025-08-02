import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="Gelir Gider Dağıtım v5", layout="wide")

with st.sidebar:
    st.header("📂 Veri Yükle")

    firma = st.selectbox("Firma", ["OSGB", "BELGE"])
    tur = st.selectbox("Tür", ["Gider", "Gelir"])
    yil = st.selectbox("Yıl", list(range(2020, 2031)), index=5)
    ay = st.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=5)

    uploaded_file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"], help="Limit 200MB")
    osgb_orani = st.slider("OSGB Oranı (%)", 0, 100, 50)
    start_button = st.button("Dağıtımı Başlat")

st.title("📊 Gelir-Gider Dağıtım Uygulaması")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error("Dosya okunamadı. Lütfen geçerli bir Excel dosyası yükleyin.")
        st.stop()

    if "HESAP İSMİ" not in df.columns:
        st.error("Excel dosyasında 'HESAP İSMİ' sütunu bulunamadı.")
        st.stop()

    st.success("Dosya başarıyla yüklendi. Aşağıda verileri inceleyebilirsiniz.")
    st.dataframe(df)

    if start_button:
        belge_orani = 100 - osgb_orani
        st.success("Dağıtım tamamlandı (simülasyon).")
        st.markdown(f"**Firma:** {firma}")
        st.markdown(f"**OSGB Oranı:** {osgb_orani}% – **BELGE Oranı:** {belge_orani}%")
        dagit_verileri(df, osgb_orani, belge_orani)
