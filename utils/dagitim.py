import streamlit as st

def dagit_verileri(df, oranlar):
    st.write("🔎 Dağıtım Oranları:")
    st.dataframe(oranlar)

    st.write("📊 Örnek Dağıtım:")
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
        st.write(f"{hesap}: OSGB = {osgb_pay:.2f} TL | BELGE = {belge_pay:.2f} TL")

def dagit_alt_kirilim(df, alt_oranlar):
    st.markdown("### 📚 Alt Kırılım Dağılımı (BELGE)")
    for _, row in df.iterrows():
        hesap = row.get("HESAP İSMİ", "GENEL")
        belge_tutar = row.get("ANA DÖVİZ TUTAR", 0)
        st.write(f"🔸 {hesap} Toplam: {belge_tutar:.2f} TL")
        for isim, oran in alt_oranlar.items():
            pay = belge_tutar * oran / 100
            st.markdown(f"  • {isim}: {pay:.2f} TL")
