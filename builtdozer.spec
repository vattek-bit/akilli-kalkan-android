[app]

# Uygulama adı
title = AkilliKalkan

# Paket adı (küçük harf, boşluk yok)
package.name = akillikalkan

# Paket domain (örnek)
package.domain = org.tekin

# main.py dosyası
source.dir = .
source.include_exts = py,png,jpg,kv

# Ana dosya
entrypoint = main.py

# Kütüphaneler
requirements = python3,kivy,numpy

# Android sürüm ayarları
android.api = 33
android.minapi = 21

# Ekran yönü
orientation = portrait

# Tam ekran
fullscreen = 1

# Log açık (hata ayıklamak için önemli)
log_level = 2

# İzinler
android.permissions = INTERNET

# Mimari (EN ÖNEMLİ KISIM)
android.archs = arm64-v8a,armeabi-v7a

# Build tipi
android.debug = 1

# Java ayarı
android.enable_androidx = True

# SDK & NDK otomatik indirilsin
android.accept_sdk_license = True

# Temiz build (hata azaltır)
android.clean_build = True


[buildozer]

# Buildozer sürümü
log_level = 2

# Android SDK/NDK yolu (Actions için boş kalmalı)
android.sdk_path =
android.ndk_path =
android.ant_path =

# Cache kullanma (ilk build için daha güvenli)
warn_on_root = 1
