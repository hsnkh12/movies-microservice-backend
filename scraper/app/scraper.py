from bs4 import BeautifulSoup
import requests
from .utils import titleParser
import re
import json
import concurrent.futures
import time
from fp.fp import FreeProxy
from . import db

class MovieScraper:


    CATEGORIES = {
        "documentary":"وثائقية",
        "music":"موسيقية",
        "adventure":"مغامرة",
        "comedy":"كوميديا",
        "mystery":"غموض",
        "strange":"غربية",
        "family":"عائلية",
        "sport":"رياضة",
        "romantic":"رومانسية",
        "horror":"رعب",
        "drama":"دراما",
        "science fiction":"خيال-علمي",
        "fantasy":"خيال",
        "war":"حرب",
        "crime":"جريمة",
        "history":"تاريخ",
        "anime":"انيميشن",
        "action":"اكشن",
        "thrilling":"اثارة"
    }
    
    LANGUAGES = {
        "الانجليزية":"english",
        "العربية":"arabic",
        "الإسبانية":"spanish",
        "الهندية":"indian",
        "الالمانية":"german",
        "الايطالية":"italian",
        "البرتغالية":"portuguese",
        "الفرنسية":"french",
        "اليابانية":"japanese",
        "الروسية":"russian",
        "الصينية":"chinese",
        "التايلندية":"thai",
        "التركية":"turkish",
        "السويدية":"swedish",
        "الهولندية":"dutch"
    }

    proxy = None

    def __init__(self, category, page_s,page_e, store_in_db=False, threads=16):

        #self.proxy = {"https": FreeProxy(country_id=['US']).get() } 
        self.movies_len = 0
        self.category = category
        self.page_s = page_s
        self.page_e = page_e
        self.store_in_db = store_in_db
        self.threads = threads
        try:
            self.url = f"https://egybest.mx/category/movie/{self.CATEGORIES[category]}?page="
        except:
            print("SCRAPER ERROR: This category does not exist")
            self.url = None

    def __getSourceFile(self,iframe_src):

        if "img" in iframe_src:
            return None
        
        res = requests.get(iframe_src)
        soup = BeautifulSoup(res.content,'lxml')

        scripts = soup.find_all('script')

        for script in scripts:

            r = re.findall(r"https?.*?\.mp4", script.text)
            if len(r) > 0:
                return r[0]
    
    def __getDuration(self,trs):

        duration_td = trs[5].find_all("td")[1]

        duration_text = duration_td.text

        return duration_text[0: duration_text.index(" ")]
    
    def __getLanguage(self, trs):

        language_td = trs[1]

        language_text = language_td.find_all("a")[0].text.strip()

        return self.LANGUAGES[language_text]
    
    def __getCategories(self,trs):

        categories_td = trs[3].find_all("td")[1]
        categories = []

        for a in categories_td.find_all("a"):

            value = a.text.strip()
            key = ""

            for k,v in self.CATEGORIES.items():
                if v == value:
                    key = k
                    break

            categories.append(key)

        return categories

    def __getInformation(self,tbody):

        trs = tbody.find_all("tr")
        
        categories = self.__getCategories(trs)
        duration = self.__getDuration(trs)
        language = self.__getLanguage(trs)


        return {"categories":categories,
                "duration":duration,
                "language":language}

    def __scrapMovieDetails(self, movie_watch_url):

        
        res = requests.get(movie_watch_url)
        soup = BeautifulSoup(res.content, 'lxml')
        iframe = soup.find_all("iframe")[-1]
        iframe['data-src'] = iframe['data-src'].replace('\r',"")

        video_source_file =  self.__getSourceFile(iframe['data-src'])

        tbody = soup.find("tbody")

        information = self.__getInformation(tbody)
        
        
        return {'video_src': video_source_file,
                'information': information}
    

    def __scrapMovie(self,a):

        movie = {}

        try:
            movie_id = a['href'][a['href'].index("movies/")+7:]
            movie_watch_url = f"https://egybest.mx/movies/watch/{movie_id}"
            movie_title = titleParser(a["title"])

            if self.store_in_db:
                if db.doesMovieExist(movie_title.strip()) == True:
                    return 

            image_url = a.find("img")['data-src']

            details = self.__scrapMovieDetails(movie_watch_url)

            movie["title"]= movie_title.strip()
            movie["image_src"]= image_url
            movie["video_src"]= details["video_src"]
            movie["categories"]= details["information"]["categories"]
            movie["duration"]= details["information"]["duration"]
            movie["language"]= details["information"]["language"]
            movie["date_added"] = int(round(time.time() * 1000))


            if self.store_in_db:
                self.__storeMovieInDB(movie)
            else:
                print(movie)

            self.movies_len +=1

        except Exception as err:
            print(f"SCRAPER ERROR: {err}")
            return 

        


    def __scrapPage(self, page_number):

        print(f"category: {self.category} - page number: {page_number}")
        url = self.url+f'{page_number}'
        res = requests.get(url)

        soup = BeautifulSoup(res.content,"lxml")
        movies_div = soup.find("div",{"class":"loaded-data"})

        try:
            movies_as = movies_div.find_all("a")
        except:
            print(f"No movies in page {page_number} for category '{self.category}'")
            return False

        if len(movies_as) == 0:
            print(f"No movies in page {page_number} for category '{self.category}'")
            return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:

            executor.map(self.__scrapMovie, movies_as)



    def scrap(self):

        if self.url == None:
            return None
        
        startTime = time.time()

        for page in range(self.page_s,self.page_e+1):
            self.__scrapPage(page)

        endTime = time.time() - startTime

        print(f"Number of movies scraped: {self.movies_len}")
        print(f"Elapsed time: {endTime}")


    def __storeMovieInDB(self, data):

        db.insertNewMovie(data)