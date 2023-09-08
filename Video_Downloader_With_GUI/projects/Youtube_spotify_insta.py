from pytube import YouTube
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from youtubesearchpython import VideosSearch
import os
import instaloader
from moviepy.editor import *
import shutil

def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    return str(hours)+" hrs "+str(minutes)+" minutes "+str(remaining_seconds)+" seconds"


def bytes_to_human_readable(size_bytes):
    units = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3}
    for unit in ['GB', 'MB', 'KB', 'B']:
        if size_bytes >= units[unit]:
            size = size_bytes / units[unit]
            return f"{size:.2f} {unit}"
        

def get_youtube_video_info(video_url):
    yt = YouTube(video_url)
    video_info = {
        'thumbnail_url': yt.thumbnail_url,
        'title': yt.title,
        'channel_name': yt.author,
        'views': str(yt.views),
        'duration': convert_seconds_to_hms(yt.length),
        'vid_size': bytes_to_human_readable(yt.streams.get_highest_resolution().filesize),
        'aud_size': bytes_to_human_readable(yt.streams.filter(only_audio=True).first().filesize)
    }

    return video_info

def download_video(link,path):
    try:
        yt = YouTube(link)
        path=path+"/Videos"
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path=path)
        return True,1
    except Exception as e:
        return False,e

def download_audio(link,path):
    try:
        yt = YouTube(link)
        path=path+"/Audios"
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=path)
        return True,1
    except Exception as e:
        return False,e
    

def songname(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser').text
    return soup[:soup.find("|")]

def get_song_names(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    playlist=soup.text
    playlist=playlist[:playlist.find("|")]
    data = soup.findAll("meta", attrs={"name": "music:song"})
    song_urls = [i["content"] for i in data]
    with ThreadPoolExecutor(max_workers=len(song_urls)+1) as executor:
        list_of_songs = list(executor.map(songname, song_urls))
    list_of_songs.insert(0,playlist)
    return list_of_songs

def search_youtube(query):
    return VideosSearch(query, limit=1).result()['result'][0]["link"]

def link_fetcher(video_names):
    with ThreadPoolExecutor(max_workers=len(video_names)+1) as executor:
        list_of_links=list(executor.map(search_youtube, video_names))
    return list_of_links

def download_all_audios(video_urls, output_path):
    output_path=[output_path]*len(video_urls)
    workers=len(video_urls)+1
    video_urls=link_fetcher(video_urls)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(download_audio, video_urls,output_path)

def get_account_info_from_url(url):
    loader = instaloader.Instaloader()
    try:
        profile = instaloader.Post.from_shortcode(loader.context, url.split('/')[-2])
        account_name = profile.owner_username
        thumbnail_url = profile.url
        return account_name, thumbnail_url
    except instaloader.exceptions.ProfileNotExistsException:
        return "The provided URL does not correspond to a valid Instagram account."
    
def insta_video_downloader(url, path_name):
    L = instaloader.Instaloader()
    vid_path = os.path.join(path_name, "Videos")
    if not os.path.exists(vid_path):
        os.makedirs(vid_path)
    post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
    filename = str(post.owner_username)
    download_path = os.path.join(vid_path, filename)
    L.download_pic(filename=download_path, url=post.video_url, mtime=post.date_utc)

def insta_audio_downloader(url, path_name):
    L = instaloader.Instaloader()
    vid_path = os.path.join(path_name, "Audios", "temp")
    if not os.path.exists(vid_path):
        os.makedirs(vid_path)
    post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
    filename = str(post.owner_username)
    download_path = os.path.join(vid_path, filename)
    L.download_pic(filename=download_path, url=post.video_url, mtime=post.date_utc)

    aud_path = os.path.join(path_name, "Audios")
    video = VideoFileClip(download_path+'.mp4')
    audio = video.audio
    audio.write_audiofile(os.path.join(aud_path, f"{filename}.mp3"))
    video.close()
    audio.close()
    shutil.rmtree(vid_path)

def fb_download(link):
    url = "https://facebook-reel-and-video-downloader.p.rapidapi.com/app/main.php"
    querystring = {"url":link}
    headers = {
        "X-RapidAPI-Key": "1ba4106eafmsh801fca8cea75c92p14a607jsn8628ffc128a4",
        "X-RapidAPI-Host": "facebook-reel-and-video-downloader.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    if response['success'] == True:
        title=response['title'].strip()
        thumbnail=response['thumbnail']
        low_q=response['links']['Download Low Quality']
        high_q=response['links']['Download High Quality']
        return (title,thumbnail,high_q,low_q)
    return 'Problem While Downloading'

def down_vid(link,path):
    try:
        if not os.path.exists(os.path.join(path,'Videos')):
            os.makedirs(os.path.join(path,'Videos'))
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.join(path,'Videos', link.split("/")[-1].split('?')[0])
            with open(file_name, 'wb') as video_file:
                video_file.write(response.content)
                return True
    except Exception as e:
        return False
    
def fb_aud(link,path):
    try:
        if not os.path.exists(os.path.join(path,'Audios','temp')):
            os.makedirs(os.path.join(path,'Audios','temp'))
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.join(path,'Audios')
            name=link.split("/")[-1].split('?')[0][:-4]
            temp=os.path.join(path,'Audios','temp', link.split("/")[-1].split('?')[0])
            with open(temp, 'wb') as video_file:
                video_file.write(response.content)
            video = VideoFileClip(temp)
            audio = video.audio
            audio.write_audiofile(os.path.join(file_name, f"{name}.mp3"))
            video.close()
            audio.close()
            shutil.rmtree(os.path.join('Downloads','Audios','temp'))
            return True
            
    except Exception as e:
        return False