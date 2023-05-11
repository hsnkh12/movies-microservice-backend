// Import the functions you need from the SDKs you need
const { initializeApp } = require("firebase-admin/app");
const { getFirestore, Timestamp, FieldValue } = require('firebase-admin/firestore');
var admin = require("firebase-admin");


var serviceAccount = require("../service_account_key.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = getFirestore();
//const db = getDatabase(app);

module.exports = {
    db
}



