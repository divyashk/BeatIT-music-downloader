from flask import Flask, flash
import requests
from flask import render_template, url_for, redirect, request, session, send_from_directory
from datetime import datetime
import time
import os
import shutil
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import moviepy.editor as mp
import re
from slugify import slugify
import pdb
from youtube_dl import YoutubeDL
import os
from moviepy.editor import *
import validators
import pafy

app = Flask(__name__)



SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['API_KEY'] = os.environ.get("API_KEY")
def sensor():
    try:
        shutil.rmtree('/static/cache',ignore_errors=True)
    except:
        pass

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',hours=24)
sched.start()

@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def home():
    
    
    if request.method=="POST":
        
        if "search" in request.form:

            # storing the search form-data
            sortby = request.form["sortby"]
            search = request.form['search']
            
            valid=validators.url(search)
            if search[:32] == "https://www.youtube.com/watch?v=":
                video = True
            if valid==True and video:
                # if the search-input is a valid URL and points to a youtube video
                url = search
                ind = url.find("?v=");
                id = url[ind+3:]            #extracting the id of the video from the url
                
                #using youtube API call to find the details of the video using the `id   
                video_ids = []
                video_ids.append(id)
                id_search_params = {
                    'key': app.config['API_KEY'],
                    'id': ','.join(video_ids),
                    'part': 'snippet,contentDetails,statistics',
                    'maxResults': 9
                }
                api_url_for_id = 'https://www.googleapis.com/youtube/v3/videos';
                with_id = requests.get(api_url_for_id, params=id_search_params);
                video_details = [];
                for video in with_id.json()['items']:
                    
                    temp = {
                        'id': video['id'],
                        'title': video['snippet']['title'],
                        'thumbnail': video['snippet']['thumbnails']['medium']['url'],
                        'views': video['statistics']['viewCount'],
                        
                    }
                    
                    video_details.append(temp);
            
                return render_template("home.html", title='Music Downloader', results_dict=video_details, search=search)

            else:
                # if the input is not an URL                
                if sortby == 'Relevance':
                    order = "relevance";
                elif sortby == 'Views':
                    order = "viewCount";
                elif sortby == 'Upload date':
                    order = "date";
                elif sortby == 'Rating':
                    order = "rating";


                # using youtube API call to find the search results
                api_url_for_search = 'https://www.googleapis.com/youtube/v3/search'
                search_params = {
                    'key': app.config['API_KEY'],
                    'q': search,
                    'part': 'snippet',
                    'maxResults': 9,
                    'type': 'video',
                    'order': order
                }
                r = requests.get(api_url_for_search, params=search_params);


                #storing the ID's of the result           
                video_ids = [];
                for video in r.json()['items']:
                    video_ids.append(video['id']['videoId']);


                #using the search id's to find the video details with another API call
                id_search_params = {
                    'key': app.config['API_KEY'],
                    'id': ','.join(video_ids),
                    'part': 'snippet,contentDetails,statistics',
                    'maxResults': 9
                }
                api_url_for_id = 'https://www.googleapis.com/youtube/v3/videos';
                with_id = requests.get(api_url_for_id, params=id_search_params);
                video_details = [];
                for video in with_id.json()['items']:
                    temp = {
                        'id': video['id'],
                        'title': video['snippet']['title'],
                        'thumbnail': video['snippet']['thumbnails']['medium']['url'],
                        'views': video['statistics']['viewCount'],
                    }
                    video_details.append(temp);
                return render_template("home.html", title='Music Downloader', results_dict=video_details, search=search)

        if "url" in request.form:
            url = request.form["url"]
            img=request.form["thumbnail"]
            
            
            #here ctitle is the name of the video that is independent of the pytube lib and has been fetched using Youtube API
            ctitle=request.form["ctitle"]
            stitle = slugify(ctitle)      #turned the name into file-valid name

            video = pafy.new(url)
            best = video.getbest()
            video_file = best.download(filepath='static/cache/video/'+stitle+"."+best.extension)
            mp4 = best.extension
            besta = video.getbestaudio()
            mp3 = besta.extension
            audio_file = besta.download(filepath='static/cache/audio/'+stitle+"."+besta.extension)
            # ydl_opts = {
            # 'format': 'best',      #this site isn't meant for commercial applications, therefore minimum quality would suffice
            # 'outtmpl': 'static/cache/video/'+stitle+'.mp4',
            # 'noplaylist': True,
            # 'extract-audio': True,
            # }
            # video = url
            # with YoutubeDL(ydl_opts) as ydl:
            #     info_dict = ydl.extract_info(video, download=True)
             
            # #using youtube-dl for download the video
            
            # ydl_opts = {
            #     'format': 'bestaudio/best',
            #     'outtmpl': 'static/cache/video/'+stitle+'.mp3',
            #     'postprocessors': [{
            #         'key': 'FFmpegExtractAudio',
            #         'preferredcodec': 'mp3',
            #         'preferredquality': '192',
            #     }],
            # }
            # with YoutubeDL(ydl_opts) as ydl:
            #     ydl.download([video]) 
            



            return render_template("home.html", title="Music Downloader",stitle=stitle,ctitle=ctitle,img=img, mp3=mp3, mp4=mp4)

    return render_template('home.html', title='Music Downloader')

atexit.register(lambda: sched.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
