from xmlrpc.client import boolean
from pymongo import MongoClient
import pymongo
import scrape

## Need to pip install dnspython
CONNECTION_STRING = "mongodb+srv://dbUser:Cosc4P01@chatbot.lorgj.mongodb.net/test"

## STILL NEEDS EDGE CASES

## Establish connection to db.
def getTemplate(template):
    templates = {
        "schedule":{"time":"","sport": "","gender": "","pool": "","location": ""},
        "athlete_sport":{"athlete":"","sport":""}
    }
    return templates[template].copy()


## Provide the mongodb atlas url to connect python to mongodb using pymongo
def get_database():
    try:
        client = MongoClient(CONNECTION_STRING, connect=False)
        print("Connected Successfully.")
    except:
        print("Connection Failed.")
  
    return client["SummerGames"]

## Inserts into specified table. Format should be a list of dictionary.
def insertManyIntoTable(tableName,data):
    db = get_database()
    table = db[tableName]
    
    template = getTemplate(tableName)
    template_keys = list(template.keys())
    input = []
    for i in range(len(data)):
        input.append({j:data[i][template_keys.index(j)] for j in template_keys})

    res = []


    ## keyGen and check

    genderField = False
    
    if ("gender" in input[0]):  genderField = True #If there is a Gender Field in DB
    #for i in range (len(input)):
        
    for i in range(len(input)):

        input[i]["key"]="".join(data[i])

        input[i]["key"] = input[i]["key"].replace (" ","") #Removes spaces from Key

        if genderField: 
            input[i]["gender"] = gender_function(data[i][2]) #if there is a key of Gender -> Simplify gender key field
         
        if checkIfExists(table,input[i]["key"])==False:
            res.append(input[i])


        
    if len(res)>0:
        table.insert_many(res)
        
        #print("inserted "+str(len(res))+" records successfully.")

## Inserts into specified table. Format should be a list.
def insertIntoTable(tableName,data):
    db = get_database()
    table = db[tableName]
    template = getTemplate(tableName)
    template_keys = list(template.keys())

    for i in range(len(template_keys)):
        template[template_keys[i]]=data[i]

    template["key"]="".join(data)
    ## keyGen and check
    if checkIfExists(table,template["key"]):
        table.insert_one(template)

## Return a list of dictionaries in table.
def returnTableData(tableName):
    db = get_database()
    return [i for i in db[tableName].find()]

## Compares key to existing table to check if it exists.
def checkIfExists(table,key):
    if len(list(table.find())) > 0:
        keys = [i["key"] for i in table.find()]
        if key in keys:
            return True
    return False

#Simplifies Gender Key Field into Male, Female, Team Mixed, and Para 
def gender_function (gender):

    male = "Male"
    paramale = "Para Male"
    female = "Female"
    parafemale = "Para Female"
    if paramale in gender:
        return paramale
    elif male in gender:
        return male
    elif parafemale in gender:
        return parafemale
    elif female in gender:
        return female
    else:
        return "Team Mixed"
    

if __name__ == "__main__":
    ## Example use cases:
    
    #insertManyIntoTable("athlete_sport",scrape.scrapeAthleteData_gemspro())
    #returnTableData("athlete_sport")

    #test
    #insertIntoTable("schedule",["1","2","3","4","5"])
    
    
    insertManyIntoTable("schedule",scrape.scrapeSchedule_niagaragames())
    returnTableData("schedule")

    
    pass