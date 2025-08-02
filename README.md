# Gelir Gider Dağıtım Uygulaması (v3)

Bu sürümde her bir HESAP İSMİ için ayrı ayrı OSGB/BELGE ve alt kırılım oranları girilebilir. Tüm oranlar tablo formatında düzenlenir.

## Kurulum

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Özellikler
- HESAP İSMİ bazlı oran girişi
- Toplam kontrolü (OSGB + BELGE = 100, alt kırılım = 100)
- Oran girişi tablo üzerinden
