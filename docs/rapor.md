# BLG106 İnternet Programcılığı - Dönem Projesi Raporu

**Proje Adı:** VibeLog (Hata Takip ve Yönetim Sistemi)  
**Geliştirici:** Muhammed Miraç BÜRGE  
**Öğrenci No:** 25380102012  
**Kurum:** Gazi Üniversitesi - TUSAŞ Kazan Meslek Yüksek Okulu  

---

## 1. Projenin Amacı ve Ne İşe Yaradığı
VibeLog, bağımsız yazılım geliştiricilerin, küçük ekiplerin ve bilgisayar programcılığı öğrencilerinin geliştirme süreçlerinde karşılaştıkları yazılım hatalarını (bug) merkezi, sistematik ve modern bir arayüz üzerinden takip etmelerini sağlayan dinamik bir web uygulamasıdır. Özellikle eğitim hayatı boyunca geliştirilen kişisel projelerde (örneğin daha önce üzerinde çalıştığım SoundVibe müzik çalar veya Kardeşler Pide Fırını oyunu gibi bağımsız konseptlerde) ortaya çıkan kod hataları genellikle geçici not defterlerinde kaybolmakta ya da planlı bir şekilde belgelenememektedir. Diğer taraftan, kurumsal piyasada kullanılan Jira veya Azure DevOps gibi devasa platformlar ise hem çok karmaşık, ağır ve maliyetlidir hem de bireysel geliştiriciler ile öğrenciler için ciddi bir öğrenme eğrisi barındırmaktadır.

VibeLog, bu iki uç nokta arasında köprü vazifesi görerek tam olarak ihtiyaç duyulan ölçekte bir çözüm sunar. Kullanıcılar, platform üzerinde kendi projelerini esnek bir şekilde tanımlayabilir, bu projelere bağlı hata biletleri (bug tickets) oluşturabilir, hataların teknik detaylarını, önem derecelerini ve güncel durumlarını ("Açık" / "Çözüldü") tek bir merkezi dashboard üzerinden anlık olarak yönetebilirler. Uygulama, geliştiriciye hataları kategorize etme ve geçmişe dönük izlenebilirlik sağlama imkanı sunarak, yazılım kalitesini ve proje yönetim disiplinini artırmayı hedefler.

## 2. Mimari Özet (Klasör Yapısı ve Ana Akışlar)
Proje, ileride eklenebilecek yeni modüller ve genişleme potansiyeli göz önünde bulundurularak Flask framework'ünün en iyi pratiklerinden biri olan **Application Factory Pattern (Uygulama Fabrikası Tasarım Deseni)** temelleri üzerine inşa edilmiştir. Tüm sistemin monolitik, yönetilmesi imkansız tek bir kod dosyasına yığılması engellenmiş; sorumlulukların ayrılması (Separation of Concerns) ilkesine sadık kalınarak modüler bileşenlere bölünmüştür.

```text
VibeLog/
│
├── app/
│   ├── __init__.py          # Uygulama fabrikası (create_app) ve eklentilerin başlatılması
│   ├── models.py            # SQLAlchemy 2.x Mapped modelleri (User, Project, BugTicket)
│   │
│   ├── auth/                # Kimlik doğrulama Blueprint modülü
│   │   ├── forms.py         # Flask-WTF giriş/kayıt form tanımları
│   │   └── routes.py        # /login, /register, /logout rotaları ve auth mantığı
│   │
│   ├── main/                # Ana uygulama işlevleri Blueprint modülü
│   │   └── routes.py        # Proje/Hata CRUD operasyonları ve yetki kontrolleri
│   │
│   ├── static/              # CSS arayüz dosyaları ve custom stiller
│   └── templates/           # Jinja2 şablonları (base.html, auth/ ve main/ alt klasörleri)
│
├── migrations/              # Flask-Migrate / Alembic veritabanı göç dosyaları
├── tests/                   # Pytest birim testleri
├── config.py                # Ortam değişkenleri ve konfigürasyon sınıfları
├── requirements.txt         # Proje bağımlılık listesi
└── run.py                   # Uygulamayı başlatan ana script
```

### Sistem Ana Akış Diyagramı
Uygulamanın istek döngüsü, veritabanı ilişkileri ve yönlendirme mimarisi aşağıdaki şema üzerinden yürütülmektedir:

```mermaid
graph TD
    A[Kullanıcı / Tarayıcı] -->|İstek Gönderir| B[Uygulama Fabrikası: create_app]
    B -->|Uygulama Durumunu Başlatır| C{Kullanıcı Oturumu Açık mı?}
    C -- Hayır -->|@login_required Koruması| D[Auth Blueprint: /login]
    C -- Evet -->|Rotaları Eşleştir| E[Main Blueprint: /index]
    
    D -->|Kimlik Doğrulama| F[(SQLAlchemy Modeli: User)]
    E -->|Veri Çekme / CRUD| G[(SQLAlchemy Modeli: Project)]
    G -->|One-to-Many İlişkisi| H[(SQLAlchemy Modeli: BugTicket)]
    
    F -->|Jinja2 Şablonu ile Çıktı Üret| I[Kullanıcı Arayüzü / Bootstrap 5]
    H -->|Jinja2 Şablonu ile Çıktı Üret| I
```

Sistemde veritabanı katmanı SQLAlchemy 2.x standartlarına uygun olarak `Mapped` ve `mapped_column` kullanılarak kurgulanmıştır. `User` ile `Project` modelleri arasında, `Project` ile `BugTicket` modelleri arasında bire-çok (One-to-Many) ilişkiler `relationship(back_populates=...)` parametreleriyle çift yönlü olarak bağlanmıştır. Bu sayede bir proje silindiğinde ona bağlı tüm hata biletlerinin otomatik olarak temizlenmesi (cascade delete) sağlanarak veritabanı bütünlüğü (integrity) korunmuştur.

## 3. Vibe Coding Deneyimim: Ne İşe Yaradı, Nerede Zorlandım?
Antigravity editörü ve entegre yapay zeka ajanları ile yürüttüğüm "Vibe Coding" süreci, geleneksel yazılım geliştirme alışkanlıklarımı kökten değiştiren, ufuk açıcı bir deneyim oldu. Bu yaklaşım, beni satır satır kod yazan bir "kod işçisi" konumundan çıkartıp, projenin yüksek seviyeli mimarisini, veri akışını ve güvenlik adımlarını tasarlayan bir "yazılım mimarı" rolüne konumlandırdı.

* **Ne İşe Yaradı:** Özellikle projenin ilk ayağa kaldırılma evresinde, klasör hiyerarşisinin kurulmasında, boilerplate (basmakalıp) konfigürasyon dosyalarının hatasız oluşturulmasında yapay zeka ajanı inanılmaz bir sürat kazandırdı. Normal şartlarda elle yazarken circular import (döngüsel içe aktarma) hatasına düşme riski yüksek olan Application Factory desenini, ajan sayesinde dakikalar içinde temiz bir şekilde kurabildim. Syntax ezberleme yükünü hafifleterek tamamen mantıksal tasarıma odaklanmamı sağladı.
* **Nerede Zorlandım:** En çok zorlandığım nokta, ajanın bazen projenin mevcut bağlamından (context) koparak eski veya alternatif kütüphane standartlarına (örneğin SQLAlchemy 1.x stilindeki `db.Column` yapısına) yönelme eğilimi göstermesi oldu. Bu durum, yapay zekanın ürettiği her satırı satır satır okumanın ve teknik denetim yapmanın ne kadar hayati olduğunu gösterdi. Ayrıca tasarım aşamasında ajana "modern ve güzel bir arayüz yap" gibi soyut ve göreceli komutlar verdiğimde başarısız, kaotik sonuçlar aldım. Yapay zekadan doğru çıktıyı alabilmek için `box-shadow`, `backdrop-filter: blur`, `gradient arkaplan` gibi nokta atışı, somut teknik terimlerle konuşmam gerektiğini keşfettim.

## 4. Antigravity'de En Faydalı Bulduğum 2 Özellik
Geliştirme sürecini Antigravity üzerinde yürütürken projenin kalitesini doğrudan etkileyen ve en çok fayda sağladığım iki temel özellik şunlardır:

1. **Manager View ve Plan Modu Disiplini:** Kompleks ve çok dosyayı etkileyen büyük özellikleri (örneğin kullanıcı kayıt ve giriş akışının uçtan uca yazılması) devreye alırken Plan Modu bir cankurtaran görevi gördü. Ajanın tek bir satır bile kod üretmeden önce atacağı tüm adımları, oluşturacağı dosyaları ve kuracağı mantığı bir "Plan Artifact" olarak önüme sunması, süreç üzerindeki kontrolümü maksimize etti. Yanlış mimari kararları daha kod yazılmadan plan aşamasında sorgulayıp revize ettirerek zaman kayıplarının önüne geçtim.
2. **Terminal Sandbox ve Request Review Güvenlik Politikası:** Bir bilişim güvenliği öğrencisi olarak sistemimde kontrolsüz komut çalıştırılmasına her zaman mesafeli yaklaşırım. Antigravity'nin terminal komut çalıştırma politikasını "Request Review" moduna çekerek, ajanın kendi kafasına göre arka planda veritabanı silme, paket yükleme veya işletim sistemi komutları çalıştırmasını fiziksel olarak engelledim. Ajanın ürettiği her terminal komutunu (`flask db migrate` dahil) önce inceleyip onay vererek sisteme işletmem, projenin güvenlik ve kararlılık düzeyini en üst seviyede tuttu.

## 5. Ajanın Yakalayıp Düzelttiğim En Kritik 3 Hatası
Süreç boyunca yapay zekanın "ürettiği her kod kusursuzdur" yanılgısına düşmeyerek, dikkatli bir kod incelemesi (code review) ve terminal takibiyle yakalayıp düzelttiğim 3 kritik hata şu şekildedir:

### Hata 1: Eksik Bağımlılık (email_validator) ve Sunucu Çökmesi
Ajan, kullanıcı kayıt formunu (`RegisterForm`) Flask-WTF ve WTForms kütüphanelerini kullanarak inşa ederken e-posta alanının doğrulanması için yerleşik `Email()` validator'ını koda dahil etti. Ancak bu filtre arka planda çalışan üçüncü parti `email_validator` paketine ihtiyaç duymaktadır ve ajan bunu `requirements.txt` dosyasına eklemeyi unuttu. Uygulamayı ayağa kaldırıp ilk kayıt denemesini yaptığımda sistem doğrudan `500 Internal Server Error` vererek çöktü. Terminaldeki Traceback loglarını inceleyerek `ModuleNotFoundError: No module named 'email_validator'` hatasını teşhis ettim. Sunucuyu durdurup paketi manuel kurdum, bağımlılık dosyasını güncelleyerek hatayı giderdim.

### Hata 2: Flask Fabrikasında Modellerin Unutulması ve Şema Körlüğü
Veritabanı şemasını oluşturup `flask db init` komutunu çalıştırdıktan sonra, modelleri fiziksel veritabanına işlemek için `flask db migrate` komutunu yürüttüm. Ancak terminalde `INFO [alembic.env] No changes in schema detected.` uyarısı aldım ve tablolar bir türlü oluşturulmadı. Kodu incelediğimde, ajanın modelleri `models.py` içinde yazmasına rağmen, ana uygulama fabrikasının (`app/__init__.py`) bu dosyanın varlığından haberdar olmadığını, yani import etmediğini fark ettim. Ajana müdahale ederek `create_app` fonksiyonunun gövdesine `from app import models` satırını zorunlu olarak eklettim ve Flask-Migrate'in şemayı sorunsuz algılamasını sağladım.

### Hata 3: SQLite Sütun Güncelleme Krizi (NOT NULL Constraint)
Projenin ilerleyen aşamalarında kullanıcılara avatar yükleme ve karanlık mod desteği eklemek istedik. Ajan model dosyasına gerekli sütunları ekledi ve migrasyon scriptini üretti. Ancak `flask db upgrade` komutunu çalıştırdığımda SQLite veritabanı `Cannot add a NOT NULL column with default value NULL` hatası fırlatarak işlemi iptal etti. Hataya sebep olan durum; içeride zaten kayıtlı kullanıcıların bulunması ve yeni eklenen `NOT NULL` işaretli sütunlara geçmişe dönük ne değer verileceğinin veritabanı seviyesinde belirtilmemiş olmasıydı. Üretilen göç (migration) dosyasının içine manuel olarak müdahale ederek SQL komutlarına `server_default='default.png'` ve `server_default='0'` argümanlarını ekledim, böylece veritabanı bütünlüğünü çökertmeden yapıyı başarıyla güncelledim.

## 6. Projeyi Sıfırdan AI Olmadan Yapsaydım Ne Kadar Sürerdi?
Eğer bu projeyi hiçbir yapay zeka desteği almadan, tamamen geleneksel yöntemlerle (StackOverflow aramaları, resmi Flask, WTForms ve SQLAlchemy dokümantasyonlarını satır satır okuma, hata ayıklama süreçleri) tek başıma geliştirmeye çalışsaydım, tahminen **2 ila 3 haftalık bir zaman dilimine yayılan, yaklaşık 40-50 saatlik yoğun bir saf mesai** harcamam gerekirdi.

Özellikle SQLAlchemy 2.x'in getirdiği yeni birleşik sorgu mantığını kavramak, Application Factory pattern mimarisinde yaşanabilecek olası import çakışmalarını manuel temizlemek ve Bootstrap elementlerinin custom CSS ile responsive (mobil uyumlu) hale getirilmesi süreçleri tek başına ciddi bir zaman maliyeti doğuracaktı. Vibe coding metodolojisi, bu süreyi mantıklı ve odaklanmış 9 oturuma indirgeyerek (yaklaşık 12-14 saat) bana %70'e yakın bir zaman tasarrufu sağladı ve enerjimi tamamen projenin mantıksal doğruluğuna vermeme imkan tanıdı.

## 7. Bu Projeyi Sürdürürseniz Bir Sonraki Adım Ne Olur?
VibeLog uygulamasını akademik bir ödev seviyesinden çıkartıp, gerçek anlamda üretim ortamına (production) hazır, ticari veya geniş ölçekli bir SaaS ürününe dönüştürmek istersem atacağım sonraki stratejik adımlar şunlar olacaktır:

* **Rol Tabanlı Yetkilendirme Sistemi (RBAC):** Projeye sadece bireysel kullanım değil, ekip çalışması desteği eklenecektir. Kullanıcılar "Manager", "Developer" ve "Tester" olarak rollere ayrılacak; hata biletini sadece Tester açabilecek, Developer durumunu güncelleyebilecek, Manager ise projeyi yönetebilecektir.
* **Asenkron Bildirim ve Entegrasyon Servisleri:** Bir hata bileti "Çözüldü" durumuna getirildiğinde veya kritik bir bug girildiğinde, projeye dahil olan tüm geliştiricilere anlık e-posta veya Slack/Discord webhook bildirimleri gönderen bir altyapı kurulacaktır. Bu işlemler ana uygulama akışını yavaşlatmaması için Celery ve Redis kullanılarak asenkron (arka plan görevi) hale getirilecektir.
* **Merkezi RESTful API Katmanı:** Diğer harici yazılımların veya masaüstü/mobil araçların VibeLog sistemine hata kaydı gönderebilmesi için Flask-RESTful kullanılarak güvenli, API anahtarı (API Key) korumalı bir `/api/v1/` endpoint mimarisi uygulamaya dahil edilecektir.
