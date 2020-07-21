
from  __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import os
import urllib.request
from youtube_search import YoutubeSearch
import youtube_dl
import subprocess
import sys


# lenk = 'https://open.spotify.com/track/4mPOYg53faLL6brBcoZ5T8?si=zRIGUlsqThOdQm_AsXzioA' # link here
print("Welcome to Spotify Downloader")
print("Input a Spotify Link")

lenk = input()

if lenk.find('https://open.spotify.com') != 1:
    try:    
        res = requests.get(lenk)
        soup = BeautifulSoup(res.text,'lxml')
        title = soup.find('meta', property='og:title')
        artist_link = soup.find('meta', property="music:musician")['content']
        artist_page = BeautifulSoup(requests.get(artist_link).text,'lxml')
        artist_name = artist_page.find('meta', property='og:title')
        song = title['content']
        artist =  artist_name['content']
        song_name = str(song + " " + artist) 
        print( "Song Found :  " +  song_name)

        song_name_final = song_name.replace(" ", "+")
        pre_url = "https://www.youtube.com/results?search_query="
        yt_search = pre_url + song_name_final
        print(yt_search)

        results = list(YoutubeSearch(str(song_name), max_results=1).to_dict())[-1]
        # results2 = list(results)[-1]

        # print(type(results))

        results2 = str(results['url_suffix'])
        print(results2)
        
        print("Song Found")
        yt_pre = str("https://www.youtube.com/" + results2)
        print(yt_pre)
        print("Starting download...")
        # os.system('cmd /c "python mp3.py "')

        # youtube_dl.YoutubeDL(yt_pre)

        # checks if the required 'youtube-dl' package is available
        def check():
            import importlib
            try:                            # CHECKS if AVAILABLE
                importlib.import_module('youtube_dl')

            except ModuleNotFoundError:     # if NOT AVAILABLE --> then installs 'youtube-dl' python package
                print('youtube-dl NOT FOUND in this Computer !')
                print('The SCRIPT will install youtube-dl python package . . .')
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'youtube-dl'])

            finally:                        # if AVAILABLE --> then proceeds with downloading the music
                globals()['youtube_dl'] = importlib.import_module('youtube_dl')
                run()




        # Returns the default downloads path for linux or windows
        def get_download_path():
            if os.name == 'nt':         # for WINDOWS system
                import winreg
                sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
                downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                    location = winreg.QueryValueEx(key, downloads_guid)[0]
                return location
            else:                       # for LINUX & MAC
                return os.path.join(os.path.expanduser('~'), 'downloads')






        # gets ./ffmpeg.exe PATH 
        ffmpeg_path = os.getcwd()

        '''sets DEFALUT PATH for download Location'''
        path = get_download_path()

        ''' add a CUSTOM PATH for download loaction (remove '#' from the line BELOW & add the new PATH inside ' '(quotes) '''
        #path = ''

        # Main Download Script
        def run():
            options = {
                # PERMANENT options
                'format': 'bestaudio/best',
                'ffmpeg_location': f'{ffmpeg_path}/ffmpeg.exe',
                'keepvideo': False,
                'outtmpl': f'{path}/%(title)s.*',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320'
                }],

                #(OPTIONAL options)
                'noplaylist': True
            }

            # the 'youtube_dl' module will be imported on program run
            with youtube_dl.YoutubeDL(options) as mp3:
                mp3.download([yt_pre])
                print("Download Completed!")
                






        # runs Main Download Script


      
            
    except:
        print("Enter valid url")        
                
if __name__ == '__main__':
    check()
    



