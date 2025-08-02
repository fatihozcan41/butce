import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri, dagit_alt_kirilim

st.set_page_config(page_title="Gelir Gider Dağıtım v8", layout="wide")

# Oturum durumları
if "gecmis_oranlar" not in st.session_state:
    st.session_state["gecmis_oranlar"] = pd.DataFrame(columns=["Yıl", "Ay", "HESAP İSMİ", "OSGB", "BELGE"])
if "alt_kirilim_oranlari" not in st.session_state:
    st.session_state["alt_kirilim_oranlari"] = {"Eğitim": 25, "İlk Yardım": 25, "Kalite": 25, "Uzmanlık": 25}

# Sol panel (v6 ile aynı yapı korunur)
with st.sidebar:
    st.header("📂 Veri Yükle")
    firma = st.selectbox("Firma", ["OSGB", "BELGE"])
    tur = st.selectbox("Tür", ["Gider", "Gelir"])
    yil = st.selectbox("Yıl", list(range(2020, 2031)), index=5)
    ay = st.selectbox("Ay", ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], index=5)
    uploaded_file = st.file_uploader("Excel Dosyası Yükle", type=["xlsx"])
    start_button = st.button("Dağıtımı Başlat")

st.title("📊 Gelir-Gider Dağıtım Uygulaması")

def oran_tablosu_guncelle(df, yil, ay):
    mevcut = st.session_state["gecmis_oranlar"]
    yeni_veriler = []

    for hesap in df["HESAP İSMİ"].unique():
        filtre = (mevcut["HESAP İSMİ"] == hesap)
        onceki = mevcut[filtre].sort_values(by=["Yıl", "Ay"], ascending=False).head(1)
        osgb = 50
        belge = 50
        if not onceki.empty:
            osgb = onceki["OSGB"].values[0]
            belge = onceki["BELGE"].values[0]
        yeni_veriler.append({"Yıl": yil, "Ay": ay, "HESAP İSMİ": hesap, "OSGB": osgb, "BELGE": belge})

    yeni_df = pd.DataFrame(yeni_veriler)
    birlesen = pd.concat([mevcut, yeni_df]).drop_duplicates(subset=["Yıl", "Ay", "HESAP İSMİ"], keep="last")
    st.session_state["gecmis_oranlar"] = birlesen

    edited = st.data_editor(
        yeni_df,
        use_container_width=True,
        key="oran_editor",
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

    st.markdown("### 🎯 Hesap Bazlı Oran Girişi")
    oranlar = oran_tablosu_guncelle(df, yil, ay)

    if firma == "BELGE":
        st.markdown("### 🧩 BELGE Alt Kırılım Oranları")
        for key in st.session_state["alt_kirilim_oranlari"]:
            val = st.number_input(f"{key} (%)", min_value=0, max_value=100, step=1,
                                  value=st.session_state["alt_kirilim_oranlari"][key])
            st.session_state["alt_kirilim_oranlari"][key] = val

        toplam = sum(st.session_state["alt_kirilim_oranlari"].values())
        if toplam != 100:
            st.warning("Alt kırılım oranları toplamı %100 olmalıdır.")
        else:
            st.success("Alt kırılım oranları geçerli.")

    if start_button:
        st.success("Dağıtım tamamlandı (simülasyon).")
        dagit_verileri(df, oranlar)
        if firma == "BELGE":
            dagit_alt_kirilim(df, st.session_state["alt_kirilim_oranlari"])
