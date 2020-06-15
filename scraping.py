
#####scraping################

from bs4 import BeautifulSoup as bs
import time
import requests
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry


def generateURL(search="", sortby="Relevance"):
    search = search.split(" ")
    url = "https://www.youtube.com/results?search_query="
    for s in search:
        if s is search[0]:
            url = url + s
        else:
            url = url + '+' + s
        if sortby=="Views":
            url += "&sp=CAMSAhgB"
        elif sortby=="Rating":
            url += "&sp=CAESAhgB"
        elif sortby=="Upload date":
            url += "&sp=CAISAhgB"

    
    return url


def findVideos(url,limit=5):
    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)

    # sCode = requests.get(url,verify=False)

    sCode = ""
    while sCode == "":
        try:
            sCode = requests.get(url)
            break
        except:
            time.sleep(5)

    # sCode = requests.get(url)
    page = sCode.text

    
    soup = bs(page, 'html.parser')
    
    #stores all the website links in results
    results = soup.select("#results ol li:nth-child(2) ol>li")

    #used for understanding the stru#page-topcture of the parsed html
    #open('parsed.html','w',encoding="utf8").write(page)


    home = "https://www.youtube.com"

    allVideos = []


    #limit for videos is 5 by default
    
    count = 0;

    #storing all the video data
    for video in results:
        
        # to check that the video there because of a channel
        if video.find("ul")!=None and video.find('ul').has_attr('class') and video.find('ul')["class"][0]=="shelf-content":
            continue
        link = video.find("a")
        if link["href"][1] == 'w':
            link = home + link["href"]



            img = video.find("img")
            if img != None:
                img_check = img["src"]
                if img_check[0] == "/" and img.has_attr('data-thumb'):                 #if the src doesn't have the right address then store the one from data-thumb
                    img_check = img["data-thumb"]
                img=img_check
                if img[0] == "/":
                    img=None




            name = video.find("h3")
            if name!=None:
                name = name.a["title"]

            views = video.find('ul', class_="yt-lockup-meta-info")
            if views != None and len(views.find_all("li"))==2:
                views = views.select("li")
                views = views[1].get_text()
                split_views = views.split(' ')
                if split_views[1] != "views":
                    continue;
            else:
                views = None

            if name == None or views==None or img==None:
                continue;
            allData={
                "link":link,
                "name":name,
                "img":img,
                "views":views
            }
            allVideos.append(allData)
            count+=1
            if count > limit:
                break;


    return allVideos




