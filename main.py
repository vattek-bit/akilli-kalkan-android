from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import numpy as np
import base64
import math

# --------------------------------------------------
# TAM SINIF LİSTESİ (30 KİŞİ)
# --------------------------------------------------

SINIF_LISTESI = [
    "ELİF SENA ALGIN", "ZELİHA BÜYÜKDOĞAN", "ÜMRAN LALEK", "EFE SAÇMALI",
    "YASİN ERDOĞAN", "MUSTAFA EFE BAYSAL", "NASIF EMRE GÖZÜKÜÇÜK",
    "ALTAN ÖZTÜRK", "ZEYNEP BEREKETLİ", "ONUR KAAN ÖZYURT",
    "ECE SU KAYA", "EGEHAN KUDDAR", "ELA YILDIRIM", "ELİSA BAL",
    "FADİME HİRANUR AYKÜL", "HATİCE KARAKAŞ", "HAVVA SİZGEN",
    "MAHMUD SAMİ SIÇRAMAZ", "İSA ALPEREN DURUKAN", "BAYRAM DEMİRKESER",
    "MELİSANUR TELEK", "MİNE DURU UZUN", "MİRAÇ CAN TARAÇ",
    "MUHAMMED ALİ KILINÇ", "FEDYE ÖMERİ", "ŞADİYE GÜL KUŞDEMİR",
    "TUANA SUNA YALÇIN", "YAĞMUR ÇETİN", "YAHYA NEBİ ERDOĞAN",
    "ZELİHA ŞİFA KILIÇ"
]

# --------------------------------------------------
# KARAKTER HARİTASI (ISO-8859-9 UYUMLU)
# --------------------------------------------------

KARAKTER_HARITASI = {
    'Ç':199,'Ğ':208,'İ':221,'Ö':214,'Ş':222,'Ü':220,
    'ç':231,'ğ':240,'ı':253,'ö':246,'ş':254,'ü':252
}

MATRIS_SABITLERI = [1, 2, 4, 3]

# --------------------------------------------------
# ALGORİTMA FONKSİYONLARI
# --------------------------------------------------

def get_ascii(c):
    return KARAKTER_HARITASI.get(c, ord(c))

def anahtar_uret(isim):
    isim = isim.split()[0]
    toplam = 0
    for i, h in enumerate(isim):
        toplam += get_ascii(h) * (i + 1)
    return toplam % 256

def xor_islemi(veri, anahtar):
    return [v ^ anahtar for v in veri]

def matris_olustur(tuz):
    hucreler = [(s + tuz) % 10 for s in MATRIS_SABITLERI]
    return np.array(hucreler).reshape(2, 2)

def matris_sifrele(veri, matris):
    if len(veri) % 2 != 0:
        veri.append(0)
    sonuc = []
    for i in range(0, len(veri), 2):
        v = np.array([[veri[i]], [veri[i+1]]])
        r = np.dot(matris, v) % 256
        sonuc.extend([int(r[0][0]), int(r[1][0])])
    return sonuc

def bit_sola(veri, n=2):
    return [((v << n) | (v >> (8 - n))) & 0xFF for v in veri]

def bit_saga(veri, n=2):
    return [((v >> n) | (v << (8 - n))) & 0xFF for v in veri]

def ters_matris(matris):
    det = int(round(np.linalg.det(matris)))
    if math.gcd(det, 256) != 1:
        return None
    inv = pow(det, -1, 256)
    a, b = matris[0]
    c, d = matris[1]
    adj = np.array([[d, -b], [-c, a]])
    return (inv * adj) % 256

def sifrele(mesaj, ogrenci):
    anahtar = anahtar_uret(ogrenci)
    veri = [get_ascii(c) for c in mesaj]
    x = xor_islemi(veri, anahtar)
    m = matris_olustur(anahtar)
    y = matris_sifrele(x, m)
    z = bit_sola(y)
    return base64.b64encode(bytes(z)).decode()

def coz(b64, ogrenci):
    anahtar = anahtar_uret(ogrenci)
    veri = list(base64.b64decode(b64))
    x = bit_saga(veri)
    m = matris_olustur(anahtar)
    tm = ters_matris(m)
    if tm is None:
        return "Hatalı anahtar"
    y = []
    for i in range(0, len(x), 2):
        v = np.array([[x[i]], [x[i+1]]])
        r = np.dot(tm, v) % 256
        y.extend([int(r[0][0]), int(r[1][0])])
    z = xor_islemi(y, anahtar)
    return "".join(chr(v) for v in z if v != 0)

# --------------------------------------------------
# KIVY ARAYÜZ
# --------------------------------------------------

class AkilliKalkanUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10)

        self.spinner = Spinner(
            text="Öğrenci Seç",
            values=SINIF_LISTESI,
            size_hint=(1, None),
            height=50
        )
        self.add_widget(self.spinner)

        self.mesaj = TextInput(
            hint_text="Mesaj veya Şifreli Metin",
            multiline=True,
            size_hint=(1, 0.4)
        )
        self.add_widget(self.mesaj)

        btn_sifrele = Button(text="ŞİFRELE")
        btn_sifrele.bind(on_press=self.sifrele)
        self.add_widget(btn_sifrele)

        btn_coz = Button(text="ÇÖZ")
        btn_coz.bind(on_press=self.coz)
        self.add_widget(btn_coz)

        self.sonuc = TextInput(
            hint_text="Sonuç",
            readonly=True,
            size_hint=(1, 0.4)
        )
        self.add_widget(self.sonuc)

    def sifrele(self, instance):
        self.sonuc.text = sifrele(self.mesaj.text, self.spinner.text)

    def coz(self, instance):
        self.sonuc.text = coz(self.mesaj.text, self.spinner.text)

class AkilliKalkanApp(App):
    def build(self):
        return AkilliKalkanUI()

AkilliKalkanApp().run()
