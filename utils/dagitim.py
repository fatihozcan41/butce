import streamlit as st

def dagit_verileri(df, firma, osgb_oran, belge_oran, egitim=0, ilk_yardim=0, kalite=0, uzmanlik=0):
    st.write(f"Firma: {firma}")
    st.write(f"OSGB Oranı: {osgb_oran}% - BELGE Oranı: {belge_oran}%")
    if firma == "BELGE":
        st.write(f"Alt Kırılımlar → Eğitim: {egitim}%, İlk Yardım: {ilk_yardim}%, Kalite: {kalite}%, Uzmanlık: {uzmanlik}%")
    st.dataframe(df.head())  # Gerçek dağıtım mantığı burada uygulanacak

def kontrol_paneli(durumlar: dict):
    for adim, durum in durumlar.items():
        st.write(f"{'✅' if durum else '❌'} {adim}")
