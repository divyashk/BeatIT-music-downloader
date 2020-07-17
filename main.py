from flask import Flask, flash
from flask import render_template, url_for, redirect, request, session, send_from_directory
from scraping import generateURL, findVideos
from pytube import YouTube,Stream
from datetime import datetime
import time
import os
import shutil
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import moviepy.editor as mp
import re
from slugify import slugify
SECRET_KEY = os.urandom(32)
import pdb
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


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
            
            sortby = request.form["sortby"]
            search = request.form['search']
            
            results_dict=findVideos(generateURL(search,sortby),8)
            count = 0;
            
            while len(results_dict) == 0:
                count+=1;	
                if count > 10:	
                    return redirect(url_for("home"))
                results_dict=findVideos(generateURL(search))
            
            return render_template("home.html", title='Music Downloader', results_dict=results_dict, search=search)


        if "url" in request.form:
            url = request.form["url"]
            video = YouTube(url)
            
            #here ctitle is the name of the video that is independent of the pytube lib and has been scraped along with the url of the video.
            ctitle=request.form["ctitle"]
            stitle = slugify(ctitle)      #turned the name into file-valid name
    
            #here ytitle is the name of the video according to the pytube library
            ytitle=video.streams.first().default_filename

            img=request.form["thumbnail"]

            if "format" in request.form:
                format = request.form["format"]
            else:
                format = "mp3";

            # wont be using this for now
            # shutil.rmtree("static/cache", ignore_errors=True)
            
            if format == "mp4":                
                video.streams.filter(progressive=True).first().download("static/cache/video",stitle)
                
            else:
               
                video.streams.filter(only_audio=True).first().download("static/cache/audio",stitle)
                
                #convert all the downloaded mp4 files to mp3
               
                old = "static/cache/audio/"+stitle+".mp4"
                new = "static/cache/audio/"+stitle+".mp3"
                os.rename(old, new)
                                         
              
           
            return render_template("home.html", title="Music Downloader",stitle=stitle,ctitle=ctitle,img=img, format=format)

        


    return render_template('home.html', title='Music Downloader')

atexit.register(lambda: sched.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
