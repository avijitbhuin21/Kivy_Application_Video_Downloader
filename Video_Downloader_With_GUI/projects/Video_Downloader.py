from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from Youtube_spotify_insta import get_youtube_video_info,download_audio,download_video,get_song_names,songname,search_youtube,download_all_audios,insta_video_downloader,get_account_info_from_url,insta_audio_downloader,fb_download,down_vid,fb_aud
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
import os
import shutil





class HomeScreen(Screen):
    pass

class YTScreen(Screen):
    
    def yt_update_btn_txt(self):
        self.children[0].text="Checking..."
        Clock.schedule_once(lambda dt: self.link_to_details(), 0.1)

    def link_to_details(self):
        self.children[0].text="Check"
        link = self.ids.yt_text_input.text
        path=self.ids.yt_path_input.text
        if path=="":
            path="Downloads"
        self.manager.current = 'details_yt'
        self.manager.get_screen('details_yt').set_link(link,path)


class ytdetailsScreen(Screen):
    thumbnail_url = StringProperty()
    title = StringProperty()
    channel_name = StringProperty()
    views = StringProperty()
    duration = StringProperty()
    path=StringProperty()
    link=StringProperty()
    vid_size=StringProperty()
    aud_size=StringProperty()


    def set_link(self, link,path):
        thumb_link=get_youtube_video_info(link)
        self.thumbnail_url = thumb_link['thumbnail_url']
        self.title = thumb_link['title']
        self.channel_name = thumb_link['channel_name']
        self.views = thumb_link['views']
        self.duration = thumb_link['duration']
        self.vid_size=  thumb_link['vid_size']
        self.aud_size=  thumb_link['aud_size']
        self.path = path
        self.link = link

    def vid(self,link,path):
        self.ids.choice.text ="Downloading..."
        Clock.schedule_once(lambda dt: self.download_and_update(link, path,1), 0.1)

    def audio(self,link,path):
        self.ids.choice.text ="Downloading..."
        Clock.schedule_once(lambda dt: self.download_and_update(link, path,0), 0.1)

    def download_and_update(self, link, path,c):
        if c==1:
            a, b = download_video(link, path)
        else:
            a, b = download_audio(link, path)
        if a:
            self.ids.choice.text = "Download Completed Successfully ;)"
        else:
            self.ids.choice.text = "Error downloading video: " + b


class SpotifyScreen(Screen):

    def sp_update_btn_txt(self):
        self.children[1].text = "Checking..."
        self.ids.sp_songview.text = ""
        if 'sp_list' in sm.screen_names:
            sm.remove_widget(sm.get_screen('sp_list'))
        sm.add_widget(SP_list_Screen(name='sp_list'))
        Clock.schedule_once(lambda dt: self.link_to_details1(), 0.1)

    def link_to_details1(self):
        path = self.ids.sp_path_input.text
        if path == "":
            path = "Downloads"
        link = self.ids.sp_text_input.text
        if "track" in link:
            names = songname(link)
            self.ids.sp_songview.text = names
            self.children[1].text = "check"
            Clock.schedule_once(lambda dt: self.chk(names,path),0.1)

        else:
            names=get_song_names(link)
            self.manager.get_screen('sp_list').list_update(names,path)
            self.manager.current = 'sp_list'
            self.children[1].text = "Check"

    def chk(self,names,path):
        link=search_youtube(names)
        self.ids.sp_songview.text = names+'\n\n'+"Downloading..."
        Clock.schedule_once(lambda dt: self.dwn(names,link,path), 0.1)

    def dwn(self,names,link,path):
        a,b=download_audio(link,path)
        if a==True:
            self.ids.sp_songview.text = names+'\n\n'+"Downloaded Complete"
        else:
            self.ids.sp_songview.text = names+'\n\n'+"Error While Downloading: "+b


class SP_list_Screen(Screen):
    name = "sp_list"
    layout = BoxLayout(orientation='vertical')

    def list_update(self, my_list,path):
        self.layout.clear_widgets()
        self.my_list = my_list[1:]
        self.my_list_copy=self.my_list
        self.heading=my_list[0]
        self.down_path=path
        self.b_l()
    
    def b_l(self):
        self.layout = BoxLayout(orientation='vertical')
        top_padding_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        icon_button = MDIconButton(icon='arrow-left', on_release=self.back)
        label = Label(text=self.heading, halign='left', color=(0, 0, 0, 1), text_size=(350, None))
        top_padding_layout.add_widget(icon_button)
        top_padding_layout.add_widget(label)
        self.layout.add_widget(top_padding_layout)
        scrollview = ScrollView()
        self.selected_songs = []
        grid_layout = GridLayout(cols=1, spacing=dp(20), size_hint_y=None, padding=dp(5))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        self.checkboxes = []
        self.list_display(grid_layout, scrollview, self.layout)
    
    def list_display(self, grid_layout, scrollview, layout):

        for i in range (len(self.my_list)):
            checkbox_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
            label = Label(text=self.my_list[i], size_hint=(0.7, None), color=(0, 0, 0, 1),height=dp(30),text_size=(250,None))
            checkbox = CheckBox(size_hint=(0.3, None), height=dp(30), color=(0, 0, 0, 1))
            checkbox.label = self.my_list[i]
            checkbox.active = False
            checkbox.bind(active=self.on_checkbox_active)
            checkbox_layout.add_widget(label)
            checkbox_layout.add_widget(checkbox)
            self.checkboxes.append(checkbox)
            grid_layout.add_widget(checkbox_layout)
        self.a_l(scrollview, grid_layout, layout)
        
    def a_l(self, scrollview, grid_layout, layout):
        scrollview.add_widget(grid_layout)
        layout.add_widget(scrollview)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))

        download_button = MDRectangleFlatButton(text='Download Selected', size_hint=(0.5, 1),on_press=self.download_selected_songs)
        buttons_layout.add_widget(download_button)

        select_all_button = MDRectangleFlatButton(text='Download All', size_hint=(0.5, 1), on_press=self.select_all)
        buttons_layout.add_widget(select_all_button)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def select_all(self,instance):
        select_all_btn=instance
        select_all_btn.text="Downloading..."
        Clock.schedule_once(lambda dt: self.download_all(1,select_all_btn), 0.1)

    def on_checkbox_active(self, checkbox, value):
        song_name = checkbox.label
        if value:
            self.selected_songs.append(song_name)
        else:
            self.selected_songs.remove(song_name)

    def back(self,instance):
        self.manager.current = 'spotify'

    def download_selected_songs(self, instance):
        download_button = instance
        download_button.text = "Downloading..."
        Clock.schedule_once(lambda dt: self.download_all(download_button,1), 0.1)

    def download_all(self, download_button,select_all_btn):
        if download_button==1:
            select_all_btn.text='Download All'
            l=self.my_list_copy
        else:
            download_button.text = "Download Selected"
            if self.selected_songs!=[]:
                l=self.selected_songs
            else:
                download_button.text = "No Song Selected"
        download_all_audios(l,self.down_path)
        
class IGScreen(Screen):
    
    def ig_update_btn_txt(self):
        self.children[0].text="Checking..."
        Clock.schedule_once(lambda dt: self.link_to_details(), 0.1)

    def link_to_details(self):
        link = self.ids.ig_text_input.text
        path=self.ids.ig_path_input.text
        if path=="":
            path="Downloads"
        self.children[0].text="Check"
        self.manager.current = 'details_ig'
        self.manager.get_screen('details_ig').set_ig(link,path)
    

class IgdetailsScreen(Screen):
    thumbnail_url = StringProperty()
    title = StringProperty()
    path=StringProperty()
    link=StringProperty()
    dwn_Path=StringProperty()
    filename=StringProperty()
    chk=StringProperty('not clicked')

    def set_ig(self,link,path):
        self.path=path
        self.title,self.thumbnail_url=get_account_info_from_url(link)
        self.link=link

    def ig_vid_down(self,url,path):
        insta_video_downloader(url,path)

    def ig_audio_down(self,url,path):
        insta_audio_downloader(url,path)
        
class FBScreen(Screen):
    def fb_update_btn_txt(self):
        self.children[0].text="Checking..."
        Clock.schedule_once(lambda dt: self.link_to_details(), 0.1)

    def link_to_details(self):
        self.children[0].text="Check"
        link = self.ids.fb_text_input.text
        path=self.ids.fb_path_input.text
        if path=="":
            path="Downloads"
        self.manager.current = 'details_fb'
        self.manager.get_screen('details_fb').set_link(link,path)

class fbdetailsScreen(Screen):
    thumbnail_url = StringProperty()
    title = StringProperty()
    path=StringProperty()
    high_q=StringProperty()
    checker=StringProperty('not clicked')
    file_path=StringProperty()
    name=StringProperty()

    def set_link(self, link,path):
        thumb_link=fb_download(link)
        self.thumbnail_url = thumb_link[1]
        self.title = thumb_link[0]
        self.high_q = thumb_link[2]
        self.path = path

    def hy_vid(self):
        self.ids.choice.text ="Downloading..."
        Clock.schedule_once(lambda dt: self.download_and_update(1), 0.1)
    
    def fb_aud_down(self):
        self.ids.choice.text ="Downloading..."
        Clock.schedule_once(lambda dt: self.download_and_update(0), 0.1)

    def download_and_update(self,c):
        if c==1:
            status = down_vid(self.high_q, self.path)
            if status:
                self.ids.choice.text = "Download Completed Successfully ;)"
                self.checker='clicked'
                Clock.schedule_once(lambda dt: self.reset(), 2)
            else:
                self.ids.choice.text = "Error downloading video" 
                Clock.schedule_once(lambda dt: self.reset(), 2)
        else:
            status=fb_aud(self.high_q,self.path)
            if status:
                self.ids.choice.text = "Download Completed Successfully ;)"
                self.checker='clicked'
                Clock.schedule_once(lambda dt: self.reset(), 2)
            else:
                self.ids.choice.text = "Error downloading audio" 
                Clock.schedule_once(lambda dt: self.reset(), 2)

        
    def reset(self):
        self.ids.choice.text = 'Please Choose One'





#size of the window
Window.size=(340,600)
# Create the screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='Home'))
sm.add_widget(YTScreen(name='yt'))
sm.add_widget(FBScreen(name='fb'))
sm.add_widget(IGScreen(name='spotify'))
sm.add_widget(SpotifyScreen(name='ig'))
sm.add_widget(ytdetailsScreen(name='details_yt'))
sm.add_widget(IgdetailsScreen(name='details_ig'))
sm.add_widget(fbdetailsScreen(name='details_fb'))





class Video_Downloader(MDApp):

    def build(self):
        screen = Builder.load_file("screen.kv")
        return screen

    def on_stop(self):
        shutil.rmtree('projects\__pycache__')

Video_Downloader().run()