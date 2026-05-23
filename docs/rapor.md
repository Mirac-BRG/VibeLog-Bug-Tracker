# BLG106 İnternet Programcılığı - Dönem Projesi Raporu
**Proje Adı:** VibeLog (Hata Takip ve Yönetim Sistemi)
**Geliştirici:** [Muhammed Miraç BÜRGE]
**Öğrenci No:** [25380102012]
**Kurum:** Gazi Üniversitesi - TUSAŞ Kazan Meslek Yüksek Okulu

---

## 1. Projenin Amacı ve Ne İşe Yaradığı
VibeLog, bağımsız yazılım geliştiricilerin ve bilgisayar programcılığı öğrencilerinin (özellikle kendi geliştirdikleri SoundVibe gibi kişisel projelerinde) karşılaştıkları yazılım hatalarını (bug) merkezi, düzenli ve modern bir arayüz üzerinden takip etmelerini sağlayan dinamik bir web uygulamasıdır. Günümüzde öğrenciler veya bağımsız geliştiriciler, projelerindeki hataları genellikle Not Defteri gibi geçici ortamlarda tutmakta ya da Jira gibi çok karmaşık, kurumsal ve ağır araçlar içinde kaybolmaktadır. VibeLog, bu iki uç noktanın arasında durarak kullanıcıların kendi projelerini sisteme tanımlamasına, karşılaştıkları hataları detaylı bir açıklamayla not almasına ve bu hataların "Açık/Çözüldü" durumlarını tek bir dashboard üzerinden kolayca yönetmesine olanak tanımaktadır.

## 2. Mimari Özet (Klasör Yapısı ve Ana Akışlar)
Proje, büyüme potansiyeli göz önünde bulundurularak Flask'ın en iyi pratiklerinden biri olan **Application Factory Pattern (Uygulama Fabrikası Deseni)** üzerine inşa edilmiştir. Tüm sistem monolitik bir `app.py` dosyasına yığılmak yerine modüler bir yapıya bölünmüştür.

**Ana Klasör Yapısı:**
* `app/`: Uygulamanın kalbini oluşturan ana modül.
    * `__init__.py`: Flask uygulamasının, veritabanının (db), Flask-Migrate ve Flask-Login eklentilerinin başlatıldığı fabrika fonksiyonunu (`create_app`) içerir.
    * `auth/` (Blueprint): Kullanıcı kayıt, giriş ve çıkış işlemlerinin (`/register`, `/login`, `/logout`) yönetildiği kimlik doğrulama modülü.
    * `main/` (Blueprint): Projelerin listelenmesi, yeni proje/bug eklenmesi ve detayların görüntülenmesi gibi uygulamanın ana (CRUD) işlevlerini barındıran modül.
    * `models.py`: Veritabanı tablolarının (User, Project, BugTicket) SQLAlchemy 2.x standardı ile (Mapped, mapped_column) modellendiği dosya.
    * `templates/` & `static/`: HTML şablonlarının ve CSS dosyalarının bulunduğu, Bootstrap 5 destekli sunum katmanı.
* `migrations/`: Veritabanı şema değişikliklerinin (Alembic) versiyonlandığı klasör.

**Ana Akış:** Kayıtsız bir kullanıcı sistemi açtığında `@login_required` sayesinde doğrudan `auth.login` rotasına yönlendirilir. Giriş yapan kullanıcı, `main.index` rotasında kendi projelerini (One-to-Many ilişkisi) görür. Bir projeye tıkladığında `main.project_detail` rotası tetiklenir ve sadece o projeye ait hata biletleri çekilerek (pagination ile) listelenir.

## 3. Vibe Coding Deneyimim: Ne İşe Yaradı, Nerede Zorlandım?
Vibe coding (ajan destekli geliştirme) yaklaşımı, geleneksel "satır satır kod yazma" zihniyetimi "sistem mimarisi tasarlama" zihniyetine dönüştürdü. 
* **Ne İşe Yaradı:** Özellikle uygulamanın başlangıç iskeletini (klasör yapıları, `requirements.txt`, blueprint bağlantıları) kurarken inanılmaz bir zaman tasarrufu sağladı. Geliştirici olarak syntax (sözdizimi) ezberlemek veya boilerplate kodlar yazmak yerine, "Uygulamanın veritabanı ilişkileri nasıl olmalı?" veya "Yetkilendirme mimarisi nasıl çalışmalı?" gibi daha üst düzey mühendislik kararlarına odaklanabildim. 
* **Nerede Zorlandım:** Ajanın verdiği kodları doğrudan çalıştırmanın her zaman güvenli olmadığını anladığımda zorlandım. Yapay zeka ajanları bazen bağlamı unutabiliyor veya Python sanal ortam (venv) yollarını karıştırabiliyor (örneğin koda yanlışlıkla terminal komutu yapıştırması gibi). Ayrıca arayüz tasarımı konusunda ajana "bunu daha güzel yap" demek yerine "box-shadow ve rounded-pill kullan" gibi çok spesifik teknik CSS terimleri vermek gerektiğini tecrübe ettim. Vibe coding, ajana emir vermek değil, ajanı doğru yönlendirme sanatıdır.

## 4. Antigravity'de En Faydalı Bulduğum 2 Özellik
1.  **Manager View ve Plan Modu:** Büyük çaplı özellikleri (örneğin Authentication sistemi) kurarken ajan, kodu direkt yazmak yerine önce bir Plan sundu. Bu özellik, ajanın yanlış bir yola (örneğin eski SQLAlchemy 1.x sürümünü kullanmaya) sapmasını engelledi. Koda dökülmeden önce planı okuyup onaylamak, kontrolün tamamen bende kalmasını sağladı.
2.  **Terminal Sandbox ve Request Review Güvenliği:** Antigravity ayarlarından "Terminal Command Auto Execution" seçeneğini "Request Review" olarak ayarlamak hayatiydi. Ajan, klasörleri oluşturmak veya `flask db migrate` yapmak istediğinde benden onay almak zorundaydı. Bu sayede ajanın arka planda gizlice sistemimde işlem yapmasını veya projeyi bozacak zararlı bir komut çalıştırmasını fiziksel olarak engellemiş oldum.

## 5. Ajanın Yakalayıp Düzelttiğim En Kritik 3 Hatası
Süreç boyunca ajanın ürettiği çıktılarda körü körüne kabul etmediğim ve düzelttiğim 3 kritik an şunlardı:
1.  **Eksik Bağımlılık (email_validator) Hatası:** Ajan kayıt (Register) formunu WTForms ile oluştururken e-posta alanı için `validate_email` filtresini kullandı ancak `email_validator` kütüphanesini indirmeyi unuttu. Bu durum sunucuda doğrudan 500 Internal Server Error fırlattı. Hatayı Traceback loglarından tespit edip, paketi manuel olarak `pip` ile kurdum ve `requirements.txt` dosyasını güncelleyerek çözdüm.
2.  **Modellerin Flask'a Tanıtılmaması:** Ajan veritabanı modellerini kusursuz tasarladı ancak `flask db migrate` yaptığımda "No changes in schema detected" hatası aldım. Ajanın `app/__init__.py` içindeki `create_app` fonksiyonunda modelleri import etmeyi (uygulamaya tanıtmayı) unuttuğunu fark ettim ve `from app import models` satırını manuel ekleterek veritabanının oluşmasını sağladım.
3.  **Güvenlik - Yetki Kontrolü (Authorization) Teşhisi:** CRUD rotalarını tasarlarken ajan sadece veriyi çekmeye odaklanabilirdi. Planda ajanın IDOR (Insecure Direct Object Reference) zafiyetine karşı bir önlem alıp almadığını sıkı bir şekilde sorguladım. Ajanın `if bug.project.user_id != current_user.id: abort(403)` şeklindeki güvenlik kontrolünü planladığını görünce bunu tasdikledim ve kodun güvenli olduğundan emin olduktan sonra onayladım.

## 6. Projeyi Sıfırdan AI Olmadan Yapsaydım Ne Kadar Sürerdi?
Eğer bu projeyi hiçbir yapay zeka asistanı kullanmadan, tamamen klasik yöntemlerle (dokümantasyon okuyarak, StackOverflow'da hata arayarak) geliştirseydim, tahminen **2 ila 3 haftalık (yaklaşık 40-50 saatlik) yoğun bir mesai** harcamam gerekirdi. Sadece SQLAlchemy 2.x'in yeni Mapped yapısını kavramak, Flask-Login ile güvenli bir auth mimarisi kurmak ve Application Factory pattern'deki "circular import" sorunlarını çözmek bile güncemi alırdı. Vibe coding sayesinde bu süreci odaklanmış birkaç oturuma sığdırarak hem çok daha hızlı sonuç aldım hem de hatasız çalışan bir ürün ortaya çıkardım.

## 7. Bu Projeyi Sürdürürsem Bir Sonraki Adım Ne Olur?
VibeLog projesini geliştirip ölçeklendirmek istersem ilk yapacağım geliştirme, projeye **"Kullanıcı Rolleri (User Roles)"** eklemek olurdu. Şirket mantığına uyarlayarak projeleri yöneten bir "Admin" ve sadece bug kayıtlarını görüp çözen "Developer" hesapları oluştururdum. İkinci adım olarak bir bug "Çözüldü" olarak işaretlendiğinde projeye dahil olan diğer kullanıcılara otomatik e-posta gidecek bir e-posta bildirim (notification) servisi entegre ederdim. Son olarak, uygulamanın verilerini farklı platformlarda kullanabilmek için bir `/api/v1/projects` RESTful API endpoint'i yazardım.