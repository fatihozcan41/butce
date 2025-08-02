import streamlit as st
import pandas as pd

def dagit_verileri(df, oranlar):
    osgb_rows = []
    belge_rows = []
    belge_alt_rows = []

    for _, satir in df.iterrows():
        hesap = satir.get("HESAP İSMİ", "GENEL")
        oran = oranlar[oranlar["HESAP İSMİ"] == hesap]
        tutar_raw = satir.get("ANA DÖVİZ TUTAR", 0)
        try:
            tutar = float(tutar_raw or 0)
        except:
            tutar = 0

        if oran.empty:
            osgb, belge = 50, 50
            egitim = ilk = kalite = uzmanlik = 25
        else:
            osgb = oran["OSGB"].values[0]
            belge = oran["BELGE"].values[0]
            egitim = oran["Eğitim"].values[0]
            ilk = oran["İlk Yardım"].values[0]
            kalite = oran["Kalite"].values[0]
            uzmanlik = oran["Uzmanlık"].values[0]

        osgb_pay = tutar * osgb / 100
        belge_pay = tutar * belge / 100

        osgb_rows.append([hesap, osgb_pay])
        belge_rows.append([hesap, belge_pay])
        belge_alt_rows.append([hesap, "Eğitim", belge_pay * egitim / 100])
        belge_alt_rows.append([hesap, "İlk Yardım", belge_pay * ilk / 100])
        belge_alt_rows.append([hesap, "Kalite", belge_pay * kalite / 100])
        belge_alt_rows.append([hesap, "Uzmanlık", belge_pay * uzmanlik / 100])

    st.markdown("### 🟦 OSGB Dağıtımı")
    df_osgb = pd.DataFrame(osgb_rows, columns=["HESAP İSMİ", "TUTAR (TL)"])
    st.dataframe(df_osgb)

    st.markdown("### 🟨 BELGE Dağıtımı")
    df_belge = pd.DataFrame(belge_rows, columns=["HESAP İSMİ", "TUTAR (TL)"])
    st.dataframe(df_belge)

    st.markdown("### 🧩 BELGE Alt Kırılım Dağılımı")
    df_belge_alt = pd.DataFrame(belge_alt_rows, columns=["HESAP İSMİ", "ALT KIRILIM", "TUTAR (TL)"])
    st.dataframe(df_belge_alt)
