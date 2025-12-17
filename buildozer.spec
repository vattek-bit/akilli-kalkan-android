[app]

title = AkilliKalkan
package.name = akillikalkan
package.domain = org.akillikalkan

version = 0.1

source.dir = .
source.include_exts = py,kv

requirements = python3,kivy,numpy==1.23.5

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.ndk = 25b

bootstrap = sdl2

log_level = 2
warn_on_root = 1