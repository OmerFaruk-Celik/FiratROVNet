📘 Fırat-GNC: Otonom Sualtı Sürü Sistemi

Fırat Üniversitesi - Otonom Sistemler & Yapay Zeka Laboratuvarı bünyesinde geliştirilmiştir.

Bu proje, çoklu Sualtı Otonom Araçları (ROV/AUV) ve Su Üstü Araçları (ASV) için Yapay Zeka Destekli (GAT), Fizik Tabanlı ve İletişim Kısıtlı bir sürü simülasyon ortamıdır.
🌟 Özellikler

    🤖 Dağıtık Yapay Zeka (GAT): Her ROV, Graf Dikkat Ağları (Graph Attention Networks) kullanarak komşularından gelen verileri işler ve tehlikeleri (Engel, Çarpışma, Kopma) tespit eder.

    📡 Gerçekçi Akustik İletişim: Sualtı modem simülasyonu ile gecikme (delay), paket kaybı (packet loss) ve gürültü (noise) modellenmiştir.

    ⚓ Fizik Motoru: Ursina motoru üzerinde sürtünme, kaldırma kuvveti (buoyancy) ve motor itki dinamikleri simüle edilir.

    🎮 Canlı Konsol (Human-in-the-Loop): Simülasyon çalışırken terminal üzerinden Python kodlarıyla anlık müdahale, görev atama ve parametre değişimi yapılabilir.

    🧠 Otonom Navigasyon (GNC): Hedef noktasına giderken engellerden kaçınan ve sürü formasyonunu koruyan otopilot sistemi.

📂 Dosya Yapısı
code Text

    
StarProjesi/
│
├── main.py                  # Ana Çalıştırıcı (Simülasyonu başlatır)
├── rov_modeli_multi.pth     # Eğitilmiş Yapay Zeka Modeli (Dosya yoksa eğitimle oluşturulur)
│
└── FiratROVNet/             # Çekirdek Kütüphane
    ├── __init__.py          # Paket yöneticisi
    ├── gat.py               # GAT Modeli ve Eğitim Fonksiyonları
    ├── ortam.py             # Veri Seti ve Senaryo Üreticisi
    ├── simulasyon.py        # 3D Render ve Fizik Motoru
    ├── iletisim.py          # Akustik Modem Simülatörü
    ├── gnc.py               # Güdüm, Navigasyon ve Kontrol Algoritmaları
    └── config.py            # Canlı Ayar Yönetimi

  

🛠️ Kurulum

Gerekli Python kütüphanelerini yükleyin:
code Bash

    
pip install torch torch_geometric ursina numpy networkx

  

🧠 Yapay Zeka Eğitimi

Sistemi ilk kez çalıştırmadan önce veya modeli güncellemek için eğitim yapılması gerekir.

    Terminali açın ve python yazarak interaktif moda girin.

    Aşağıdaki komutları çalıştırın:

code Python

    
from FiratROVNet import gat, ortam

# 1. Eski hafızayı temizle (Sıfırdan eğitim için)
gat.reset()

# 2. Eğitimi Başlat (Dinamik Veri ile 10.000 Epoch)
# Bu işlem 'rov_modeli_multi.pth' dosyasını oluşturur.
gat.Train(veri_kaynagi=lambda: ortam.veri_uret(n_rovs=None), epochs=10000)

  

🚀 Çalıştırma

Simülasyonu başlatmak için terminalden şu komutu kullanın (Linux kullanıcıları için grafik uyumluluk modu):
code Bash

    
LIBGL_ALWAYS_SOFTWARE=1 python main.py

  

Windows kullanıcıları direkt python main.py yazabilir.
💻 Canlı Konsol Komutları

Simülasyon başladığında terminal donmaz. Arka planda çalışan Python kabuğu (>>>) üzerinden sistemi yönetebilirsiniz.
1. Otonom Görev Atama (git)

ROV'lara hedef koordinat verir. GNC (Otopilot) devreye girer ve engellerden kaçarak hedefe gider.

Kullanım: git(rov_id, x, z, y, ai)

    x, z: Yatay düzlem koordinatları.

    y: Derinlik (Negatif değer su altıdır).

    ai: True (Zeki Mod) / False (Kör Mod).

Örnekler:
code Python

    
>>> git(1, 50, 50, -5)           # ROV 1'i (50, 50) noktasına, 5m derine gönder.
>>> git(2, -20, 100, -10, ai=False) # ROV 2'yi kör modda gönder (Çarpışma Testi).

  

Toplu Formasyon Emri:
code Python

    
>>> for i in range(4): git(i, i*10, 100, -5) # Tüm filoyu ileri sür.

  

2. Sistem Ayarları (cfg)

Logları canlı olarak açıp kapatır.
code Python

    
>>> cfg.goster_modem = True  # ROV'lar arası mesajlaşmayı göster.
>>> cfg.goster_gnc = True    # Navigasyon rotalarını göster.
>>> cfg.ai_aktif = False     # Tüm filonun yapay zekasını kapat (A/B Testi için).

  

3. Manuel Müdahale (rovs)

Otopilotu ezip fiziksel müdahale yapmak için kullanılır.
code Python

    
# ROV 0'ı manuel olarak ileri it
>>> rovs[0].move("ileri", 100) 

# ROV 1'in sonar menzilini 50 metreye çıkar
>>> rovs[1].set("engel_mesafesi", 50.0)

# ROV 2'yi Yeşil renge boya
>>> from ursina import color
>>> rovs[2].color = color.green

  

🌈 Renk Kodları ve Durumlar

Simülasyonda ROV'ların renkleri, GAT modelinin o anki durum analizine göre değişir:
Renk	Durum	Açıklama
🔴 KIRMIZI	Lider / Engel	Lider araçtır veya Engel tespit edilmiştir.
🟠 TURUNCU	Güvenli	Takipçi ROV normal seyir halinde.
⚫ SİYAH	Çarpışma	Başka bir ROV ile çarpışmak üzere (Acil Dur).
🟡 SARI	Kopuk	İletişim menzili dışına çıktı.
🟣 MOR	Uzak	Liderden çok uzaklaştı (Turbo mod).
🛑 Çıkış

Simülasyonu ve terminali güvenli bir şekilde kapatmak için simülasyon penceresi aktifken:

    ESC veya Q tuşuna basın.

Geliştirici: Ömer Faruk Çelik
Lisans: MIT
