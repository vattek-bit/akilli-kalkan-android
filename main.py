# @title Akıllı Kalkan: Hibrit Şifreleme Simülasyonu
# @markdown Bu kod, TÜBİTAK 2204-B projesi kapsamında geliştirilen "Akıllı Kalkan" algoritmasını simüle eder.

import numpy as np
import base64
import math

# --- 1. SABİTLER VE VERİ YAPILARI ---

# Raporunuzdaki Tablo 2'den alınan Sınıf Listesi
SINIF_LISTESI = [
    "ELİF SENA ALGIN", "ZELİHA BÜYÜKDOĞAN", "ÜMRAN LALEK", "EFE SAÇMALI",
    "YASİN ERDOĞAN", "MUSTAFA EFE BAYSAL", "NASIF EMRE GÖZÜKÜÇÜK", "ALTAN ÖZTÜRK",
    "ZEYNEP BEREKETLİ", "ONUR KAAN ÖZYURT", "ECE SU KAYA", "EGEHAN KUDDAR",
    "ELA YILDIRIM", "ELİSA BAL", "FADİME HİRANUR AYKÜL", "HATİCE KARAKAŞ",
    "HAVVA SİZGEN", "MAHMUD SAMİ SIÇRAMAZ", "İSA ALPEREN DURUKAN", "BAYRAM DEMİRKESER",
    "MELİSANUR TELEK", "MİNE DURU UZUN", "MİRAÇ CAN TARAÇ", "MUHAMMED ALİ KILINÇ",
    "FEDYE ÖMERİ", "ŞADİYE GÜL KUŞDEMİR", "TUANA SUNA YALÇIN", "YAĞMUR ÇETİN",
    "YAHYA NEBİ ERDOĞAN", "ZELİHA ŞİFA KILIÇ"
]

# Raporunuzdaki Tablo 3'e göre Özel Türkçe Karakter Haritası (ISO-8859-9 Standardı)
# Python varsayılan Unicode kullandığı için bu haritalama, raporunuzdaki matematiksel hesapların
# (ELİSA -> 5 gibi) birebir tutması için zorunludur.
KARAKTER_HARITASI = {
    'Ç': 199, 'Ğ': 208, 'İ': 221, 'Ö': 214, 'Ş': 222, 'Ü': 220,
    'ç': 231, 'ğ': 240, 'ı': 253, 'ö': 246, 'ş': 254, 'ü': 252
}

# Raporunuzdaki Matris Sabitleri: [3, 2, 5, 4]
# Yeni önerilen Matris Sabitleri: [1, 2, 4, 3] veya [5, 2, 4, 7] gibi [tek, çift, çift, tek] paritesinde olmalı
MATRIS_SABITLERI = [1, 2, 4, 3] # Örnek olarak değiştirildi

# --- 2. YARDIMCI FONKSİYONLAR ---

def get_ascii(char):
    """Karakterin rapordaki tabloya uygun ASCII değerini döndürür."""
    return KARAKTER_HARITASI.get(char, ord(char))

def anahtar_uret(isim):
    """
    Raporun Katman 1: Sınıf Listesi Tabanlı Anahtar Üretimi
    Formül: Toplam(Karakter * Konum) mod 256
    """
    # Sadece ismi alalım (Soyadı ayırıyoruz, raporda ELİSA örneği kullanılmış)
    sadece_isim = isim.split()[0]

    toplam = 0
    print(f"\n--- Anahtar Üretim Detayları ({sadece_isim}) ---")
    print(f"{'Karakter':<10} {'ASCII':<10} {'Konum':<10} {'Çarpım'}")
    print("-" * 40)

    for i, harf in enumerate(sadece_isim):
        ascii_val = get_ascii(harf)
        konum = i + 1
        carpim = ascii_val * konum
        toplam += carpim
        print(f"{harf:<10} {ascii_val:<10} {konum:<10} {carpim}")

    anahtar = toplam % 256
    print("-" * 40)
    print(f"Toplam Değer: {toplam}")
    print(f"Mod 256 Sonucu (Kullanıcı Tuzu): {anahtar}")
    return anahtar

def xor_islemi(veri_listesi, anahtar):
    """
    Raporun Katman 2: XOR Mantık İşlemi
    """
    sonuc = []
    print(f"\n--- XOR İşlemi (Anahtar: {anahtar}) ---")
    # Debug için ilk 5 karakteri göster
    for i, val in enumerate(veri_listesi):
        yeni_val = val ^ anahtar
        sonuc.append(yeni_val)
        if i < 3: # Sadece baştaki birkaç örneği gösterelim ekran dolmasın
            print(f"Veri: {val} (Bin: {val:08b}) XOR Anahtar -> {yeni_val} (Bin: {yeni_val:08b})")
    return sonuc

def matris_olustur(anahtar_tuzu):
    """
    Raporun Katman 3: Hibrit Matrisin Oluşturulması
    Formül: Hücre = (Sistem Sabiti + Tuz) mod 10
    """
    hucreler = []
    print("\n--- Anahtar Matrisi Oluşturuluyor ---")
    print(f"Sistem Sabitleri: {MATRIS_SABITLERI}")
    print(f"Kullanıcı Tuzu: {anahtar_tuzu}")

    for sabit in MATRIS_SABITLERI:
        deger = (sabit + anahtar_tuzu) % 10
        hucreler.append(deger)

    matris = np.array(hucreler).reshape(2, 2)
    determinant = int(round(np.linalg.det(matris)))

    print(f"Oluşan Matris:\n{matris}")
    print(f"Determinant: {determinant}")

    return matris, determinant

def matris_sifrele(veri_listesi, matris):
    """
    Matris ile şifreleme (Encryption)
    """
    # Dolgu (Padding) kontrolü: Çift sayı olmalı
    if len(veri_listesi) % 2 != 0:
        veri_listesi.append(0) # Padding

    sifreli_veri = []
    # Veriyi 2'li gruplara ayırıp matrisle çarp
    for i in range(0, len(veri_listesi), 2):
        vektor = np.array([[veri_listesi[i]], [veri_listesi[i+1]]])
        # Matris Çarpımı: [2x2] * [2x1]
        carpim = np.dot(matris, vektor)
        # Mod 256
        modlu_sonuc = carpim % 256
        sifreli_veri.extend([modlu_sonuc[0][0], modlu_sonuc[1][0]])

    return sifreli_veri

def ters_matris_moduler(matris, mod=256):
    """
    Şifre çözme için matrisin modüler tersini alır.
    Bu matematiksel bir işlemdir: A^(-1) = det^(-1) * Adj(A) mod M
    """
    det = int(round(np.linalg.det(matris)))

    # Determinantın modüler tersini bul (Eğer aralarında asal değilse hata verir)
    try:
        det_inv = pow(det, -1, mod)
    except ValueError:
        return None # Tersi alınamaz

    # Ek Matris (Adjugate)
    # [a b]  ->  [d -b]
    # [c d]      [-c a]
    a, b = matris[0,0], matris[0,1]
    c, d = matris[1,0], matris[1,1]

    adj = np.array([[d, -b], [-c, a]])

    # Ters Matris = det_inv * adj % mod
    ters_matris = (det_inv * adj) % mod
    return ters_matris

def matris_coz(sifreli_veri, matris):
    """
    Matris ile şifre çözme (Decryption)
    """
    ters_matris = ters_matris_moduler(matris)
    if ters_matris is None:
        return None

    cozulmus_veri = []
    for i in range(0, len(sifreli_veri), 2):
        vektor = np.array([[sifreli_veri[i]], [sifreli_veri[i+1]]])
        carpim = np.dot(ters_matris, vektor)
        modlu_sonuc = carpim % 256
        cozulmus_veri.extend([int(modlu_sonuc[0][0]), int(modlu_sonuc[1][0])])

    return cozulmus_veri

def bit_kaydir_sola(veri_listesi, n=2):
    """Raporun Katman 4: Döngüsel Bit Kaydırma (Sola)"""
    sonuc = []
    for val in veri_listesi:
        # 8 bitlik döngüsel kaydırma
        # ((x << n) | (x >> (8 - n))) & 0xFF formülü
        yeni_val = ((val << n) | (val >> (8 - n))) & 0xFF
        sonuc.append(yeni_val)
    return sonuc

def bit_kaydir_saga(veri_listesi, n=2):
    """Şifre Çözme için: Döngüsel Bit Kaydırma (Sağa - Tersi)"""
    sonuc = []
    for val in veri_listesi:
        yeni_val = ((val >> n) | (val << (8 - n))) & 0xFF
        sonuc.append(yeni_val)
    return sonuc

# --- 3. ANA PROGRAM (MENÜ) ---

global_anahtar = None
global_matris = None
global_sifreli_veri = None # Base64 string değil, ham liste
global_sifreli_b64 = None

def main_menu():
    global global_anahtar, global_matris, global_sifreli_veri, global_sifreli_b64

    while True:
        print("\n" + "="*40)
        print("    AKILLI KALKAN - ANA MENÜ")
        print("="*40)
        print("1. SINIF LİSTESİNİ YÜKLE VE ANAHTAR ÜRET")
        print("2. ŞİFRELENECEK MESAJI GİR")
        print("3. ŞİFRE ÇÖZME (DECRYPTION)")
        print("4. ÇIKIŞ")
        print("-" * 40)

        secim = input("Seçiminiz (1-4): ")

        if secim == '1':
            print("\n--- Sınıf Listesi ---")
            for i, isim in enumerate(SINIF_LISTESI):
                print(f"{i+1}. {isim}")

            try:
                ogr_no = int(input("\nBir öğrenci numarası seçin (1-30): ")) - 1
                if 0 <= ogr_no < len(SINIF_LISTESI):
                    secilen_isim = SINIF_LISTESI[ogr_no]
                    print(f"\nSeçilen Öğrenci: {secilen_isim}")
                    global_anahtar = anahtar_uret(secilen_isim)

                    # Matris Kontrolü Burada Yapılıyor
                    global_matris, det = matris_olustur(global_anahtar)

                    # Determinant 0 veya mod 256 ile aralarında asal değilse (Tersi alınamazsa)
                    if det == 0 or math.gcd(det, 256) != 1:
                        print(f"\n[UYARI] Determinant: {det}. Bu matrisin modüler tersi alınamaz!")
                        print("Lütfen Başka Bir Öğrenci Seçiniz.")
                        global_anahtar = None # Sıfırla
                    else:
                        print("\n[BAŞARILI] Anahtar ve Matris şifreleme için uygun.")

                else:
                    print("Geçersiz numara.")
            except ValueError:
                print("Lütfen sayı giriniz.")

        elif secim == '2':
            if global_anahtar is None:
                print("\n[HATA] Önce 1. adımdan bir öğrenci seçip anahtar üretmelisiniz!")
                continue

            mesaj = input("\nŞifrelenecek Mesajı Girin: ")

            # 1. Adım: Metin -> ASCII Listesi
            veri = [get_ascii(c) for c in mesaj]
            print(f"\n[1] ASCII Veri: {veri}")

            # 2. Adım: XOR
            xor_veri = xor_islemi(veri, global_anahtar)
            print(f"[2] XOR Sonrası: {xor_veri}")

            # 3. Adım: Hibrit Matris
            matris_veri = matris_sifrele(xor_veri, global_matris)
            print(f"[3] Matris Çarpımı Sonrası: {matris_veri}")

            # 4. Adım: Bit Kaydırma
            kaydirilmis_veri = bit_kaydir_sola(matris_veri)
            print(f"[4] Bit Kaydırma Sonrası: {kaydirilmis_veri}")

            # 5. Adım: Base64 Çıktı
            # Byte dizisine çevir
            byte_data = bytes(kaydirilmis_veri)
            global_sifreli_b64 = base64.b64encode(byte_data).decode('utf-8')
            global_sifreli_veri = kaydirilmis_veri # Şifre çözme testi için sakla

            print(f"\n>>> ŞİFRELENMİŞ MESAJ (Base64): {global_sifreli_b64}")

        elif secim == '3':
            print("\n--- ŞİFRE ÇÖZME MENÜSÜ ---")
            if global_sifreli_veri is None:
                print("[BİLGİ] Hafızada şifreli mesaj yok. Önce şifreleme yapın veya manuel giriş yapın.")
                # İsterseniz buraya manuel base64 giriş kodu eklenebilir
                continue

            print(f"Şifreli Veri (Liste): {global_sifreli_veri}")
            print("Tersine Mühendislik Başlatılıyor...")

            # 1. Ters Bit Kaydırma (Sağa)
            ters_bit = bit_kaydir_saga(global_sifreli_veri)
            print(f"[1] Ters Bit Kaydırma: {ters_bit}")

            # 2. Ters Matris İşlemi
            ters_matris_sonuc = matris_coz(ters_bit, global_matris)
            if ters_matris_sonuc is None:
                print("[HATA] Matrisin tersi alınamadı!")
                continue

            # Padding (Dolgu) 0 varsa temizle (Sadece sondaysa ve mesaj tek sayı idiyse)
            # Basitlik adına burada son eleman 0 ise ve orijinali tekse diye kontrol etmiyoruz,
            # Genelde string çevirince null char etkilemez veya strip edilebilir.
            print(f"[2] Ters Matris Sonucu: {ters_matris_sonuc}")

            # 3. Ters XOR (XOR'un tersi yine XOR'dur)
            cozulen_ascii = xor_islemi(ters_matris_sonuc, global_anahtar)
            print(f"[3] Ters XOR Sonucu: {cozulen_ascii}")

            # 4. ASCII -> Metin
            # Paddingden gelen 0'ı (Null char) temizle
            cozulen_metin = ""
            for val in cozulen_ascii:
                if val != 0:
                    # Türkçe karakter desteği için chr() bazen yetmez, harita gerekebilir ama 
                    # genelde Python chr() unicode uyumludur. ISO-8859-9 tersine bakalım.
                    # Basitlik için chr kullanıyoruz, Türkçe karakterler unicode olduğu için tutmayabilir.
                    # Bu yüzden ters harita yapmak en doğrusu:
                    found = False
                    for k, v in KARAKTER_HARITASI.items():
                        if v == val:
                            cozulen_metin += k
                            found = True
                            break
                    if not found:
                        cozulen_metin += chr(val)

            print(f"\n>>> ÇÖZÜLEN ORİJİNAL MESAJ: {cozulen_metin}")

        elif secim == '4':
            print("Çıkış yapılıyor. Başarılar!")
            break

# Programı Başlat
if __name__ == "__main__":
    main_menu()

