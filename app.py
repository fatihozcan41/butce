import streamlit as st
import pandas as pd
from utils.dagitim import dagit_verileri

st.set_page_config(page_title="Gelir Gider Dağıtım v4", layout="wide")
st.title("📊 Gelir Gider Dağıtım Uygulaması")

st.markdown("""
Bu uygulama ile:

- OSGB ve BELGE firmalarının gelir/giderlerini Excel dosyası üzerinden yükleyebilir,
- Her HESAP İSMİ için OSGB/BELGE oranlarını ayrı ayrı belirleyebilir,
- BELGE için alt kırılım (Eğitim, İlk Yardım, Kalite, Uzmanlık) oranlarını tanımlayabilir,
- Tüm oranlar tablo formatında düzenlenip kontrol edilebilir,
- Aylara göre dağıtılmış tablolar oluşturulabilir.

🔁 Lütfen önce Excel dosyanızı yükleyin, ardından oranları girin ve dağıtımı başlatın.
""")

uploaded_file = st.file_uploader("1. Excel Dosyası Yükle (Gelir/Gider)", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error("Dosya okunamadı. Lütfen geçerli bir Excel dosyası yükleyin.")
        st.stop()

    if "HESAP İSMİ" not in df.columns:
        st.error("Excel dosyasında 'HESAP İSMİ' sütunu bulunamadı.")
        st.stop()

    st.success("Dosya yüklendi, HESAP İSMİ'ler listelendi.")
    hesap_isimleri = df["HESAP İSMİ"].dropna().unique().tolist()

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

    st.markdown("### 2. 🧮 Hesap Bazlı Oran Giriş Tablosu")
    edited_oran_df = st.data_editor(oran_df, use_container_width=True, num_rows="dynamic")

    st.markdown("### 3. ✅ Dağıtım Sonucu")
    if st.button("Dağıtımı Başlat"):
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
