'''
import requests

def fb_download(link):
    url = "https://facebook-reel-and-video-downloader.p.rapidapi.com/app/main.php"
    querystring = {"url":link}
    headers = {
        "X-RapidAPI-Key": "1ba4106eafmsh801fca8cea75c92p14a607jsn8628ffc128a4",
        "X-RapidAPI-Host": "facebook-reel-and-video-downloader.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    if response['success'] == True:
        title=response['title']
        thumbnail=response['thumbnail']
        low_q=response['links']['Download Low Quality']
        high_q=response['links']['Download High Quality']
        return (title,thumbnail,low_q,high_q)
    return 'Problem While Downloading'

print(fb_download("https://www.facebook.com/100004064092501/videos/1320534102209591/"))
'''

import requests
import os
import shutil
a=('Gabimaru vs. Zhu Jin 🔥\n\n#episode9\n#hellsparadise\n#anime | By Ryan', 'https://scontent-sin6-4.xx.fbcdn.net/v/t15.5256-10/350378394_691715226055298_4190701468780007873_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=b0ccae&_nc_ohc=wz7GuDX2w0sAX8Q_Wxr&_nc_ht=scontent-sin6-4.xx&oh=00_AfDhxdAT9dwdTDuL0HmpoyzbPDEjaSykS0RggRWj12Ki2A&oe=64FF0C87', 'https://video-sin6-2.xx.fbcdn.net/v/t42.1790-2/351092731_1406341039921908_194973637687690238_n.mp4?_nc_cat=102&ccb=1-7&_nc_sid=985c63&efg=eyJybHIiOjMyOSwicmxhIjoxMTUwLCJ2ZW5jb2RlX3RhZyI6InN2ZV9zZCJ9&_nc_ohc=WSbxaSLE3c4AX-mWdxN&rl=329&vabr=183&_nc_ht=video-sin6-2.xx&oh=00_AfBRlxmIeiz3T6kPf-sQSHa_ZQCppsME6-dAy03WDT-GaA&oe=64FEAE2B&dl=1', 'https://video-sin6-4.xx.fbcdn.net/v/t39.25447-2/362662499_298498396038543_8272200204041655462_n.mp4?_nc_cat=101&vs=82e1dc2dacd4a360&_nc_vs=HBksFQAYJEdHUEtuUldQcGR5U2V3OEJBS1lVMGZCQndzeHlibWRqQUFBRhUAAsgBABUAGCRHQW5oNUJRMWowWU0ydXNCQU5MWkFtRjBRTjRWYnY0R0FBQUYVAgLIAQBLB4gScHJvZ3Jlc3NpdmVfcmVjaXBlATENc3Vic2FtcGxlX2ZwcwAQdm1hZl9lbmFibGVfbnN1YgAgbWVhc3VyZV9vcmlnaW5hbF9yZXNvbHV0aW9uX3NzaW0AKGNvbXB1dGVfc3NpbV9vbmx5X2F0X29yaWdpbmFsX3Jlc29sdXRpb24AHXVzZV9sYW5jem9zX2Zvcl92cW1fdXBzY2FsaW5nABFkaXNhYmxlX3Bvc3RfcHZxcwAVACUAHIwXQAAAAAAAAAAREQAAACbI2Iauv%2BCkAxUCKAJDMxgLdnRzX3ByZXZpZXccF0B09VP3ztkXGCdkYXNoX3IyX2F2Y19nZW4xYXZjX2xjX3E4MF9mcmFnXzJfdmlkZW8SABgYdmlkZW9zLnZ0cy5jYWxsYmFjay5wcm9kOBJWSURFT19WSUVXX1JFUVVFU1QbCogVb2VtX3RhcmdldF9lbmNvZGVfdGFnBm9lcF9oZBNvZW1fcmVxdWVzdF90aW1lX21zATAMb2VtX2NmZ19ydWxlB3VubXV0ZWQTb2VtX3JvaV9yZWFjaF9jb3VudAUxMDMyMxFvZW1faXNfZXhwZXJpbWVudAAMb2VtX3ZpZGVvX2lkEDEzMjA1MzQxMDIyMDk1OTESb2VtX3ZpZGVvX2Fzc2V0X2lkDzY4NTI5MzM2MDI3NTMzMRVvZW1fdmlkZW9fcmVzb3VyY2VfaWQPOTI1MjQ3NTM4Nzc5Njg0HG9lbV9zb3VyY2VfdmlkZW9fZW5jb2RpbmdfaWQQMTA2ODUyMzE0Nzg4NjM4Ng52dHNfcmVxdWVzdF9pZAAlAhwAJcQBGweIAXMENjgxNAJjZAoyMDIzLTA2LTAzA3JjYgUxMDMwMANhcHAFVmlkZW8CY3QZQ09OVEFJTkVEX1BPU1RfQVRUQUNITUVOVBNvcmlnaW5hbF9kdXJhdGlvbl9zCjMzNS4zMzg2NDYCdHMVcHJvZ3Jlc3NpdmVfZW5jb2RpbmdzAA%3D%3D&ccb=1-7&_nc_sid=894f7d&efg=eyJ2ZW5jb2RlX3RhZyI6Im9lcF9oZCJ9&_nc_ohc=MG_eE_8VIK0AX-9uTWW&_nc_oc=AQnp3IrxUbl5O5tOa6gJTL50LhvYCwMUQsQsO6txOuE7xkXQRjxDJbs4iej_H9dz8h8&_nc_ht=video-sin6-4.xx&oh=00_AfAGhYYO_jyjtdBszEbh6ib7JD3Xf6-myCcZz7bw6QlS2g&oe=64FEEB98&_nc_rid=329511402165549&dl=1')

def down_vid(link,path):
    try:
        os.makedirs(os.path.join(path,'Video'))
        response = requests.get(link)
        if response.status_code == 200:
            file_name =  os.path.join(path,'Video', link.split("/")[-1].split('?')[0])
            print(file_name)
            with open(file_name, 'wb') as video_file:
                video_file.write(response.content)
                return True,1
    except Exception as e:
        return False,e

