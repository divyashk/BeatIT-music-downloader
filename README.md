# BeatIT-music-downloader

This web-application allows you to download both audio and video from youtube. You can use either the link of the video or search through manually.

## hosted on [music.divyasheel.com](http://music.divyasheel.com)



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites

You need to install the following before you create a virtual env.


```
sudo apt update
sudo apt install python3-pip
```

### Installing

A step by step series of examples that teaches you how to get a development env running from the requirements.txt file.

First, clone the repo into your local machine.

```
git clone https://github.com/divyashk/BeatIT-music-downloader.git
```

now cd into the directory and create a virtual environment with any name(env is this illustration).

```
cd BeatIT-music-downloader & python3 -m venv env
```

now activate the virtual environment.

```
source ./env/bin/activate
```

install all the dependencies from the requirements.txt file

```
pip install -r requirements.txt
```
note that this web-app requires an youtube v3-API key to function, which can be obtained from google cloud platform(free of cost). You need to set an environment variable with the name 'API_KEY' as follows.

```
export 'API_KEY'="YOUR-API-KEY"
```
Now you are all set and ready to roll!
## Launching the application.

When in the root directory run the main.py file using the terminal.
```
python main.py
```
The site is now active on your local host server.


## Author

* **Divyasheel Kumar** - [divyashk](https://github.com/divyashk)
