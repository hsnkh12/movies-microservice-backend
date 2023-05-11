


class DB:

    def __init__(self, conn):
        self.conn = conn
        self.collection = conn.collection("movies")

    def insertNewMovie(self,data):

        try:
            self.collection.document(data["title"]).set(data)

        except Exception as err:
            print(f"DATABASE ERROR: {err}")
            return False

        print(f"'{data['title']}' added to database")
        return True
        
        

    def doesMovieExist(self,title):

        doc = self.collection.document(title).get()

        if doc.exists:
            print(f"'{title}' already exists")
            return True
        return False



    