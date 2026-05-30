# VibeLog - AI Günlüğü (BLG106 İnternet Programcılığı)

## Oturum 1 - 18 Mayıs 2026 - 19:00-20:30
### Hedef
Uygulamanın temel Flask klasör yapısını (Application Factory Pattern) kurmak ve projeyi modüler hale getirmek için blueprint'leri oluşturmak. Uygulamanın ileride büyüme ihtimaline karşı baştan temiz bir mimari kurgulamak istedim.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Manager

### Verdiğim Promptlar
1. "İnternet Programcılığı dersi için Flask 3.x tabanlı, uygulama fabrikası (application factory) tasarım desenini ve Blueprint'leri kullanan temiz bir proje iskeleti kur. app/main ve app/auth blueprint'lerini oluştur. Henüz hiçbir model veya route yazma, sadece iskeleti ve requirements.txt gibi konfigürasyon dosyalarını hazırla."

### Ajanın Önerdiği Plan
Ajan bana tam istediğim gibi application factory pattern'a uygun bir klasör ağacı sundu. `app/__init__.py` içinde `create_app()` fonksiyonunu kurguladı ve blueprint kayıt işlemlerini planladı. Ayrıca `.env.example`, `.gitignore` ve `requirements.txt` gibi projenin iskeletini ayakta tutacak yardımcı dosyaları da başarıyla kurguladı.

### Plan'da Sorguladıklarım
Ajanın blueprint yapılarını ana dizinde mi yoksa `app` klasöründe mi tutacağını kontrol ettim. İstenilen modüler yapıyı doğru şekilde `app/main` ve `app/auth` olarak ayırdığını görünce onay verdim.

### Üretilen Kodda Düzelttiklerim
- Üretilen `.env.example` dosyasına gereksiz yere veritabanı şifresi gibi değişkenler koymuştu, oraları temizleyip daha genel bir yapıya çevirdim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Yok.
- Çözüm: İlk kurulum aşaması olduğu için temiz ilerledi.

### Bu Oturumdan Öğrendiğim
Vibe coding sürecinde ajana "bana bir hata takip uygulaması yap" demek yerine, sadece uygulamanın mimari iskeletini kurmasını söylemek çok daha güvenli bir başlangıç oldu. Application factory pattern sayesinde "circular import" (döngüsel içe aktarma) sorunlarının önüne nasıl geçebileceğimi ve projenin kontrolünü başından itibaren nasıl elimde tutacağımı anladım.

### Sonraki Oturum İçin Notlar
Bir sonraki adımda, uygulamanın temelini oluşturacak olan veritabanı modellerinin (User, Project, BugTicket) tasarımına geçilecek.

---

## Oturum 2 - 20 Mayıs 2026 - 21:00-22:15
### Hedef
Uygulamanın veritabanı şemasını (User, Project, BugTicket) oluşturmak. İlişkisel veritabanı mantığına uygun olarak tabloları bağlamak ve SQLAlchemy 2.x'in güncel sözdizimini kullanmak.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Manager

### Verdiğim Promptlar
1. "SQLAlchemy 2.x formatını kullanarak User, Project ve BugTicket modellerini oluştur. User modeli Flask-Login için UserMixin'den miras alsın ve şifreleri hashlemek için werkzeug.security fonksiyonları içersin. Bir kullanıcının birden fazla projesi (One-to-Many), bir projenin de birden fazla bug bileti (One-to-Many) olabileceği ilişkileri back_populates kullanarak kur."

### Ajanın Önerdiği Plan
Ajan, eski `db.Column` yapısı yerine tamamen modern `Mapped` ve `mapped_column` sözdizimini kullanarak modelleri taslak halinde sundu. İlişkileri `relationship(back_populates="...")` parametreleriyle doğru bir şekilde kurguladı ve şifre güvenliği için `set_password` ile `check_password` metotlarını User modeline dahil etti.

### Plan'da Sorguladıklarım
İlişkileri kurgularken eski sürüm alışkanlığıyla `backref` kullanıp kullanmadığını kontrol ettim. Modern yaklaşım olan `back_populates` kullandığını görünce plana onay verdim.

### Üretilen Kodda Düzelttiklerim
- Ajan kodun en başına kullanılmayacak birkaç datetime import'u eklemişti, onları silerek dosyayı sadeleştirdim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Ajan kodu yazdıktan sonra IDE üzerinde (Antigravity'de) `missing-import` (flask_login, sqlalchemy) gibi uyarılar aldım.
- Çözüm: Bu hatanın paketlerin eksik olmasından değil, IDE'nin Python yorumlayıcısının sanal ortamı (venv) görmemesinden kaynaklı görsel bir hata olduğunu fark ettim. Sağ alttan "Select Python Interpreter" diyerek projeye ait `venv` yolunu gösterdiğimde tüm hata bildirimleri ortadan kalktı.

### Bu Oturumdan Öğrendiğim
Eski SQLAlchemy eğitimlerindeki yapılarla 2.x sürümü arasındaki farkları net bir şekilde gördüm. Veritabanı tasarımını koda dökmeden önce plan modunda incelemenin, hatalı tablo ilişkileri kurulmasını engellediğini fark ettim.

### Sonraki Oturum İçin Notlar
Oluşturulan modellerin fiziksel SQLite veritabanına dönüştürülmesi için Flask-Migrate işlemleri yapılacak.

---

## Oturum 3 - 21 Mayıs 2026 - 15:00-16:00
### Hedef
Yazılan `models.py` dosyasındaki taslağı, Flask-Migrate aracılığıyla fiziksel bir SQLite veritabanına dönüştürmek ve tabloları oluşturmak.

### Kullandığım Mod ve Model
Mod: Fast 
Model: Gemini 3 Pro 
Görünüm: Editor

### Verdiğim Promptlar
1. "Veritabanını migrate etmek için gereken terminal komutlarında bana asiste ol ve modelleri algılaması için app/__init__.py içindeki gerekli import düzenlemelerini yap."

### Ajanın Önerdiği Plan
Fast modda olduğum için ajan bir plan sunmak yerine doğrudan terminal komutlarını önerdi ve eksik import'ları koda satır içi olarak dahil etmeyi teklif etti.

### Plan'da Sorguladıklarım
Terminal komutlarını sırayla verip vermediğini sorguladım. Doğrudan `upgrade` komutuna geçmediğini, öncesinde `init` ve `migrate` adımlarını uyguladığını gördüm.

### Üretilen Kodda Düzelttiklerim
- `models.py` dosyasının en üstünde ajanın değil, benim panomdan yanlışlıkla yapışan `.\venv\Scripts\activate` metni kalmıştı. Bu satırı manuel olarak silip dosyayı temizledim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Terminalde `flask db migrate` komutunu çalıştırdığımda tabloların algılanmasını beklerken `INFO [alembic.env] No changes in schema detected.` şeklinde bir log aldım.
- Çözüm: Sorunu araştırdığımda, Flask'ın `app/__init__.py` dosyasında modelleri import etmediğimiz için veritabanı şemalarından haberdar olmadığını keşfettim. Ajana `create_app` fonksiyonunun içine `from app import models` satırını eklemesi için komut verdim ve tablolar oluştu.

### Bu Oturumdan Öğrendiğim
Ajanın mükemmel kod yazmasının yeterli olmadığını; framework'lerin birbirine nasıl bağlandığını (örneğin Flask'ın modellerden haberdar olma mekanizmasını) insan gözüyle kontrol etmenin zorunlu olduğunu öğrendim. Ajan sadece bir asistan, orkestra şefi benim.

### Sonraki Oturum İçin Notlar
Kullanıcı giriş-çıkış mekanizmaları için Authentication sistemi kodlanacak.

---

## Oturum 4 - 23 Mayıs 2026 - 20:00-21:30
### Hedef
Kullanıcıların sisteme güvenli bir şekilde kayıt olabileceği, giriş yapabileceği ve yetkilendirileceği (Flask-Login) altyapıyı tam fonksiyonel olarak kurmak.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Manager

### Verdiğim Promptlar
1. "app/auth blueprint'i içine tam çalışan bir Kayıt (Register), Giriş (Login) ve Çıkış (Logout) sistemi kur. WTForms kullanarak formları oluştur, şifreleri veritabanına werkzeug.security ile hashleyerek kaydet ve CSRF koruması ekle. Template'leri Bootstrap 5 ile modern görünümlü tasarla."

### Ajanın Önerdiği Plan
Ajan; veri doğrulama için `forms.py` (RegisterForm, LoginForm), yönlendirmeler ve hashleme işlemleri için `routes.py` ve kullanıcı arayüzü için HTML dosyalarını içeren kapsamlı bir plan sundu. Ayrıca `login_manager` ve `user_loader` fonksiyonlarını ana projeye entegre edeceğini belirtti.

### Plan'da Sorguladıklarım
Formlardan gelen şifreleri düz metin mi (plain text) yoksa hashlenmiş mi kaydedeceğine baktım. `werkzeug.security` paketinden `generate_password_hash` kullanılacağını gördükten sonra onayladım.

### Üretilen Kodda Düzelttiklerim
- `flash()` mesajlarını varsayılan olarak İngilizce bırakmıştı. "Invalid username or password" gibi metinleri manuel olarak "Geçersiz kullanıcı adı veya şifre" şeklinde Türkçeleştirdim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Sunucuyu çalıştırıp kayıt olma ekranında form bilgilerimi girip gönderdiğimde ekranda doğrudan `500 Internal Server Error` hatasıyla karşılaştım.
- Çözüm: Hemen terminaldeki Traceback loglarına döndüm. Hatayı incelediğimde WTForms'un e-posta doğrulaması (`validate_email`) yapabilmesi için `email_validator` adlı ekstra bir pakete ihtiyaç duyduğunu (`ModuleNotFoundError: No module named 'email_validator'`) tespit ettim. Sunucuyu durdurup `pip install email-validator` komutunu çalıştırdım, `requirements.txt` güncelleyip sorunu çözdüm.

### Bu Oturumdan Öğrendiğim
"Kod üretildi" demek "kod hatasız çalışıyor" demek değildir. Uçtan uca test yapmadan uygulamanın o kısmını bitmiş kabul etmemek gerektiğini ve terminal Traceback loglarının hatanın asıl kaynağını bulmada ne kadar hayati olduğunu tecrübe ettim.

### Sonraki Oturum İçin Notlar
Uygulamanın ana çekirdeği olan proje ve bug yönetim sayfaları (CRUD işlemleri) kodlanacak.

---

## Oturum 5 - 25 Mayıs 2026 - 19:00-20:30
### Hedef
VibeLog uygulamasının temel amacı olan; kullanıcının projelerini görebileceği (Dashboard), yeni proje ekleyebileceği ve o projelere hata (bug) kayıtları girebileceği ana akışı (CRUD) oluşturmak.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Manager

### Verdiğim Promptlar
1. "Kullanıcıların kendi projelerini yönetebileceği ve yeni bug ekleyebileceği rotaları oluştur. Ana sayfada kullanıcının projeleri listelensin, detay sayfasında o projeye ait bug'lar listelensin. Sayfalama (pagination) kullan (sayfa başı 10 kayıt) ve en önemlisi yetki kontrolü yap; bir kullanıcı URL'den ID değiştirse bile başkasının projesini göremesin."

### Ajanın Önerdiği Plan
Ajan `app/main/routes.py` içerisine CRUD işlemleri için get/post rotalarını içeren geniş bir yapı önerdi. Projeleri çekmek için SQLAlchemy sorgularını hazırladı.

### Plan'da Sorguladıklarım
Tüm rotalara yetkilendirme katmanının eklendiğinden emin olmak istedim. Proje detaylarına erişimde `if project.user_id != current_user.id: abort(403)` şeklindeki mantıksal güvenlik kontrolünün (IDOR zafiyetine karşı) bulunup bulunmadığını kontrol edip onayladım.

### Üretilen Kodda Düzelttiklerim
- Sayfalama (pagination) butonları çalışıyordu fakat varsayılan tasarımları çok bozuktu. Ajanın ürettiği HTML etiketlerine arayüze uygun Bootstrap class'larını (`page-item`, `page-link`) manuel ekledim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Yeni proje ekleme rotasında yetki hatası aldım.
- Çözüm: Ajan, görünümü koruyan `@login_required` decorator'ünü bir rotada unutmuştu, sadece içeride `current_user` sorgusu yapıyordu. Decorator'ü ekleyerek çözdüm.

### Bu Oturumdan Öğrendiğim
Backend geliştirirken en önemli konunun veriyi çekmek değil, "bu veriyi kimin çekmeye yetkisi var?" sorusunu sormak olduğunu anladım. Sayfalama özelliğinin Flask-SQLAlchemy'de `.paginate()` metodu ile ne kadar kolay entegre edilebildiğini gördüm.

### Sonraki Oturum İçin Notlar
Uygulamanın genel UI/UX tasarımı düzeltilecek, klasik Bootstrap görünümünden kurtulunacak.

---

## Oturum 6 - 27 Mayıs 2026 - 21:00-22:30
### Hedef
Uygulamanın arayüzünü (UI), basit ve sıkıcı varsayılan Bootstrap görünümünden çıkarıp daha modern, kaliteli ve profesyonel bir SaaS dashboard'u hissiyatına kavuşturmak.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Editor

### Verdiğim Promptlar
1. "Arayüzümüzü modern dashboard stiline dönüştürmek istiyorum. Arka plana yumuşak renk geçişli bir gradient ekle. Projeleri ve bug listelerini beyaz kartlar (card) içine al; bunlara hafif bir gölge (box-shadow) ve yuvarlatılmış köşeler ver. Navbar'ı hafif transparan yapıp blur efekti ekle. Status alanlarındaki (Açık/Çözüldü) metinleri Bootstrap'in rounded-pill badge'leri ile tasarla. Bu işlemleri yaparken Jinja kodlarını KESİNLİKLE bozma."

### Ajanın Önerdiği Plan
UI elementleri için güncel Bootstrap class'ları ve bu class'ları destekleyecek custom bir CSS yapısı planladı. Jinja değişkenlerini koruyan yeni HTML blokları önerdi.

### Plan'da Sorguladıklarım
Yapılacak CSS eklentilerinin ve div değişikliklerinin `for` döngülerini veya `if` koşullarını sağlayan Jinja kodlarını ezip bozmadığını satır satır inceledim.

### Üretilen Kodda Düzelttiklerim
- Ajanın eklediği saydamlık ve blur oranlarını (backdrop-filter) o sevdiğim cam ve neon arası hissiyata daha çok uyması için kendi zevkime göre editledim. Navbar arkaplan rengini biraz daha kısarak transparanlığı artırdım.

### Karşılaştığım Hatalar ve Çözümler
Hata: Kartlara eklenen gölgeler (box-shadow) mobil görünümde taşma yaptı ve ekranı sağa doğru kaydırılabilir (horizontal scroll) hale getirdi.
- Çözüm: Konteynerlara eklenen paddingleri (`p-3`) daraltıp gölge yayılım alanını küçülterek responsive sorunu çözdüm.

### Bu Oturumdan Öğrendiğim
AI ajanlarına tasarım yaptırırken "bunu daha güzel ve profesyonel yap" gibi muğlak ifadeler kullanmanın pek işe yaramadığını fark ettim. Bunun yerine `box-shadow`, `rounded-pill`, `gradient`, `backdrop-filter` gibi spesifik CSS terimlerini kullanarak net direktifler vermek, çok daha başarılı çıktılar üretti.

### Sonraki Oturum İçin Notlar
Bug detaylarına girildiğinde uzun metinleri rahat okumak için yeni bir detay sayfası tasarlanacak.

---

## Oturum 7 - 28 Mayıs 2026 - 18:00-19:30
### Hedef
Listelenen uzun hata açıklamalarının metin kutularına sığmaması sorununu çözmek için, her bug biletinin kendi detaylarının ve aksiyon butonlarının yer aldığı tekil bir sayfa oluşturmak.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Manager

### Verdiğim Promptlar
1. "/bug/<int:bug_id> rotası oluştur. Kullanıcı listedeki bug başlığına tıkladığında tüm açıklamayı görebileceği yeni bir bug_detail.html sayfasına yönlendirilsin. Sayfa tasarımı yeni oluşturduğumuz beyaz kart ve gölge stiline uyumlu olsun. En önemlisi, veritabanından çekilen bug'ın bağlı olduğu projenin user_id'si ile o anki current_user.id'yi karşılaştırıp başkasının bug biletine erişimi (403 ile) engelle."

### Ajanın Önerdiği Plan
Ajan yeni bir rota ve template yapısı önerdi. Detayları çekerken SQLAlchemy ilişki (relationship) üzerinden güvenlik duvarını plana dahil etti.

### Plan'da Sorguladıklarım
Ajanın yetki kontrolü mekanizmasının doğruluğundan emin olmak istedim. Sadece `BugTicket` tablosunu sorgulamakla kalmayıp, ilişki üzerinden `bug.project.user_id` özelliğine erişerek doğru bir sahiplik doğrulaması yaptığını teyit ettim.

### Üretilen Kodda Düzelttiklerim
- HTML tarafında her şeyi yapmıştı ancak kullanıcıların detay sayfasından önceki listeye dönmesi için bir "Geri Dön" butonu koymayı unutmuştu. Manuel olarak `url_for('main.index')` yönlendirmesi yapan bir buton ekledim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Yok. 
- Çözüm: Kontroller sıkı tutulduğu için sorunsuz entegre edildi.

### Bu Oturumdan Öğrendiğim
Veritabanındaki Foreign Key ve ORM ilişkilerinin pratikte ne kadar işlevsel olduğunu anladım. Bir modele bağlı olan diğer modele geçiş yaparak (`bug.project.user_id` gibi) çapraz yetki kontrollerinin çok temiz bir şekilde yazılabileceğini öğrendim.

### Sonraki Oturum İçin Notlar
Kullanıcılara avatar ve tema seçeneği (dark mode) sunmak için veritabanına ek sütunlar eklenecek.

---

## Oturum 8 - 29 Mayıs 2026 - 21:00-22:30
### Hedef
Kullanıcılara avatar yükleme ve "Karanlık Mod (Dark Mode)" seçeneği sunmak için User veritabanı tablosuna yeni sütunlar eklemek.

### Kullandığım Mod ve Model
Mod: Plan 
Model: Gemini 3 Pro 
Görünüm: Manager

### Verdiğim Promptlar
1. "User modeline avatar dosya adını tutacak bir sütun ve kullanıcının karanlık mod tercihini tutacak boolean bir sütun ekle. Ardından bu değişiklikleri uygulamak için gereken migrasyon dosyalarını oluştur."

### Ajanın Önerdiği Plan
User modelini güncelledi ve terminalde çalıştırılmak üzere `flask db migrate` komutunu plana ekledi.

### Plan'da Sorguladıklarım
Sütunlar eklendikten sonra mevcut kullanıcılara varsayılan olarak ne değer atanacağını düşündüm. Ajan planında bunu atlamıştı. 

### Üretilen Kodda Düzelttiklerim
- Migrasyon dosyasına girip mevcut satırların çökmemesi için `server_default='default.png'` ve karanlık mod için `server_default='0'` parametrelerini manuel olarak ekledim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Ajanın yazdığı kodlarla veritabanını güncellerken (upgrade) SQL'den şu hatayı aldım: `Cannot add a NOT NULL column with default value NULL`.
- Çözüm: Ajanın Python tarafında varsayılan değer atadığını ama bunu SQL seviyesine yansıtmayı unuttuğunu fark ettim. İçeride zaten kayıtlı kullanıcılar olduğu için SQLite eski kullanıcılara ne değer vereceğini bilemeyip çökmüştü. Yukarıda bahsettiğim `server_default` eklemelerini bizzat yaparak sorunu aştım.

### Bu Oturumdan Öğrendiğim
Veritabanı şemalarını güncellerken (özellikle SQLite gibi katı kuralları olan sistemlerde) yapay zekanın yazdığı migrasyon kodlarına körü körüne güvenmemek gerektiğini, arka planda SQL'in nasıl çalıştığını bilmenin hayat kurtardığını anladım.

### Sonraki Oturum İçin Notlar
Eklenen karanlık mod özelliğinin CSS/UI kısmındaki uyumsuzlukları giderilecek.

---

## Oturum 9 - 30 Mayıs 2026 - 14:00-15:30
### Hedef
Karanlık modu aktifleştirdiğimde arayüzün tamamen koyu renklere bürünmesini sağlamak ve tasarım hatalarını çözmek.

### Kullandığım Mod ve Model
Mod: Fast 
Model: Gemini 3 Pro 
Görünüm: Editor

### Verdiğim Promptlar
1. "Karanlık modu aktifleştirdiğimde arkaplan hala beyaz kalıyor. Bootstrap'in hazır bg-light class'larını ezip karanlık modu nasıl aktif tutabilirim?"

### Ajanın Önerdiği Plan
Ajan doğrudan `style.css` dosyasında değişiklik yapmayı ve Bootstrap class'larını ezmek için `!important` kuralını uygulamayı önerdi.

### Plan'da Sorguladıklarım
Bu radikal `!important` eklentilerinin, standart aydınlık modu kullanmak isteyen kullanıcıların arayüzünü bozup bozmayacağını kontrol ettim. Değişiklikleri sadece `body.dark-mode` gibi özel bir wrapper sınıfın altında yaptığı için onayladım.

### Üretilen Kodda Düzelttiklerim
- Sadece arkaplan rengini düzeltmesi yetmedi; beyaz kartları siyaha çevirdiğinde içerideki yazılar da siyah kalıyordu. Yazı renklerini de beyaza çeviren (color: #fff !important) satırlarını koda ben ekledim.

### Karşılaştığım Hatalar ve Çözümler
Hata: Ajanın yazdığı kodları uygulamama rağmen arayüzün yarısı aydınlık, yarısı karanlık kalıyordu. Beyaz kartlar siyah oluyor ama arka plan inatla parlıyordu.
- Çözüm: Sorunun `base.html` içindeki Bootstrap `bg-light` class'larından kaynaklandığını teşhis ettim. Ajanın nazik CSS kodları Bootstrap'i ezemiyordu. CSS hiyerarşisini `!important` kalkanıyla kırarak sorunu temelden hallettim.

### Bu Oturumdan Öğrendiğim
Front-end geliştirirken framework'lerin (Bootstrap) kendi stillerinin ne kadar baskın (specificity) olabileceğini ve gerektiğinde CSS hiyerarşisini ezmenin arayüz hatalarını kökünden çözdüğünü tecrübe ettim.

### Sonraki Oturum İçin Notlar
Uygulama yayına (deploy) hazırlanacak ve projenin genel raporu yazılacak.
