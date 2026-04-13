# Okuldayız Backend

Bu proje, "Okuldayız" platformunun backend (API) servisidir. Django ve Django REST Framework kullanılarak geliştirilmiş olup, Docker ve Docker Compose ile kolayca kurulup çalıştırılabilecek şekilde tasarlanmıştır.

## Özellikler

*   **RESTful API:** Django REST Framework ile modern ve hızlı API.
*   **Kimlik Doğrulama:** JWT (JSON Web Token) tabanlı güvenli kimlik doğrulama.
*   **Redis ve Throttling:** Rate limiting (Hız sınırlaması) ve önbellekleme (cache) için Redis entegrasyonu.
*   **Modüler Yapı:** `accounts`, `core`, `schools`, `leads`, `favorites`, `comments` gibi modüler Django uygulamaları.
*   **Kapsayıcı Mimari (Docker):** Uygulama, MySQL veritabanı ve Redis servisleri Docker Compose ile kullanıma hazırdır.

## Gereksinimler

Proje geliştirmek veya çalıştırmak için sisteminizde aşağıdaki yazılımların kurulu olması önerilir:
*   [Docker ve Docker Compose](https://www.docker.com/) (Önerilen)
*   [Python 3.14+](https://www.python.org/) (Sadece lokal geliştirme için)

## Kurulum ve Çalıştırma (Docker ile Önerilen)

Projeyi en hızlı ve hatasız şekilde çalıştırmak için Docker Compose kullanabilirsiniz. MySQL ve Redis servisleri otomatik olarak ayağa kalkacaktır.

1.  **Repository'yi Klonlayın:**
    ```bash
    git clone <repo-url>
    cd okuldayiz-backend
    ```

2.  **Çevresel Değişkenleri (Environment Variables) Ayarlayın:**
    Projeyi çalıştırmadan önce güvenlik sebebiyle ayarlar `.env` dosyası üzerinden okunmaktadır.
    
    `okulproj` dizini altındaki örnek ayar dosyasını kopyalayın:
    ```bash
    cp okulproj/.env.example okulproj/.env
    ```
    Oluşturulan `okulproj/.env` dosyasının içeriğindeki veritabanı şifrelerini, `SECRET_KEY` değerini ve diğer ayarları kendi tercihlerinize göre güncelleyebilirsiniz. (Varsayılan değerlerle de çalışacaktır).

3.  **Docker Compose ile Servisleri Başlatın:**
    Ana dizindeki `docker-compose.yml` dosyasını kullanarak konteynerleri oluşturun ve başlatın. Docker'ın çevresel değişkenleri doğru görmesi için `--env-file` parametresini kullanmayı unutmayın:
    ```bash
    docker-compose --env-file okulproj/.env up -d --build
    ```
    Bu komut MySQL, Redis ve Django web sunucusunu arka planda ayağa kaldıracaktır. İlk kurulumda veritabanı tabloları otomatik oluşturulacaktır (migration komutları container içerisinde çalışır).

4.  **Uygulamaya Göz Atın:**
    Sunucu ayağa kalktıktan sonra API'ye aşağıdaki adresten ulaşabilirsiniz:
    [http://localhost:8000](http://localhost:8000)

## Kurulum ve Çalıştırma (Lokal Geliştirme - Docker Hariç)

Eğer projeyi kendi Python ortamınızda, lokal bir MySQL ve Redis sunucusu ile çalıştırmak isterseniz:

1. Gereksinimleri yükleyin:
    ```bash
    cd okulproj
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux için (Windows için: .venv\Scripts\activate)
    pip install -r requirements.txt
    ```

2. `.env` dosyasını oluşturun ve sisteminizde kurulu olan lokal MySQL ve Redis sunucunuzun bağlantı bilgilerini dosyaya işleyin:
    ```bash
    cp .env.example .env
    ```

3. Veritabanı tablolarını oluşturun:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Sunucuyu başlatın:
    ```bash
    python manage.py runserver
    ```

## Güvenlik ve Gizlilik (Github Öncesi Dikkat Edilenler)
*   **Gizli Anahtarlar:** Gerçek `SECRET_KEY`, `DB_PASSWORD` gibi veri tabanı ve güvenlik bilgileri kaynak kodda hardcoded (sabit) olarak yer almaz. Bunun yerine güvende tutulması gereken detaylar `.env` dosyasına alınmıştır.
*   `.gitignore` dosyası güncellenerek lokal veritabanı (`db.sqlite3`), çevresel değişkenler dosyası (`.env`) ve diğer cache/IDE dosyaları git takibinden çıkarılmıştır.
*   Böylelikle proje güvenle Github gibi açık kaynak platformlarına aktarılabilir durumdadır.
