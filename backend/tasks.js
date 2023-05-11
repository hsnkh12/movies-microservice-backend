const amqp = require('amqplib');
const dotenv = require('dotenv');
const { celery } = require('./utils/celery.config')
dotenv.config();

async function delayQueuedTask(category) {

  const queueName = 'celery';
  const taskName = "app.celery.scrapNewMovies"

  const headers = {
    'task': taskName,
    'id': category,
    'lang': 'py',
    'argsrepr': '',
    'kwargsrepr': '{}'
  }

  const body = {
    args: [],
    kwargs:{'category': category}
  }

  const options = {
    headers:headers, 
    contentType:'application/json', 
    contentEncoding:'utf-8',
    deliveryMode: 2

  }
  await celery.channel.assertQueue(queueName);
  await celery.channel.publish('',queueName, Buffer.from(JSON.stringify(body)), options);

}
  
module.exports = {delayQueuedTask}

