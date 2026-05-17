\# Flask Bug Tracker İskelet Planı



İnternet Programcılığı dersi projeniz olan Hata Takip (Bug Tracker) sistemi için Flask 3.x tabanlı, uygulama fabrikası (application factory) tasarım desenini ve Blueprint'leri kullanan temiz bir proje iskeleti oluşturacağız.



\## Hedeflenen Klasör Yapısı



Aşağıdaki klasör yapısı ve dosyalar oluşturulacaktır:



```text

BLG106\_BugTracker/

├── app/

│   ├── \_\_init\_\_.py          # Uygulama fabrikası (create\_app) ve eklenti tanımlamaları

│   ├── main/

│   │   └── \_\_init\_\_.py      # Ana uygulama blueprint'i

│   ├── auth/

│   │   └── \_\_init\_\_.py      # Kimlik doğrulama blueprint'i

│   ├── models.py            # Veritabanı modelleri (şu an için boş bırakılacak)

│   ├── templates/           # HTML şablonları (klasör olarak oluşturulacak)

│   └── static/              # CSS, JS, Görseller (klasör olarak oluşturulacak)

├── migrations/              # Flask-Migrate tarafından yönetilecek (başlangıçta boş klasör)

├── tests/

│   └── \_\_init\_\_.py          # Test klasörü

├── config.py                # Uygulama yapılandırma ayarları

├── requirements.txt         # Proje bağımlılıkları (Flask 3.x ve eklentileri)

├── .env.example             # Örnek çevre değişkenleri dosyası

├── .gitignore               # Versiyon kontrolünden dışlanacak dosyalar listesi

└── run.py                   # Uygulamayı başlatacak ana dosya

```



\## Önerilen Değişiklikler ve İçerikler



\### Bağımlılıklar (`requirements.txt`)

Yalnızca talep edilen paketler eklenecektir:

\- `flask` (Flask 3.x sürümü belirtilecek, örn: `Flask>=3.0.0`)

\- `flask-sqlalchemy`

\- `flask-migrate`

\- `flask-login`

\- `flask-wtf`

\- `python-dotenv`



\### Yapılandırma ve Başlangıç Dosyaları

\- \*\*`.gitignore`\*\*: İçerisinde `.env`, `\_\_pycache\_\_/`, `venv/`, `\*.pyc` vb. Python ve çevre değişkeni dosyalarının engellendiği bir liste olacak.

\- \*\*`.env.example`\*\*: `FLASK\_APP=run.py`, `FLASK\_DEBUG=1`, `SECRET\_KEY=...` gibi temel ayarları içeren örnek bir dosya olacak.

\- \*\*`config.py`\*\*: `.env` dosyasından bu ayarları çeken temel bir `Config` sınıfı bulunacak.

\- \*\*`run.py`\*\*: `app` klasöründen `create\_app` fonksiyonunu çağırarak uygulamayı başlatacak.



\### Uygulama İskeleti (`app/`)

\- \*\*`app/\_\_init\_\_.py`\*\*: Eklentilerin (SQLAlchemy, Migrate vb.) başlatılacağı ve `create\_app()` factory fonksiyonunun tanımlanacağı yer. Blueprint'ler de bu fonksiyon içinde uygulamaya (app) kaydedilecek.

\- \*\*`app/main/\_\_init\_\_.py`\*\*: `main` adında bir Blueprint oluşturulacak. İçerik (route) yazılmayacak.

\- \*\*`app/auth/\_\_init\_\_.py`\*\*: `auth` adında bir Blueprint oluşturulacak. İçerik yazılmayacak.

\- \*\*`app/models.py`\*\*: Boş bırakılacak veya sadece `db` nesnesi import edilecek.



\## User Review Required



Lütfen yukarıdaki planı inceleyin. İskelet yapısı, klasörler ve belirtilen kurallar uygunsa onay verin. Onayınızın ardından dosya ve klasörleri oluşturmaya başlayacağım.



