import streamlit as st
import pandas as pd

aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

def aylar_arasi_dagilim(tutar, baslangic, bitis):
    ay_sayisi = bitis - baslangic + 1
    dagilim = [0] * 12
    if ay_sayisi <= 0:
        return dagilim
    pay = tutar / ay_sayisi
    for i in range(baslangic - 1, bitis):
        dagilim[i] = pay
    return dagilim

def dagit_verileri(df, oranlar):
    osgb_rows = {}
    belge_rows = {}
    belge_alt_rows = {}

    for _, satir in df.iterrows():
        hesap = satir.get("HESAP İSMİ", "GENEL")
        oran = oranlar[oranlar["HESAP İSMİ"] == hesap]
        tutar_raw = satir.get("ANA DÖVİZ TUTAR", 0)
        try:
            tutar = float(tutar_raw or 0)
        except:
            tutar = 0

        baslangic = satir.get("Başlangıç", 1)
        bitis = satir.get("Bitiş", 1)
        if pd.isna(baslangic) or pd.isna(bitis):
            continue
        try:
            baslangic = int(baslangic)
            bitis = int(bitis)
        except:
            continue

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
        osgb_aylik = aylar_arasi_dagilim(osgb_pay, baslangic, bitis)
        belge_aylik = aylar_arasi_dagilim(belge_pay, baslangic, bitis)
        egitim_aylik = aylar_arasi_dagilim(belge_pay * egitim / 100, baslangic, bitis)
        ilk_aylik = aylar_arasi_dagilim(belge_pay * ilk / 100, baslangic, bitis)
        kalite_aylik = aylar_arasi_dagilim(belge_pay * kalite / 100, baslangic, bitis)
        uzmanlik_aylik = aylar_arasi_dagilim(belge_pay * uzmanlik / 100, baslangic, bitis)

        osgb_rows.setdefault(hesap, [0]*12)
        belge_rows.setdefault(hesap, [0]*12)
        for i in range(12):
            osgb_rows[hesap][i] += osgb_aylik[i]
            belge_rows[hesap][i] += belge_aylik[i]

        for isim, dagilim in zip(
            ["Eğitim", "İlk Yardım", "Kalite", "Uzmanlık"],
            [egitim_aylik, ilk_aylik, kalite_aylik, uzmanlik_aylik]
        ):
            belge_alt_rows.setdefault((hesap, isim), [0]*12)
            for i in range(12):
                belge_alt_rows[(hesap, isim)][i] += dagilim[i]

    st.markdown("### 🟦 OSGB Dağıtımı")
    df1 = pd.DataFrame.from_dict(osgb_rows, orient="index", columns=aylar)
    df1.index.name = "HESAP İSMİ"
    st.dataframe(df1)

    st.markdown("### 🟨 BELGE Dağıtımı")
    df2 = pd.DataFrame.from_dict(belge_rows, orient="index", columns=aylar)
    df2.index.name = "HESAP İSMİ"
    st.dataframe(df2)

    st.markdown("### 🧩 BELGE Alt Kırılım Dağılımı")
    df3 = pd.DataFrame.from_dict(belge_alt_rows, orient="index", columns=aylar)
    if not isinstance(df3.index, pd.MultiIndex):
        df3.index = pd.MultiIndex.from_tuples(df3.index, names=["HESAP İSMİ", "ALT KIRILIM"])
    st.dataframe(df3)
