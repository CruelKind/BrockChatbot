var MongoClient = require('mongodb').MongoClient;
var url = 'mongodb+srv://dbUser:Cosc4P01@chatbot.lorgj.mongodb.net/test';


function query(datab, name, collects, type){

  var query = {};
  query[type] = name


  MongoClient.connect(url, function(err, db) {
      if (err) throw err;
      var dbo = db.db(datab);
      dbo.collection(collects).find(query).toArray(function(err, result) {
      if (err) throw err;
      console.log(result);
      db.close();
      });
  });

}

query("SummerGames", "British Columbia", "athletes", "cont")



