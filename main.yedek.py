from FiratROVNet.simulasyon import Ortam
from FiratROVNet.iletisim import AkustikModem
from FiratROVNet.gnc import GNCKomutan, LiderGNC, TakipciGNC
from FiratROVNet.gat import FiratAnalizci
from FiratROVNet.config import cfg
from ursina import *
import numpy as np
import random
import sys
import os

# 1. KURULUM
print("🔵 Fırat-GNC Sistemi Başlatılıyor...")
app = Ortam()
app.sim_olustur(n_rovs=4, n_engels=15)

try: beyin = FiratAnalizci(model_yolu="rov_modeli_multi.pth")
except: print("⚠️ Model yüklenemedi."); beyin = None

komutan = GNCKomutan()
tum_modemler = {}
lider_modem = AkustikModem(rov_id=0, gurultu_orani=0.05)
tum_modemler[0] = lider_modem

for i, rov in enumerate(app.rovs):
    rov.set("engel_mesafesi", 5.0)
    if i == 0:
        rov.set("rol", 1); rov.modem = lider_modem
        gnc = LiderGNC(rov, lider_modem)
        komutan.ekle(gnc); komutan.git(0, 40, 60, 0)
    else:
        rov.set("rol", 0)
        modem = AkustikModem(rov_id=i, gurultu_orani=0.1)
        rov.modem = modem; tum_modemler[i] = modem
        gnc = TakipciGNC(rov, modem, lider_modem_ref=lider_modem)
        komutan.ekle(gnc); komutan.git(i, 30 + (i*5), 50, -10)

komutan.rehber_dagit(tum_modemler)
app.konsola_ekle("git", komutan.git)
app.konsola_ekle("gnc", komutan.sistemler)
print("✅ Sistem aktif.")

# 2. ANA DÖNGÜ (SADELEŞTİRİLMİŞ)
def update():
    try:
        # --- TEK SATIRDA VERİ ALMA ---
        veri = app.get_gat_data()
        
        # AI Kararı
        ai_aktif = getattr(cfg, 'ai_aktif', True)
        if ai_aktif and beyin:
            try: tahminler, _, _ = beyin.analiz_et(veri)
            except: tahminler = np.zeros(len(app.rovs), dtype=int)
        else:
            tahminler = np.zeros(len(app.rovs), dtype=int)

        # Görselleştirme
        kod_renkleri = {0:color.orange, 1:color.red, 2:color.black, 3:color.yellow, 5:color.magenta}
        durum_txts = ["OK", "ENGEL", "CARPISMA", "KOPUK", "-", "UZAK"]
        
        for i, gat_kodu in enumerate(tahminler):
            if app.rovs[i].role == 1: app.rovs[i].color = color.red
            else: app.rovs[i].color = kod_renkleri.get(gat_kodu, color.white)
            
            ek = "" if ai_aktif else "\n[AI OFF]"
            app.rovs[i].label.text = f"R{i}\n{durum_txts[gat_kodu]}{ek}"
            
        komutan.guncelle_hepsi(tahminler)
        
    except Exception as e: pass

def input(key):
    if key == 'escape' or key == 'q':
        os.system('stty sane'); application.quit(); os._exit(0)

app.set_update_function(update)
app.app.input = input

if __name__ == "__main__":
    try: app.run(interaktif=True)
    except KeyboardInterrupt: pass
    finally: os.system('stty sane'); os._exit(0)
