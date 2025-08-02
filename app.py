import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="Gelir Gider Dağıtım v3", layout="wide")
st.title("📊 Gelir-Gider Dağıtım (Hesap Bazlı Oran Girişli)")

uploaded_file = st.file_uploader("Excel Dosyası Yükle (Gelir/Gider)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Dosya yüklendi, HESAP İSMİ'ler listelendi.")
    hesap_isimleri = df["HESAP İSMİ"].unique().tolist()

    # Varsayılan oran tablosu
    oran_df = pd.DataFrame({
        "HESAP İSMİ": hesap_isimleri,
        "OSGB (%)": [50] * len(hesap_isimleri),
        "BELGE (%)": [50] * len(hesap_isimleri),
        "Eğitim": [25] * len(hesap_isimleri),
        "İlk Yardım": [25] * len(hesap_isimleri),
        "Kalite": [25] * len(hesap_isimleri),
        "Uzmanlık": [25] * len(hesap_isimleri),
    })

    st.markdown("### 🧮 Hesap Bazlı Oran Giriş Tablosu")
    edited_oran_df = st.data_editor(oran_df, use_container_width=True, num_rows="dynamic")

    st.markdown("### ✅ Dağıtım Sonucu")
    if st.button("Dağıtımı Başlat"):
        # Basit doğrulama
        for i, row in edited_oran_df.iterrows():
            if row["OSGB (%)"] + row["BELGE (%)"] != 100:
                st.error(f"{row['HESAP İSMİ']} için OSGB + BELGE oranı %100 değil!")
                st.stop()
            if row["BELGE (%)"] > 0:
                alt_toplam = row["Eğitim"] + row["İlk Yardım"] + row["Kalite"] + row["Uzmanlık"]
                if alt_toplam != 100:
                    st.error(f"{row['HESAP İSMİ']} için alt kırılımlar toplamı %100 değil!")
                    st.stop()
        st.success("Tüm oranlar geçerli. Dağıtım başlatılıyor...")
        dagit_verileri(df, edited_oran_df)
