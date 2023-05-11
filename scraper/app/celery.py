from . import app
from .scraper import MovieScraper

# celery -A app.celery worker  --loglevel info

@app.task(serializer='json')
def scrapNewMovies(category):

    print(f"Task recieved for scraping '{category}'")

    # Scrap movies for a specifc category starting from page 1 to page 5, and store them in db
    scraper = MovieScraper(category=category, page_s=1, page_e=5, store_in_db=True, threads=8)
    scraper.scrap()
    return True




