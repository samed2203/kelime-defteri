import json
import os
from collections import OrderedDict

# Sabitler
KELIME_DOSYASI = 'kelime_veritabani.json'
RENKLER = {
    'baslik': '\033[1;32m',
    'secim': '\033[1;34m',
    'hata': '\033[1;31m',
    'bilgi': '\033[1;33m',
    'normal': '\033[0m'
}

kelimeler = OrderedDict()

def renkli_yazi(metin, renk):
    return f"{RENKLER[renk]}{metin}{RENKLER['normal']}"

def veri_kaydet():
    try:
        with open(KELIME_DOSYASI, 'w', encoding='utf-8') as f:
            json.dump(kelimeler, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(renkli_yazi(f"✗ Kayıt hatası: {e}", 'hata'))

def veri_yukle():
    global kelimeler
    try:
        with open(KELIME_DOSYASI, 'r', encoding='utf-8') as f:
            kelimeler = OrderedDict(json.load(f))
    except FileNotFoundError:
        kelimeler = OrderedDict()
    except Exception as e:
        print(renkli_yazi(f"✗ Yükleme hatası: {e}", 'hata'))

def temiz_ekran():
    os.system('cls' if os.name == 'nt' else 'clear')

def konu_ekle():
    temiz_ekran()
    print(renkli_yazi("\n〚 YENİ KONU EKLE 〛", 'baslik'))
    
    konu = input("\nKonu adı (ç: Çıkış): ").strip()
    if not konu or konu.lower() == 'ç':
        return None
        
    if konu in kelimeler:
        print(renkli_yazi("✗ Bu konu zaten var!", 'hata'))
        input("Devam için Enter...")
        return None
        
    kelimeler[konu] = []
    veri_kaydet()
    print(renkli_yazi(f"✓ '{konu}' eklendi!", 'bilgi'))
    return konu

def konu_sec():
    if not kelimeler:
        print(renkli_yazi("ℹ Henüz konu yok!", 'bilgi'))
        input("Devam için Enter...")
        return None

    temiz_ekran()
    print(renkli_yazi("\n〚 KONU SEÇ 〛", 'baslik'))
    
    for i, konu in enumerate(kelimeler.keys(), 1):
        print(f"{i}. {konu}")

    try:
        secim = input("\nSeçim (numara/ç): ")
        if secim.lower() == 'ç':
            return None
            
        secim = int(secim)
        if 1 <= secim <= len(kelimeler):
            return list(kelimeler.keys())[secim - 1]
        print(renkli_yazi("✗ Geçersiz numara!", 'hata'))
    except ValueError:
        print(renkli_yazi("✗ Sayı girin!", 'hata'))
    
    input("Devam için Enter...")
    return None

def konu_sil():
    if not kelimeler:
        print(renkli_yazi("ℹ Silinecek konu yok!", 'bilgi'))
        input("Devam için Enter...")
        return

    temiz_ekran()
    print(renkli_yazi("\n〚 KONU SİL 〛", 'baslik'))
    
    for i, konu in enumerate(kelimeler.keys(), 1):
        print(f"{i}. {konu}")

    try:
        secim = input("\nSilinecek numara (ç: Çıkış): ")
        if secim.lower() == 'ç':
            return
            
        secim = int(secim)
        if 1 <= secim <= len(kelimeler):
            silinecek = list(kelimeler.keys())[secim - 1]
            del kelimeler[silinecek]
            veri_kaydet()
            print(renkli_yazi(f"✓ '{silinecek}' silindi!", 'bilgi'))
        else:
            print(renkli_yazi("✗ Geçersiz numara!", 'hata'))
    except ValueError:
        print(renkli_yazi("✗ Sayı girin!", 'hata'))
    
    input("Devam için Enter...")

def kelime_islemleri(konu):
    while True:
        temiz_ekran()
        print(renkli_yazi(f"\n〚 {konu.upper()} 〛", 'baslik'))
        print("\n1. Kelime Ekle")
        print("2. Kelimeleri Göster")
        print("3. Kelime Düzenle")
        print("4. Geri Dön")
        
        secim = input("\nSeçiminiz (1-4): ")
        
        if secim == '1':
            # Kelime Ekleme Fonksiyonu
            temiz_ekran()
            print(renkli_yazi(f"\n〚 {konu.upper()} - KELİME EKLE 〛", 'baslik'))
            kelime = input("\nKelime girin (ç: Çıkış): ").strip()
            
            if kelime.lower() == 'ç':
                continue
                
            if kelime:
                kelimeler[konu].append(kelime)
                veri_kaydet()
                print(renkli_yazi(f"✓ '{kelime}' eklendi!", 'bilgi'))
            else:
                print(renkli_yazi("✗ Boş kelime giremezsiniz!", 'hata'))
            input("Devam için Enter...")
            
        elif secim == '2':
            # Kelime Listeleme Fonksiyonu
            temiz_ekran()
            print(renkli_yazi(f"\n〚 {konu.upper()} - KELİMELER 〛", 'baslik'))
            
            if not kelimeler[konu]:
                print(renkli_yazi("ℹ Henüz kelime eklenmedi!", 'bilgi'))
            else:
                for i, kelime in enumerate(kelimeler[konu], 1):
                    print(f"{i}. {kelime}")
            input("\nDevam için Enter...")
            
        elif secim == '3':
            # Kelime Düzenleme Fonksiyonu
            if not kelimeler[konu]:
                print(renkli_yazi("ℹ Düzenlenecek kelime yok!", 'bilgi'))
                input("Devam için Enter...")
                continue
                
            temiz_ekran()
            print(renkli_yazi(f"\n〚 {konu.upper()} - KELİME DÜZENLE 〛", 'baslik'))
            
            for i, kelime in enumerate(kelimeler[konu], 1):
                print(f"{i}. {kelime}")
                
            try:
                sec = input("\nDüzenlenecek numara (ç: Çıkış): ")
                if sec.lower() == 'ç':
                    continue
                    
                index = int(sec) - 1
                if 0 <= index < len(kelimeler[konu]):
                    yeni = input(f"Yeni değer ({kelimeler[konu][index]}): ").strip()
                    if yeni:
                        kelimeler[konu][index] = yeni
                        veri_kaydet()
                        print(renkli_yazi("✓ Güncellendi!", 'bilgi'))
                else:
                    print(renkli_yazi("✗ Geçersiz numara!", 'hata'))
            except ValueError:
                print(renkli_yazi("✗ Sayı girin!", 'hata'))
            input("Devam için Enter...")
            
        elif secim == '4':
            break
            
        else:
            print(renkli_yazi("✗ Geçersiz seçim!", 'hata'))
            input("Devam için Enter...")
def ana_menu():
    veri_yukle()
    
    while True:
        temiz_ekran()
        print(renkli_yazi("\n〚 ANA MENÜ 〛", 'baslik'))
        print("\n1. Konu Seç")
        print("2. Konu Sil")
        print("3. Konu Ekle")
        print("4. Çıkış")
        
        secim = input("\nSeçiminiz (1-4): ")
        
        if secim == '1':
            konu = konu_sec()
            if konu:
                kelime_islemleri(konu)
        elif secim == '2':
            konu_sil()
        elif secim == '3':
            konu = konu_ekle()
            if konu:
                kelime_islemleri(konu)
        elif secim == '4':
            print(renkli_yazi("\nÇıkılıyor...", 'bilgi'))
            break
        else:
            print(renkli_yazi("✗ Geçersiz seçim! Lütfen 1-4 arası rakam girin.", 'hata'))
            input("Devam için Enter...")

if __name__ == "__main__":
    ana_menu()