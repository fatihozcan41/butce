import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="📊 Gelir-Gider Dağıtım", layout="wide")

st.markdown("# 📊 Gelir-Gider Dağıtım Uygulaması")

# Sol Panel Arayüzü
with st.sidebar:
    st.markdown("## 📂 Dosya Yükleme")
    uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])
    firma = st.selectbox("Firma", ["OSGB", "BELGE"])
    islem_turu = st.selectbox("İşlem Türü", ["Gider", "Gelir"])
    yil = st.number_input("Yıl", value=2025)
    ay = st.selectbox("Ay", list(range(1, 13)))

    st.markdown("---")
    st.markdown("## 🎯 Hesap Bazlı Oran Girişi")

# Oran Girişi - Sol panelde görünmeyen ama içerik uyumlu
st.markdown("### 🎯 Hesap Bazlı Oran Girişi (Tablo)")
oran_df = st.data_editor(
    pd.DataFrame({
        "HESAP İSMİ": ["ELEKTRİK", "OFİS GİDERİ"],
        "OSGB": [60, 70],
        "BELGE": [40, 30],
        "Eğitim": [25, 20],
        "İlk Yardım": [25, 30],
        "Kalite": [25, 25],
        "Uzmanlık": [25, 25]
    }),
    num_rows="dynamic",
    key="oran_editor"
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Dosya başarıyla yüklendi.")
    st.dataframe(df)

    if st.button("🚀 Dağıtımı Başlat"):
        dagit_verileri(df, oran_df)
