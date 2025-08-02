import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="Gelir Gider Dağıtım v6", layout="wide")

if "gecmis_oranlar" not in st.session_state:
    st.session_state["gecmis_oranlar"] = {}

with st.sidebar:
    st.header("📂 Veri Yükle")
    firma = st.selectbox("Firma", ["OSGB", "BELGE"])
    tur = st.selectbox("Tür", ["Gider", "Gelir"])
    yil = st.selectbox("Yıl", list(range(2020, 2031)), index=5)
    ay = st.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=5)
    uploaded_file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])
    farkli_oran = st.checkbox("Bu ay için farklı oran gir", value=False)

    key = f"{yil}-{ay}"
    osgb_orani = 50
    if not farkli_oran and key in st.session_state["gecmis_oranlar"]:
        osgb_orani = st.session_state["gecmis_oranlar"][key]
        st.info(f"{key} ayı için önceki oranlar yüklendi: OSGB %{osgb_orani}, BELGE %{100 - osgb_orani}")

    osgb_orani = st.slider("OSGB Oranı (%)", 0, 100, osgb_orani)

    start_button = st.button("Dağıtımı Başlat")

st.title("📊 Gelir-Gider Dağıtım Uygulaması")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error("Excel okunamadı.")
        st.stop()

    if "HESAP İSMİ" not in df.columns:
        st.error("'HESAP İSMİ' sütunu eksik.")
        st.stop()

    st.success("Dosya yüklendi.")
    st.dataframe(df)

    if start_button:
        st.session_state["gecmis_oranlar"][key] = osgb_orani
        belge_orani = 100 - osgb_orani
        st.success("Dağıtım tamamlandı (simülasyon).")
        st.markdown(f"**Firma:** {firma}")
        st.markdown(f"**OSGB Oranı:** {osgb_orani}% – **BELGE Oranı:** {belge_orani}%")
        dagit_verileri(df, osgb_orani, belge_orani)
