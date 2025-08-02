import streamlit as st

def dagit_verileri(df, oranlar):
    st.markdown("### 🧾 Dağıtım Sonuçları")
    for _, satir in df.iterrows():
        hesap = satir.get("HESAP İSMİ", "GENEL")
        oran = oranlar[oranlar["HESAP İSMİ"] == hesap]
        if oran.empty:
            osgb, belge = 50, 50
        else:
            osgb = oran["OSGB"].values[0]
            belge = oran["BELGE"].values[0]
        tutar = satir.get("ANA DÖVİZ TUTAR", 0)
        osgb_pay = tutar * osgb / 100
        belge_pay = tutar * belge / 100
        st.write(f"🔹 {hesap}: OSGB = {osgb_pay:.2f} TL | BELGE = {belge_pay:.2f} TL")

        if not oran.empty:
            st.markdown("  **BELGE Alt Kırılım Dağılımı:**")
            for isim in ["Eğitim", "İlk Yardım", "Kalite", "Uzmanlık"]:
                oran_alt = oran[isim].values[0]
                alt_pay = belge_pay * oran_alt / 100
                st.markdown(f"    • {isim}: {alt_pay:.2f} TL")
