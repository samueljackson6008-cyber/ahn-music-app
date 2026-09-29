[app]
title = AHN Music
package.name = ahnmusic
package.domain = org.ahn
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 0.1
requirements = python3, kivy==2.3.1, kivymd==2.0.0, pillow
orientation = portrait
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
