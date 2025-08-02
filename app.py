import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="Gelir Gider Dağıtım v10", layout="wide")

# Oturum verileri
if "gecmis_oranlar" not in st.session_state:
    st.session_state["gecmis_oranlar"] = pd.DataFrame(columns=[
        "Yıl", "Ay", "HESAP İSMİ", "OSGB", "BELGE", "Eğitim", "İlk Yardım", "Kalite", "Uzmanlık"
    ])

# Sol panel
with st.sidebar:
    st.header("📂 Veri Yükle")
    firma = st.selectbox("Firma", ["OSGB", "BELGE"])
    tur = st.selectbox("Tür", ["Gider", "Gelir"])
    yil = st.selectbox("Yıl", list(range(2020, 2031)), index=5)
    ay = st.selectbox("Ay", [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ], index=5)
    uploaded_file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])
    start_button = st.button("Dağıtımı Başlat")

st.title("📊 Gelir-Gider Dağıtım v10 (3 Ayrı Sonuç Tablosu)")

def oran_tablosu_guncelle(df, yil, ay):
    mevcut = st.session_state["gecmis_oranlar"]
    yeni_veriler = []

    for hesap in df["HESAP İSMİ"].unique():
        filtre = (mevcut["HESAP İSMİ"] == hesap)
        onceki = mevcut[filtre].sort_values(by=["Yıl", "Ay"], ascending=False).head(1)
        varsayilanlar = {
            "OSGB": 50, "BELGE": 50,
            "Eğitim": 25, "İlk Yardım": 25, "Kalite": 25, "Uzmanlık": 25
        }
        if not onceki.empty:
            for key in varsayilanlar:
                varsayilanlar[key] = onceki[key].values[0]
        veri = {
            "Yıl": yil, "Ay": ay, "HESAP İSMİ": hesap,
            **varsayilanlar
        }
        yeni_veriler.append(veri)

    yeni_df = pd.DataFrame(yeni_veriler)
    birlesen = pd.concat([mevcut, yeni_df]).drop_duplicates(subset=["Yıl", "Ay", "HESAP İSMİ"], keep="last")
    st.session_state["gecmis_oranlar"] = birlesen

    edited = st.data_editor(
        yeni_df,
        use_container_width=True,
        key="tek_tablo_oran_editor",
        num_rows="dynamic"
    )

    return edited

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception:
        st.error("Excel okunamadı.")
        st.stop()

    if "HESAP İSMİ" not in df.columns:
        st.error("'HESAP İSMİ' sütunu eksik.")
        st.stop()

    st.success("Dosya yüklendi.")
    st.dataframe(df)

    st.markdown("### 🎯 Tüm Oranların Girişi (Tek Tabloda)")
    oranlar = oran_tablosu_guncelle(df, yil, ay)

    # Alt kırılım kontrolü
    for idx, row in oranlar.iterrows():
        toplam = row["Eğitim"] + row["İlk Yardım"] + row["Kalite"] + row["Uzmanlık"]
        if toplam != 100:
            st.warning(f"{row['HESAP İSMİ']} için alt kırılım toplamı %100 değil → Toplam = {toplam}")

    if start_button:
        st.success("Dağıtım tamamlandı (simülasyon).")
        dagit_verileri(df, oranlar)
