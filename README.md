# Gelir Gider Dağıtım Uygulaması (v2)

Bu proje, OSGB ve BELGE firmaları için yüklenen gelir/gider Excel verilerini oranlara ve aylara göre dağıtarak analiz etmeyi sağlar.

## Kurulum

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Özellikler
- Firma bazlı veri yükleme
- OSGB / BELGE oranları tanımı (zorunlu)
- BELGE için alt kırılım oranları kontrolü
- İşlem kontrol paneli
- Ay bazlı tablo analizi (geliştirilecek)
