const {delayQueuedTask} = require('./tasks');
const express = require("express");
const cors = require('cors');
const {db} = require('./utils/db.config')
const celery = require("./utils/celery.config")
// Initialize Express
const app = express()


app.use(express.json());
app.use(cors({
    origin: '*'
}));

app.get("", async (req, res)=> {

  try{

    const category = req.query.category
    const page = req.query.page

    if ( category == undefined){
      return res.json({"Message":"please provide category name"})
    }
    
    // Queue new task to look for new movies in this category
    await delayQueuedTask(req.query.category)

    const querySnapshot = await db.collection('movies')
    .where("categories", "array-contains", category)
    .orderBy("date_added","desc")
    .orderBy("title")
    .limit(16)
    .offset(page == undefined? 0: page-1)
    .get()

    const movies = querySnapshot.docs.map((doc) => doc.data());
    return res.json(movies)


  } catch( err ){
    console.log(err)
  }
})


app.get("/:movieTitle", async (req, res)=> {

  try{

    const title = req.params.movieTitle

    const doc = await db.collection('movies').doc(title).get()
    return res.json(doc.data())


  } catch( err ){
    console.log(err)
  }

})

celery.init().then(() => {
  app.listen(8000)
}).catch(err => {
  console.log(err)
})
