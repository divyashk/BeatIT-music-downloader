from pytube import YouTube
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    url = "https://www.youtube.com/watch?v=ncVd9Kf7ZO4"

    video = YouTube(url)
    name = "test1"
     
    video.streams.filter(progressive=True).first().download("static/cache/video",name)
    
    return "Done"



if __name__ == "__main__":
    app.run(debug=True)

