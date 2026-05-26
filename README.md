# VibeLog Hata Takip Sistemi (Bug Tracker)

Demo Videosu: [https://drive.google.com/file/d/1XgD6BYhw1TikT-ZdUc3MkIUWyFGYQDzU/view?usp=sharing]
BLG106 İnternet Programcılığı dersi kapsamında, AI destekli "Vibe Coding" yaklaşımıyla geliştirilmiş Flask tabanlı hata takip uygulaması olan
VibeLog, kullanıcıların kendi yazılım projelerini oluşturarak bu projelere ait yazılım hatalarını (bug) kayıt altına almasını, yönetmesini ve çözüldü olarak işaretlemesini sağlayan modern ve kullanıcı dostu bir hata takip sistemidir. Her kullanıcı yalnızca kendi projelerini ve hatalarını yönetebilir. Proje, şık arayüzü ve verimli mimarisiyle geliştirme süreçlerini hızlandırmak amacıyla tasarlanmıştır.

## 🚀 Kullanılan Teknolojiler
- **Backend:** Python 3.12, Flask, SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF
- **Veritabanı:** SQLite
- **Frontend:** Jinja2 Şablon Motoru, Bootstrap 5, Custom CSS (Glassmorphism, Gradient UI)
- **Konteynerleştirme:** Docker, Docker Compose, Gunicorn

## 🛠️ Kurulum Adımları (Lokal Geliştirme)

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın:

**1. Depoyu İndirin ve Dizine Girin:**
```bash
git clone <repo-url>
cd BLG106_BugTracker
```

**2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin:**
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate
# macOS/Linux için:
source venv/bin/activate
```

**3. Gereksinimleri Yükleyin:**
```bash
pip install -r requirements.txt
```

**4. Çevre Değişkenlerini (Env) Ayarlayın:**
Proje ana dizininde bulunan `.env.example` dosyasının adını `.env` olarak değiştirin veya yeni bir `.env` dosyası oluşturarak içeriğini doldurun:
```env
SECRET_KEY=sizin-gizli-anahtariniz
DATABASE_URL=sqlite:///app.db
```

**5. Veritabanını Başlatın:**
```bash
flask db upgrade
```

## ⚙️ Geliştirme ve Çalıştırma Komutları

Uygulamayı geliştirme sunucusuyla başlatmak için:
```bash
flask run
```

Veritabanı modellerinde değişiklik yaptıktan sonra migrasyonları uygulamak için:
```bash
flask db migrate -m "Migrasyon aciklamasi"
flask db upgrade
```

## 🐳 Docker ile Çalıştırma

Projeyi lokal bilgisayarınıza Python vb. kurmadan, doğrudan Docker üzerinden ayağa kaldırmak isterseniz proje ana dizininde şu komutu çalıştırmanız yeterlidir:
```bash
docker-compose up -d --build
```
Uygulamanız yapılandırıldıktan sonra `http://localhost:5000` adresinden sisteme erişebilirsiniz. Konteyner veritabanını volume aracılığıyla lokaldeki `app.db` dosyasına bağladığı için verileriniz kaybolmaz.
