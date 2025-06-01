import os
import pymongo

get_path = os.path.dirname(__file__)
print(get_path)
mongo_client = pymongo.MongoClient("mongodb+srv://alham0046:alham789@cluster0.odsdwox.mongodb.net")
mydatadb = mongo_client["Hometheater"]
mycoll = mydatadb["ShowsList"]
for shownames in mycoll.find():
    showname = shownames["showName"]
    folders = ["moviesLogo", "moviesPoster"]
    # print(shownames["showName"])
    if showname != "10:29 Ki Aakhri Dastak":
        for folder in folders:
            filePath = os.path.join(get_path, folder, showname)
            os.makedirs(filePath)