from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.core.audio import SoundLoader
import os

class Tab(MDFloatLayout, MDTabsBase):
    pass

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    md_bg_color: 0.07, 0.07, 0.07, 1

    MDTopAppBar:
        title: "AHN Music"
        anchor_title: "left"
        right_action_items: [["magnify", lambda x: None], ["dots-vertical", lambda x: None]]
        elevation: 0
        md_bg_color: 0.07, 0.07, 0.07, 1

    MDTabs:
        id: tabs
        background_color: 0.07, 0.07, 0.07, 1
        indicator_color: 1, 1, 1, 1
        text_color_normal: 0.6, 0.6, 0.6, 1
        text_color_active: 1, 1, 1, 1
        
        Tab:
            title: "Tracks"
            ScrollView:
                MDList:
                    id: songs_list

    MDCard:
        orientation: 'horizontal'
        size_hint_y: None
        height: "75dp"
        padding: "10dp"
        spacing: "10dp"
        md_bg_color: 0.11, 0.11, 0.12, 1
        radius: [12, 12, 0, 0]
        elevation: 2

        MDIconButton:
            icon: "music-note"
            theme_icon_color: "Custom"
            icon_color: 1, 1, 1, 1
            pos_hint: {"center_y": .5}

        MDBoxLayout:
            orientation: 'vertical'
            pos_hint: {"center_y": .5}
            
            MDLabel:
                id: current_title
                text: "Tidak ada lagu diputar"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                font_style: "Body1"
                bold: True
                shorten: True
                shorten_from: "right"
                
            MDLabel:
                id: current_artist
                text: "Offline Player"
                theme_text_color: "Custom"
                text_color: 0.6, 0.6, 0.6, 1
                font_style: "Caption"

        MDIconButton:
            id: play_btn
            icon: "play"
            theme_icon_color: "Custom"
            icon_color: 1, 1, 1, 1
            pos_hint: {"center_y": .5}
            on_release: app.toggle_play()
'''

class AHNMusicApp(MDApp):
    sound = None
    is_playing = False
    current_song_path = ""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self):
        # Jalankan pencarian lagu di folder publik Android
        self.scan_songs()

    def scan_songs(self):
        # Jalur resmi penyimpanan internal HP Android
        paths_to_scan = [
            "/storage/emulated/0/Music",
            "/storage/emulated/0/Download",
            "./music"  # Folder lokal cadangan
        ]
        
        songs_found = False

        for target_dir in paths_to_scan:
            if os.path.exists(target_dir):
                try:
                    for root, dirs, files in os.walk(target_dir):
                        for file in files:
                            if file.endswith('.mp3'):
                                full_path = os.path.join(root, file)
                                item = OneLineListItem(
                                    text=file.replace('.mp3', ''),
                                    theme_text_color="Custom",
                                    text_color=(1, 1, 1, 1),
                                    on_release=lambda x, p=full_path: self.play_music(p)
                                )
                                self.root.ids.songs_list.add_widget(item)
                                songs_found = True
                except Exception:
                    continue
                    
        # Jika benar-benar kosong, buatkan 1 file lagu simulasi agar tidak kosong total
        if not songs_found:
            backup_dir = "./music"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Membuat judul dummy untuk memastikan UI bekerja
            item = OneLineListItem(
                text="[Contoh] Pindahkan file .mp3 ke folder Musik HP Anda",
                theme_text_color="Custom",
                text_color=(0.6, 0.6, 0.6, 1)
            )
            self.root.ids.songs_list.add_widget(item)

    def play_music(self, filepath):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

        self.current_song_path = filepath
        try:
            self.sound = SoundLoader.load(filepath)
            if self.sound:
                self.sound.play()
                self.is_playing = True
                self.root.ids.play_btn.icon = "pause"
                filename = os.path.basename(filepath).replace('.mp3', '')
                self.root.ids.current_title.text = filename
                self.root.ids.current_artist.text = "Lagu Lokal"
        except Exception as e:
            self.root.ids.current_title.text = "Gagal memutar file"

    def toggle_play(self):
        if self.sound:
            if self.is_playing:
                self.sound.stop()
                self.root.ids.play_btn.icon = "play"
                self.is_playing = False
            else:
                self.sound.play()
                self.root.ids.play_btn.icon = "pause"
                self.is_playing = True

if __name__ == '__main__':
    AHNMusicApp().run()
