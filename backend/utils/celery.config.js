const dotenv = require('dotenv');
const amqp = require('amqplib');
dotenv.config();

class Celrey{

    connect = async () => {
        const connection = await amqp.connect('amqps://jqdjczml:wVihh1Yey_UtdpuEdxC-Bjef2kcxhzRu@hummingbird.rmq.cloudamqp.com/jqdjczml');
        this.channel = await connection.createChannel();
    }
}

const celery = new Celrey()

const init = async () => {

    await celery.connect()

}  



module.exports.init = init
module.exports.celery = celery