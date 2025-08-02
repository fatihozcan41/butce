import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri, kontrol_paneli

st.set_page_config(page_title="Gelir Gider Dağıtım", layout="wide")
st.title("📊 Gelir-Gider Dağıtım Uygulaması")

# Kontrol durumu
kontrol_durumu = {
    "Dosya Yüklendi": False,
    "Oranlar Girildi": False,
    "Alt Kırılım Girildi": False,
    "Dağıtım Yapıldı": False
}

st.sidebar.header("Veri Yükle")

firma = st.sidebar.selectbox("Firma", ["OSGB", "BELGE"])
tur = st.sidebar.selectbox("Tür", ["Gider", "Gelir"])
yil = st.sidebar.selectbox("Yıl", list(range(2022, 2027)))
ay = st.sidebar.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"])
uploaded_file = st.sidebar.file_uploader("Excel Dosyası Yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    kontrol_durumu["Dosya Yüklendi"] = True
    st.success("Dosya başarıyla yüklendi. Aşağıda verileri inceleyebilirsiniz.")
    st.dataframe(df)

    osgb_rate = st.sidebar.number_input("OSGB Oranı (%)", min_value=0, max_value=100, value=0)
    belge_rate = 100 - osgb_rate
    st.sidebar.write(f"BELGE Oranı: {belge_rate}%")

    if osgb_rate + belge_rate != 100:
        st.warning("OSGB ve BELGE oranlarının toplamı %100 olmalıdır.")
    else:
        kontrol_durumu["Oranlar Girildi"] = True

    if firma == "BELGE":
        st.sidebar.markdown("**Alt Kırılım Oranları**")
        egitim = st.sidebar.number_input("Eğitim (%)", 0, 100, 0)
        ilk_yardim = st.sidebar.number_input("İlk Yardım (%)", 0, 100, 0)
        kalite = st.sidebar.number_input("Kalite (%)", 0, 100, 0)
        uzmanlik = st.sidebar.number_input("Uzmanlık (%)", 0, 100, 0)

        alt_toplam = egitim + ilk_yardim + kalite + uzmanlik
        if alt_toplam != 100:
            st.warning(f"Alt kırılım oranlarının toplamı %100 olmalıdır. Şu an: %{alt_toplam}")
        else:
            kontrol_durumu["Alt Kırılım Girildi"] = True
    else:
        egitim = ilk_yardim = kalite = uzmanlik = 0
        kontrol_durumu["Alt Kırılım Girildi"] = True

    if st.sidebar.button("Dağıtımı Başlat"):
        if all(kontrol_durumu.values()):
            kontrol_durumu["Dağıtım Yapıldı"] = True
            st.success("Dağıtım tamamlandı (simülasyon).")
            dagit_verileri(df, firma, osgb_rate, belge_rate, egitim, ilk_yardim, kalite, uzmanlik)
        else:
            st.error("Lütfen tüm oranları doğru şekilde giriniz ve gerekli alanları doldurunuz.")

    st.markdown("## ✅ İşlem Kontrol Paneli")
    kontrol_paneli(kontrol_durumu)
