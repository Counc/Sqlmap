# SQLMAP 🚀

**SQLMAP**, Python ile geliştirilmiş hafif, komut satırı tabanlı bir **SQL Injection (SQLi)** açık test aracıdır. Yetkili sızma testi laboratuvarları ve eğitim amaçlı kullanım için özel olarak tasarlanmıştır.

## ✨ Özellikler
* **Parametre Analizi:** Hedef URL'deki parametreleri ve değerleri otomatik olarak ayrıştırır.
* **Payload Enjeksiyonu:** En sık kullanılan temel SQL Injection test payload'larını hedefe uygular.
* **Hata Tabanlı Tespit:** Sunucu yanıtlarındaki veritabanı hata mesajlarını (`MySQL`, `SQLite`, `PostgreSQL` vb.) tarar.
* **Şık Görünüm:** Terminal üzerinde dikkat çekici büyük ASCII banner arayüzüne sahiptir.

---

## 📋 Gereksinimler
* Python 3.x
* `requests` kütüphanesi

---

## ⚙️ Kurulum

Projeyi kurmak ve bağımlılıkları yüklemek için terminale şu komutları sırasıyla yazabilirsiniz:

```bash
git clone [https://github.com/Bat0sneyebaktin/Sqlmap.git](https://github.com/Bat0sneyebaktin/Sqlmap.git)
cd Sqlmap
pip install -r requirements.txt

