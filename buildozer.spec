[app]

# ------------------------------
# TEMEL UYGULAMA BÝLGÝLERÝ
# ------------------------------
title = Akilli Kalkan
package.name = akillikalkan
package.domain = org.akillikalkan

version = 1.0

# ------------------------------
# PYTHON & KÜTÜPHANELER
# ------------------------------
source.dir = .
source.include_exts = py,kv,png,jpg

requirements = python3,kivy,numpy==1.23.5

# ------------------------------
# ANDROID AYARLARI (ÇOK ÖNEMLÝ)
# ------------------------------
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b

android.permissions = INTERNET
android.allow_backup = True

# ------------------------------
# GÖRÜNÜM & ORYANTASYON
# ------------------------------
orientation = portrait
fullscreen = 0

# ------------------------------
# BOOTSTRAP
# ------------------------------
bootstrap = sdl2

# ------------------------------
# LOG & HATA AYIKLAMA
# ------------------------------
log_level = 2

# ------------------------------
# BUILD ARAÇLARI
# ------------------------------
p4a.branch = master
p4a.bootstrap = sdl2

# ------------------------------
# ANDROID GRADLE
# ------------------------------
android.gradle_dependencies =
android.enable_androidx = True

# ------------------------------
# ÝKON (ÝSTEÐE BAÐLI)
# ------------------------------
# icon.filename = icon.png

# ------------------------------
# DÝÐER
# ------------------------------
warn_on_root = 1