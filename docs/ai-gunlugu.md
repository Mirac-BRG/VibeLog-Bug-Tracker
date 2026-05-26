# VibeLog - AI Günlüğü (BLG106 İnternet Programcılığı)

## Oturum 1: Proje İskeletinin Kurulması
### Hedef
Uygulamanın temel Flask klasör yapısını (Application Factory Pattern) kurmak ve projeyi modüler hale getirmek için blueprint'leri oluşturmak. Uygulamanın ileride büyüme ihtimaline karşı baştan temiz bir mimari kurgulamak istedim.
### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3.1 Pro 
Görünüm: Manager
### Verdiğim Prompt
> "İnternet Programcılığı dersi için Flask 3.x tabanlı, uygulama fabrikası (application factory) tasarım desenini ve Blueprint'leri kullanan temiz bir proje iskeleti kur. app/main ve app/auth blueprint'lerini oluştur. Henüz hiçbir model veya route yazma, sadece iskeleti ve requirements.txt gibi konfigürasyon dosyalarını hazırla."
### Ajanın Önerdiği Plan
Ajan bana tam istediğim gibi application factory pattern'a uygun bir klasör ağacı sundu. `app/__init__.py` içinde `create_app()` fonksiyonunu kurguladı ve blueprint kayıt işlemlerini planladı. Ayrıca `.env.example`, `.gitignore` ve `requirements.txt` gibi projenin iskeletini ayakta tutacak yardımcı dosyaları da başarıyla kurguladı.
### Bu Oturumdan Öğrendiğim
Vibe coding sürecinde ajana "bana bir hata takip uygulaması yap" demek yerine, sadece uygulamanın mimari iskeletini kurmasını söylemek çok daha güvenli bir başlangıç oldu. Application factory pattern sayesinde "circular import" (döngüsel içe aktarma) sorunlarının önüne nasıl geçebileceğimi ve projenin kontrolünü başından itibaren nasıl elimde tutacağımı anladım.

---

## Oturum 2: Veritabanı Modellerinin (SQLAlchemy 2.x) Tasarımı
### Hedef
Uygulamanın veritabanı şemasını (User, Project, BugTicket) oluşturmak. İlişkisel veritabanı mantığına uygun olarak tabloları bağlamak ve SQLAlchemy 2.x'in güncel sözdizimini kullanmak.
### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3.1 Pro 
Görünüm: Manager
### Verdiğim Prompt
> "SQLAlchemy 2.x formatını kullanarak User, Project ve BugTicket modellerini oluştur. User modeli Flask-Login için UserMixin'den miras alsın ve şifreleri hashlemek için werkzeug.security fonksiyonları içersin. Bir kullanıcının birden fazla projesi (One-to-Many), bir projenin de birden fazla bug bileti (One-to-Many) olabileceği ilişkileri back_populates kullanarak kur."
### Ajanın Önerdiği Plan
Ajan, eski `db.Column` yapısı yerine tamamen modern `Mapped` ve `mapped_column` sözdizimini kullanarak modelleri taslak halinde sundu. İlişkileri `relationship(back_populates="...")` parametreleriyle doğru bir şekilde kurguladı ve şifre güvenliği için `set_password` ile `check_password` metotlarını User modeline dahil etti.
### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Ajan kodu yazdıktan sonra IDE üzerinde (Antigravity'de) `missing-import` (flask_login, sqlalchemy) gibi uyarılar aldım.
- **Çözüm:** Bu hatanın paketlerin eksik olmasından değil, IDE'nin Python yorumlayıcısının sanal ortamı (venv) görmemesinden kaynaklı görsel bir hata olduğunu fark ettim. Sağ alttan "Select Python Interpreter" diyerek projeye ait `venv` yolunu gösterdiğimde tüm hata bildirimleri ortadan kalktı.
### Bu Oturumdan Öğrendiğim
Eski SQLAlchemy eğitimlerindeki yapılarla 2.x sürümü arasındaki farkları net bir şekilde gördüm. Veritabanı tasarımını koda dökmeden önce plan modunda incelemenin, hatalı tablo ilişkileri kurulmasını engellediğini fark ettim.

---

## Oturum 3: Veritabanını Ayağa Kaldırma ve Flask-Migrate
### Hedef
Yazılan `models.py` dosyasındaki taslağı, Flask-Migrate aracılığıyla fiziksel bir SQLite veritabanına dönüştürmek ve tabloları oluşturmak.
### Görünüm: Editor (Terminal ağırlıklı)
### Karşılaştığım Hatalar ve Çözümler
- **Hata 1:** Terminalde `flask db migrate` komutunu çalıştırdığımda tabloların algılanmasını beklerken `INFO [alembic.env] No changes in schema detected.` şeklinde bir log aldım ve tablolar oluşmadı.
- **Çözüm 1:** Sorunu araştırdığımda, Flask'ın `app/__init__.py` dosyasında modelleri import etmediğimiz için veritabanı şemalarından haberdar olmadığını keşfettim. Ajana `create_app` fonksiyonunun içine `from app import models` satırını eklemesi için kısa bir komut verdim ve sorun çözüldü.
- **Hata 2:** Modeller dosyasının en üstünde yanlışlıkla panodan yapışan `.\venv\Scripts\activate` metni kalmış, bu yüzden terminalde `SyntaxError` aldım. 
- **Çözüm 2:** İlgili satırı manuel olarak bulup sildim, dosyayı kaydettim ve terminal komutlarını (`flask db migrate` ve `flask db upgrade`) tekrar çalıştırarak veritabanı kurulumunu hatasız tamamladım.
### Bu Oturumdan Öğrendiğim
Ajanın mükemmel kod yazmasının yeterli olmadığını; framework'lerin birbirine nasıl bağlandığını (örneğin Flask'ın modellerden haberdar olma mekanizmasını) insan gözüyle kontrol etmenin zorunlu olduğunu öğrendim. Ajan sadece bir asistan, orkestra şefi benim.

---

## Oturum 4: Authentication (Kayıt ve Giriş) Sisteminin Kurulması
### Hedef
Kullanıcıların sisteme güvenli bir şekilde kayıt olabileceği, giriş yapabileceği ve yetkilendirileceği (Flask-Login) altyapıyı tam fonksiyonel olarak kurmak.
### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3.1 Pro 
Görünüm: Manager
### Verdiğim Prompt
> "app/auth blueprint'i içine tam çalışan bir Kayıt (Register), Giriş (Login) ve Çıkış (Logout) sistemi kur. WTForms kullanarak formları oluştur, şifreleri veritabanına werkzeug.security ile hashleyerek kaydet ve CSRF koruması ekle. Template'leri Bootstrap 5 ile modern görünümlü tasarla."
### Ajanın Önerdiği Plan
Ajan; veri doğrulama için `forms.py` (RegisterForm, LoginForm), yönlendirmeler ve hashleme işlemleri için `routes.py` ve kullanıcı arayüzü için HTML dosyalarını içeren kapsamlı bir plan sundu. Ayrıca `login_manager` ve `user_loader` fonksiyonlarını ana projeye entegre edeceğini belirtti.
### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Sunucuyu çalıştırıp kayıt olma ekranında form bilgilerimi girip gönderdiğimde ekranda doğrudan `500 Internal Server Error` hatasıyla karşılaştım.
- **Çözüm:** Hemen terminaldeki Traceback loglarına geri döndüm. Hatayı incelediğimde WTForms'un e-posta doğrulaması (`validate_email`) yapabilmesi için arka planda `email_validator` adlı ekstra bir pakete ihtiyaç duyduğunu (`ModuleNotFoundError: No module named 'email_validator'`) tespit ettim. Sunucuyu durdurup `pip install email-validator` komutunu çalıştırdım, bağımlılığı kurdum ve `requirements.txt` dosyamı güncelledim. Sunucuyu tekrar başlattığımda form sorunsuz çalıştı.
### Bu Oturumdan Öğrendiğim
"Kod üretildi" demek "kod hatasız çalışıyor" demek değildir. Uçtan uca test yapmadan uygulamanın o kısmını bitmiş kabul etmemek gerektiğini ve terminal Traceback loglarının hatanın asıl kaynağını bulmada ne kadar hayati olduğunu çok net bir şekilde tecrübe ettim.

---

## Oturum 5: Ana CRUD İşlevleri (Proje ve Bug Yönetimi)
### Hedef
VibeLog uygulamasının temel amacı olan; kullanıcının projelerini görebileceği (Dashboard), yeni proje ekleyebileceği ve o projelere hata (bug) kayıtları girebileceği ana akışı (CRUD) oluşturmak.
### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager
### Verdiğim Prompt
> "Kullanıcıların kendi projelerini yönetebileceği ve yeni bug ekleyebileceği rotaları oluştur. Ana sayfada kullanıcının projeleri listelensin, detay sayfasında o projeye ait bug'lar listelensin. Sayfalama (pagination) kullan (sayfa başı 10 kayıt) ve en önemlisi yetki kontrolü yap; bir kullanıcı URL'den ID değiştirse bile başkasının projesini göremesin."
### Plan'da Sorguladıklarım ve Üretilen Kodda İncelediklerim
Ajanın `app/main/routes.py` içine yazdığı kodlarda iki şeye özellikle dikkat ettim:
1. Tüm rotalarda `@login_required` decorator'ünün ekli olup olmadığı.
2. Proje detaylarına erişimde `if project.user_id != current_user.id: abort(403)` şeklindeki mantıksal güvenlik kontrolünün (IDOR zafiyetine karşı) bulunup bulunmadığı. Ajan bu yetki kontrolünü başarıyla plana dahil etmişti.
### Bu Oturumdan Öğrendiğim
Backend geliştirirken en önemli konunun veriyi çekmek değil, "bu veriyi kimin çekmeye yetkisi var?" sorusunu sormak olduğunu anladım. Sayfalama (pagination) özelliğinin Flask-SQLAlchemy'de `.paginate()` metodu ile ne kadar kolay entegre edilebildiğini gördüm.

---

## Oturum 6: UI/UX İyileştirmeleri ve Modern Tasarım (Vibe Coding)
### Hedef
Uygulamanın arayüzünü (UI), basit ve sıkıcı varsayılan Bootstrap görünümünden çıkarıp daha modern, kaliteli ve profesyonel bir SaaS dashboard'u hissiyatına kavuşturmak.
### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Editor
### Verdiğim Prompt
> "Arayüzümüzü modern dashboard stiline dönüştürmek istiyorum. Arka plana yumuşak renk geçişli bir gradient ekle. Projeleri ve bug listelerini beyaz kartlar (card) içine al; bunlara hafif bir gölge (box-shadow) ve yuvarlatılmış köşeler ver. Navbar'ı hafif transparan yapıp blur efekti ekle. Status alanlarındaki (Açık/Çözüldü) metinleri Bootstrap'in rounded-pill badge'leri ile tasarla. Bu işlemleri yaparken Jinja kodlarını KESİNLİKLE bozma."
### Bu Oturumdan Öğrendiğim
AI ajanlarına tasarım yaptırırken "bunu daha güzel ve profesyonel yap" gibi muğlak ifadeler kullanmanın genellikle işe yaramadığını fark ettim. Bunun yerine `box-shadow`, `rounded-pill`, `gradient`, `backdrop-filter` gibi spesifik CSS/UI terimlerini kullanarak net direktifler vermek, çok daha başarılı ve istenilen sonuca yakın çıktılar üretmesini sağladı.

---

## Oturum 7: Bug Detay Sayfası ve Güvenlik (Authorization)
### Hedef
Listelenen uzun hata açıklamalarının (description) metin kutularına sığmaması sorununu çözmek için, her bug biletinin kendi detaylarının ve aksiyon butonlarının yer aldığı tekil bir sayfa oluşturmak.
### Kullandığım Mod ve Model
Mod: Plan
Model: Gemini 3.1 Pro
Görünüm: Manager
### Verdiğim Prompt
> "/bug/<int:bug_id> rotası oluştur. Kullanıcı listedeki bug başlığına tıkladığında tüm açıklamayı görebileceği yeni bir bug_detail.html sayfasına yönlendirilsin. Sayfa tasarımı yeni oluşturduğumuz beyaz kart ve gölge stiline uyumlu olsun. En önemlisi, veritabanından çekilen bug'ın bağlı olduğu projenin user_id'si ile o anki current_user.id'yi karşılaştırıp başkasının bug biletine erişimi (403 ile) engelle."
### Plan'da Sorguladıklarım ve Kontrol Ettiklerim
Ajanın getirdiği planda yetki kontrolü mekanizmasının doğruluğundan emin olmak istedim. Ajan, sadece `BugTicket` tablosunu sorgulamakla kalmayıp, ilişki (relationship) üzerinden `bug.project.user_id` özelliğine erişerek doğru bir sahiplik doğrulaması yaptı. Kodu inceleyip güvenlik mantığının kusursuz kurgulandığına ikna olduktan sonra onay verdim.
### Bu Oturumdan Öğrendiğim
Veritabanındaki Foreign Key (Yabancı Anahtar) ve ORM (Object-Relational Mapping) ilişkilerinin pratikte ne kadar işlevsel olduğunu anladım. Bir modele bağlı olan diğer modele geçiş yaparak (`bug.project.user_id` gibi) çapraz yetki kontrollerinin çok temiz bir şekilde yazılabileceğini öğrendim.

## Oturum 8: Profil Özelleştirme ve Veritabanı Migrasyon Krizi
### Hedef
Kullanıcılara avatar yükleme ve "Karanlık Mod (Dark Mode)" seçeneği sunmak için User veritabanı tablosuna yeni sütunlar eklemek.
### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Ajanın yazdığı kodlarla veritabanını güncellerken (upgrade) SQL'den direkt şu hatayı aldım: `Cannot add a NOT NULL column with default value NULL`.
- **Çözüm:** Ajanın Python tarafında varsayılan değer atadığını ama bunu SQL seviyesine yansıtmayı unuttuğunu fark ettim. İçeride zaten kayıtlı kullanıcılar olduğu için SQLite eski kullanıcılara ne değer vereceğini bilemeyip çökmüştü. Migrasyon dosyasına girip `server_default='default.png'` ve karanlık mod için `server_default='0'` parametrelerini manuel olarak ekleyerek sorunu bizzat çözdüm.
### Bu Oturumdan Öğrendiğim
Veritabanı şemalarını güncellerken (özellikle SQLite gibi katı kuralları olan sistemlerde) yapay zekanın yazdığı migrasyon kodlarına körü körüne güvenmemek gerektiğini, arka planda SQL'in nasıl çalıştığını bilmenin hayat kurtardığını anladım.

---

## Oturum 9: CSS ve Bootstrap İnatlaşması
### Hedef
Karanlık modu aktifleştirdiğimde arayüzün tamamen koyu renklere bürünmesini sağlamak.
### Karşılaştığım Hatalar ve Çözümler
- **Hata:** Ajanın yazdığı karanlık mod kodlarını uygulamama rağmen (defalarca Ctrl+F5 atmama rağmen) arayüzün yarısı aydınlık, yarısı karanlık kalıyordu. Beyaz kartlar siyah oluyor ama arka plan inatla parlıyordu. 
- **Çözüm:** Sorunun benim yazdığım CSS'ten değil, `base.html` içindeki hazır Bootstrap `bg-light` class'larından kaynaklandığını teşhis ettim. Ajanın nazik CSS kodları Bootstrap'i ezemiyordu. Ben de `style.css` dosyasına girip karanlık mod için `!important` kalkanını kullanarak arayüze karanlık temayı zorla (override ederek) giydirdim. 
### Bu Oturumdan Öğrendiğim
Front-end geliştirirken framework'lerin (Bootstrap) kendi stillerinin ne kadar baskın (specificity) olabileceğini ve gerektiğinde CSS hiyerarşisini `!important` ile kırmanın arayüz hatalarını kökünden çözdüğünü tecrübe ettim.