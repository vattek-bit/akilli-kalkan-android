from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import base64
import numpy as np

SINIF_LISTESI = [
    "ELIF SENA ALGIN","ZELIHA BUYUKDOGAN","UMRAN LALEK","EFE SACMALI",
    "YASIN ERDOGAN","MUSTAFA EFE BAYSAL","NASIF EMRE GOZUKUCUK","ALTAN OZTURK",
    "ZEYNEP BEREKETLI","ONUR KAAN OZYURT","ECE SU KAYA","EGEHAN KUDDAR",
    "ELA YILDIRIM","ELISA BAL","FADIME HIRANUR AYKUL","HATICE KARAKAS",
    "HAVVA SIZGEN","MAHMUD SAMI SICRAMAZ","ISA ALPEREN DURUKAN","BAYRAM DEMIRKESER",
    "MELISANUR TELEK","MINE DURU UZUN","MIRAC CAN TARAC","MUHAMMED ALI KILINC",
    "FEDYE OMERI","SADIYE GUL KUSDEMIR","TUANA SUNA YALCIN","YAGMUR CETIN",
    "YAHYA NEBI ERDOGAN","ZELIHA SIFA KILIC"
]

MATRIS = np.array([[1,2],[4,3]])

def anahtar_uret(isim):
    toplam = 0
    for i, c in enumerate(isim.split()[0]):
        toplam += ord(c) * (i+1)
    return toplam % 256

def sifrele(metin, anahtar):
    veri = [ord(c) for c in metin]
    xor = [v ^ anahtar for v in veri]
    if len(xor) % 2 == 1:
        xor.append(0)

    sonuc = []
    for i in range(0,len(xor),2):
        v = np.dot(MATRIS, [[xor[i]],[xor[i+1]]]) % 256
        sonuc.extend([int(v[0][0]), int(v[1][0])])

    return base64.b64encode(bytes(sonuc)).decode()

def coz(b64, anahtar):
    data = list(base64.b64decode(b64))
    ters = np.linalg.inv(MATRIS)
    ters = np.round(ters * np.linalg.det(MATRIS)).astype(int)

    cozulmus = []
    for i in range(0,len(data),2):
        v = np.dot(ters, [[data[i]],[data[i+1]]]) % 256
        cozulmus.extend([int(v[0][0]), int(v[1][0])])

    return "".join(chr(v ^ anahtar) for v in cozulmus if v != 0)

class AnaEkran(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10)

        self.spinner = Spinner(text="Ogrenci Sec", values=SINIF_LISTESI)
        self.add_widget(self.spinner)

        self.girdi = TextInput(hint_text="Mesaj", multiline=True)
        self.add_widget(self.girdi)

        self.sonuc = Label(text="")
        self.add_widget(self.sonuc)

        btn1 = Button(text="Sifrele")
        btn1.bind(on_press=self.sifrele)
        self.add_widget(btn1)

        btn2 = Button(text="Coz")
        btn2.bind(on_press=self.coz)
        self.add_widget(btn2)

    def sifrele(self, x):
        anahtar = anahtar_uret(self.spinner.text)
        self.sonuc.text = sifrele(self.girdi.text, anahtar)

    def coz(self, x):
        anahtar = anahtar_uret(self.spinner.text)
        self.sonuc.text = coz(self.girdi.text, anahtar)

class AkilliKalkanApp(App):
    def build(self):
        return AnaEkran()

if __name__ == "__main__":
    AkilliKalkanApp().run()
