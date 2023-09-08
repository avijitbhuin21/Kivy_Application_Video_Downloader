'''from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from Youtube_spotify import get_youtube_video_info,download_audio,download_video,get_song_names,songname
from kivy.properties import StringProperty,ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatButton





class HomeScreen(Screen):
    pass

class YTScreen(Screen):
    
    def yt_update_btn_txt(self):
        self.children[0].text="Checking..."
        Clock.schedule_once(lambda dt: self.link_to_details(), 0.1)

    def link_to_details(self):
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
        Clock.schedule_once(lambda dt: self.link_to_details1(), 0.1)

    def link_to_details1(self):
        path = self.ids.sp_path_input.text
        if path == "":
            path = "Downloads"
        link = self.ids.sp_text_input.text
        if "track" in link:
            names = songname(link)
            self.ids.sp_songview.text = names
            self.children[1].text = "Check"
        else:
            names=get_song_names(link)
            self.manager.get_screen('sp_list').list_update(names)
            self.manager.current = 'sp_list'
            self.children[1].text = "Check"
            
            
class SP_list_Screen(Screen):
    def __init__(self, **kwargs):
        super(SP_list_Screen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

    def list_update(self, my_list):
        self.layout.clear_widgets()
        self.my_list = my_list
        self.b_l()
    
    def b_l(self):
        layout = BoxLayout(orientation='vertical')
        scrollview = ScrollView()
        self.selected_songs = []

        grid_layout = GridLayout(cols=1, spacing=0, size_hint_y=None, padding=25)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        self.checkboxes = []
        self.list_display(grid_layout,scrollview,layout)
    

    def list_display(self,grid_layout,scrollview,layout):
        for song in self.my_list:
            checkbox_layout = BoxLayout(orientation='horizontal', size_hint=(0.2, None))
            label = Label(text=song, size_hint=(0.5, None),color=(0, 0, 0, 1))
            checkbox = CheckBox(size_hint=(0.5, None))
            checkbox.label = song
            checkbox.active = False
            checkbox.bind(active=self.on_checkbox_active)
            checkbox_layout.add_widget(label)
            checkbox_layout.add_widget(checkbox)
            self.checkboxes.append(checkbox)
            grid_layout.add_widget(checkbox_layout)
        self.a_l(scrollview,grid_layout,layout)
        
    def a_l(self,scrollview,grid_layout,layout):
        scrollview.add_widget(grid_layout)
        layout.add_widget(scrollview)

        download_button = MDRectangleFlatButton(text='Download Selected', size_hint=(1, 0.1), on_press=self.download_selected_songs)
        layout.add_widget(download_button)
        self.add_widget(layout)

    def on_checkbox_active(self, checkbox, value):
        song_name = checkbox.label
        if value:
            self.selected_songs.append(song_name)
        else:
            self.selected_songs.remove(song_name)

    def download_selected_songs(self, instance):
        print("Selected Songs:")
        print(self.selected_songs)




class FBScreen(Screen):
    pass
class IGScreen(Screen):
    pass



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
sm.add_widget(SP_list_Screen(name='sp_list'))



class Video_Downloader(MDApp):

    def build(self):
        screen = Builder.load_file("screen.kv")
        return screen


Video_Downloader().run()'''

'''class SP_list_Screen(Screen):
    def __init__(self, **kwargs):
        super(SP_list_Screen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

    def list_update(self, my_list):
        self.layout.clear_widgets()
        self.my_list = my_list
        self.b_l()
    
    def b_l(self):
        layout = BoxLayout(orientation='vertical')
        scrollview = ScrollView()
        self.selected_songs = []

        grid_layout = GridLayout(cols=1, spacing=dp(20), size_hint_y=None, padding=dp(5))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        self.checkboxes = []
        self.list_display(grid_layout, scrollview, layout)
    

    def list_display(self, grid_layout, scrollview, layout):
        for i in range (1,len(self.my_list)):
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
        self.a_l(scrollview, grid_layout, layout,self.my_list[0])
        
    def a_l(self, scrollview, grid_layout, layout,lab_head):
        scrollview.add_widget(grid_layout)
        layout.add_widget(scrollview)

        download_button = MDRectangleFlatButton(text='Download Selected', size_hint=(1, 0.1), on_press=self.download_selected_songs)
        layout.add_widget(download_button)
        self.add_widget(layout)

        heading=Label(text=lab_head,size_hint=(1,0.1))
        layout.add_widget(heading)
        self.add_widget(layout)



    def on_checkbox_active(self, checkbox, value):
        song_name = checkbox.label
        if value:
            self.selected_songs.append(song_name)
        else:
            self.selected_songs.remove(song_name)

    def back(self):
        self.manager.current = 'spotify'

    def download_selected_songs(self, instance):
        print("Selected Songs:")
        print(self.selected_songs)'''