from pytube import YouTube
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    url = "https://www.youtube.com/watch?v=ncVd9Kf7ZO4"

    video = YouTube(url)
    name = "test1"
     
    default_name=video.streams.filter(only_audio=True).first().default_filename
    
    return default_name;



if __name__ == "__main__":
    app.run(debug=True)

