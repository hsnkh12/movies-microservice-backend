# movies-microservice-app


## Technologies used
- Nodejs 
- Python
- RabbitMQ
- Firebase


## Installation

Clone git repo.
```
git clone https://github.com/hsnkh12/movies-microservice-app.git
```
Create Python virtual environment for **scraper app**
```
cd scraper
python3 -m venv venv
source venv/bin/activate
```
Download scraper requirements
```
pip3 install -r requirements.txt
```

Download node modules for **backend app** 
```
cd backend 
npm install
```
Generate your own **service_account_key.json** file using firebase and add it to the project

## Run the application

### Configure scraper
Go to **scraper/app/celery.py**. scraper default configuration will be as follows:
```python
MovieScraper(category=category, page_s=1, page_e=5, store_in_db=True, threads=8)
```
You can change page range by changing ```page_s``` which is starting page, and ```page_e``` which is ending page range. Check **scraper/notes.txt** to know total number of pages for each category according to **egybest.com**. 

```store_in_db``` means if you want to store the data into database after scraping, you can set it to False if you want to just test the scraping.

```threads``` stands for how many threads per worker process, which determines how fast you want the scraping processs to be.

### Run Scraper
```
cd scraper 
source venv/bin/activate
celery -A app.celery worker  --loglevel info
```

### Run Backend 
```
cd backend 
nodemon app.js
```


## How does it work
1- Request sent to backend asking for movies in a category

2- Bakcend replies with current stored movies in database

3- backend queues a new task to scrap new movies with this category

4- Rabbitmq assigns this task to the celery app

5- Celery app execute scraping and storing process



## How to use
choose a category from any categories provided in **scraper/notes.txt**. Let's say "documentary".
Then by using any rest api client. Send the following request:
```
http://localhost:8000/?category=documentary&page=1
```
You will get something like the follwoing:
```json
[
    {
        "categories": [
            "documentary"
        ],
        "video_src": "https://no-03.vidboo.org/6jmnqj6iuiazsalriw3afznqlgkfpgh7qunucccs4nol45xihjyxv4zpz4ja/v.mp4",
        "date_added": 1678973235508,
        "image_src": "https://egybest.mx/uploads/m/4440c5b675bdc5a84e802ed34d69b213.jpg",
        "language": "english",
        "duration": "100",
        "title": "The 11th Hour 2007"
    },
    {
        "categories": [
            "documentary"
        ],
        "title": "Girl in the Picture 2022",
        "date_added": 1678973235278,
        "duration": "101",
        "image_src": "https://egybest.mx/uploads/m/b7905077cd7da3287514dc1a7d7f6669.jpg",
        "video_src": "https://no-02.vidboo.org/6jmnx4pwuiazsalriw3af5p2kotpkdzqgg64sfswhiyclk366m2qscbizhkq/v.mp4",
        "language": "english"
    },
    {
        "categories": [
            "documentary"
        ],
        "duration": "96",
        "image_src": "https://egybest.mx/uploads/m/2504e19b04cb80fc736495206b1778b9.jpg",
        "language": "english",
        "video_src": "https://no-02.vidboo.org/6jmnqjxwuiazsalriw3afihuipu7k4snmrdspfzlsirgtc3pg7yhrlbienpq/v.mp4",
        "date_added": 1678973233921,
        "title": "Before the Flood 2016"
    },
    .....
]
```



To search for a specific movie:
```
http://localhost:8000/{MOVIE TITLE}
ex:
http://localhost:8000/Escape Plan The Extractors 2019
```
You will get something like the follwoing:

```json
{
    "duration": "97",
    "date_added": 1678977822134,
    "video_src": "https://no-04.vidboo.org/6jmnvkojuiazsalriw3af25waj35hgk2lozhfynckp5a6r472ujgkvd72j5a/v.mp4",
    "language": "english",
    "categories": [
        "action"
    ],
    "title": "Escape Plan The Extractors 2019",
    "image_src": "https://egybest.mx/uploads/m/842c46b4b6556f858423dc22b48c601a.jpg"
}
```
