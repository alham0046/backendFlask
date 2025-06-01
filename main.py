from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps  # Import to handle BSON serialization
from flask_cors import CORS
from resolveurl.tvlogy import tvlogy
from datetime import date, timedelta
from resolveurl.vkprime import vkprimeResolve
from collections import defaultdict
# from Functions.queryPipeline import pipeline
from resolveurl.gofile import gofileResolver
from Functions.soupObject import soupObject
from Functions.getVideoLink import getVideoLink
from Functions.validUrl import validateUrl
from resolveurl.urlResolver import resolveUrl, findHostandMediaId
from urllib.parse import parse_qsl
from Functions.constants import collection, playLinkKeys, ottPlatformKeys, searchFieldKeys


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (for testing)
app.config["MONGO_URI"] = "mongodb+srv://alham0046:alham789@cluster0.odsdwox.mongodb.net/Hometheater"
db = PyMongo(app).db


ottList = ["STAR PLUS", "STAR BHARAT", "SONY TV", "ZEE TV", "COLORS", "SAB TV", "HOTSTAR", "NETFLIX", "AMAZON PRIME", "SONYLIV", "ZEE5", "JIOCINEMA"]

def getLink(url):
    if isinstance(url, dict):
        return resolveUrl(**url)
    elif isinstance(url, str):
        return findHostandMediaId(url)

def helperQueryFunction(category):
    if category == 'ShowsList':
        return list(db[category].find({}, {'_id': 0}))
    elif category == 'moviesList' :
        movies = []
        result = list(db[category].aggregate(pipeline))

        # Print the result
        # print(result)
        for platform in result:
            for movie in platform["movies"]:
                movies.append(movie)
        # print(movies)
        return movies
    
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route('/hometheater/cat/<category>', methods = ['POST'])
def get_dbWholeList(category):
    today_date = str(date.today())
    data = request.json
    limit = data.get('limit')
    key = data.get('key')
    value = data.get('value', today_date)
    skip = data.get('skip')

    print('the value is', value)

    sortFilter = {'moviePlatform' : 'movieReleaseDate' }

    query_filter = {key: value} if key and value else {}
    if key == 'channelName':
        query_filter.update({'showStatus' : 'Airing'})

    sortedField = sortFilter.get(key, '$natural')

    query = db[category].find(query_filter, {"_id" : 0}).sort(sortedField, -1)

    print(f"key is {key} and value is {value}")
    if limit:
        query = query.limit(int(limit))

    if skip:
        query = query.skip(int(skip))
    # moviesorshowslist = [moviesorshows for moviesorshows in query]
    # if query:
    moviesorshowslist = list(query)
    return jsonify(moviesorshowslist)


@app.route('/hometheater/catagory/<category>', methods = ['POST'])
def get_List(category):
    today_date = str(date.today())
    data = request.json
    ottNameKey = data.get('ottNameKey')
    dataTitleKey = data.get('dataTitleKey')
    limit = data.get('limit', None)
    query_filter = {}
    airingTodayList = {}
    if category == 'ShowsList' : 
        airingTodayList = db['episodeList'].find({'episodeDate' : today_date}, {'_id' : 0})
        airingTodayList = {episode["showName"] : episode for episode in airingTodayList} if airingTodayList else None
        query_filter.update({"showStatus" : "Airing"})
    
    if category == 'episodeList':
        query_filter.update({ottNameKey : dataTitleKey})
    # Initialize a default dictionary to collect lists of shows for each channel
    dataList = defaultdict(list)

    queryList = helperQueryFunction(category)

    # Loop through each show in the query
    # for show in queryList:
    for show in db[category].find(query_filter, {'_id': 0}):
        ottName = show[ottNameKey]
        dataTitle = show[dataTitleKey]
        # Add the show to the corresponding channel's list in the dictionary
        if ottName in ottList:
            dataList[ottName].append(show)
        if airingTodayList and (dataTitle in airingTodayList.keys()):
            airingTodayList[dataTitle].update({"episodeBackdrop" : show["showBackdrop"], "titleLogo" : show["showTitleLogo"]})  ## write the correct variable from mongo

    ### below is original
    # for show in db[category].find({"showStatus" : "Airing"}, {'_id': 0}):
    #     ottName = show[ottNameKey]
    #     dataTitle = show[dataTitleKey]
    #     # Add the show to the corresponding channel's list in the dictionary
    #     if ottName in ottList:
    #         dataList[ottName].append(show)
    #     if airingTodayList and (dataTitle in airingTodayList.keys()):
    #         airingTodayList[dataTitle].update({"episodeBackdrop" : show["showBackdrop"], "titleLogo" : show["showTitleLogo"]})  ## write the correct variable from mongo
        
    dataList = dict(dataList)
    if category == 'ShowsList' :
        dataList.update({"AIRING TODAY" : list(airingTodayList.values())})

    return jsonify(dataList)

@app.route('/hometheater/catagoryTest/<category>', methods = ['POST'])
def get_List_Test(category):
    today_date = str(date.today())
    data = request.json
    key = data.get('key', None)
    value = data.get('value', None)
    limit = data.get('limit', None)
    addParams = data.get('addParams', None)
    excludePlayLink = {
        'botallenPlaylist' : 'urlId'
    }
    sortKey = data.get('sortkey', None)
    dataList = defaultdict(list)
    airingTodayList = {}
    if addParams:
        addParamsDict = dict(parse_qsl(addParams))
    query_filter = {}
    if (key and value):
        query_filter.update({key : value})
    if category == 'ShowsList':
        query_filter.update({"showStatus" : "Airing"})
        airingTodayList = db['episodeList'].find({'episodeDate' : today_date}, {'_id' : 0})
        airingTodayList = {episode["showName"] : episode for episode in airingTodayList} if airingTodayList else None

    projection = {"_id" : 0}
    if category in excludePlayLink:
        projection[excludePlayLink[category]] = 0
    query = db[category].find(query_filter, projection)
    if category == 'moviesList' and sortKey :
        query.sort(sortKey, -1)
    # query = db[category].find(query_filter, {"_id" : 0})


    # if category == 'episodeList':
    #     query.sort(sortKey, -1)
    #     if limit:
    #         query.limit(int(limit))
    #     moviesorshowslist = list(query)
    #     return jsonify(moviesorshowslist)


    if category == 'ShowsList' or category == 'moviesList':
        chName = addParamsDict.get('ottName')
        showName = addParamsDict.get('showName')
        for mongodata in query:
            dataList[mongodata[chName]].append(mongodata)
            if airingTodayList and mongodata[showName] in airingTodayList.keys():
                airingTodayList[mongodata[showName]].update({"episodeBackdrop" : mongodata["showBackdrop"], "titleLogo" : mongodata["showTitleLogo"]})
        # print(dataList)
        if category == 'moviesList' and limit :
            for channels in dataList:
                dataList.update({channels : dataList[channels][:limit]})

        if airingTodayList:
            dataList.update({"AIRING TODAY" : list(airingTodayList.values())})
        if category == 'botallenPlaylist':
            dataList.update({'Group List' : list(dataList.keys())})
            # dataList['Group List'] = list(dataList.keys())
        return jsonify(dataList)

    # elif category == 'botallenPlaylist':
    #     channelGroup = addParamsDict.get('channelGroup')

    
    else :
        if sortKey:
            query.sort(sortKey, -1)
        if limit:
            query.limit(int(limit))
        moviesorshowslist = list(query)
        return jsonify(moviesorshowslist)
    

@app.route('/hometheater/getWatchingData/<category>', methods = ['POST']) #### used newly for mobile devices
def getWatchingData(category):
    today_date = str(date.today())
    data = request.json
    key = data.get('key', None)
    value = data.get('value', None)
    limit = data.get('limit', None)
    sortKey = data.get('sortkey', None)
    pipeline = data.get('pipeLine', False)
    skip = data.get('skip', None)
    addParams = data.get('addParams', None)
    excludePlayLink = {
        'botallenPlaylist' : 'urlId',
        'moviesList' : 'moviePlayLink',
        'episodeList' : 'episodeUrl',
        'webEpisodes' : "webEpisodePlayLink"
    }
    if addParams:
        addParamsDict = dict(parse_qsl(addParams))
    query_filter = {}
    if (key and value):
        query_filter.update({key : value})
    projection = {}
    if category not in ['showOnWeb', 'showSeason', 'webEpisodes']:
        projection = {"_id" : 0}
    if category in excludePlayLink:
        projection[excludePlayLink[category]] = 0
    if pipeline:
        from Functions.queryPipeline import pipeLineQuery
        pipeline_filter = pipeLineQuery(platforms=value, limit=limit, category=category, exclusion=projection)
        query = db[category].aggregate(pipeline_filter)
    else:
        query = db[category].find(query_filter, projection)
        if skip:
            query.skip(skip)
        # print(list(query))
        if limit:
            query.limit(limit)
        if sortKey:
            query.sort(sortKey, -1)
            
    return jsonify(list(query))

@app.route('/hometheater/searchData', methods = ['POST'])
def searchData():
    data = request.json
    searchText = data.get('searchText')
    searchType = data.get('searchType')
    searchPlatform = data.get('searchPlatform', None)
    title = searchFieldKeys[searchType]
    dbcollection = collection[searchType]
    platform = ottPlatformKeys[searchType] if searchPlatform else None
    projection = {}
    query_filter = {title : {"$regex": searchText, "$options": "i"}}
    if searchPlatform:
        query_filter.update({platform : searchPlatform})
    # print(f'collection is {dbcollection}, platform is {searchPlatform} and text is {searchText} and searchtype is {searchType}')
    if searchType not in ['WebShows', 'WebSeasons', 'WebEpisodes']:
        projection = {"_id" : 0}
    searchResult = db[dbcollection].find(query_filter, projection)
    result_list = list(searchResult)
    # print(result_list)
    return jsonify(result_list)


        
@app.route('/hometheater/userRegistration', methods = ['POST'])
def userDetails():
    ignoreFirstName = ['md', 'mohammad', 'mohommad', 'mohamad', 'mohomad']
    # test = 'alhdfas'.upper()
    data = request.json
    registerData = data.get('userLonginDetails')
    userName, contactNumber, password, emailId = registerData.values()
    userNameList = userName.split(' ')
    firstPart = userNameList[0]
    if firstPart.lower() in ignoreFirstName:
        firstPart = userNameList[1]
    userId = firstPart + contactNumber[-4:]
    checkUser = db['userDetails'].find_one({'contactNumber' : contactNumber})
    if not checkUser:
        userDetail = {
            'userName' : userName,
            'userId' : userId,
            'emailId' : emailId,
            'contactNumber' : contactNumber,
            'subscription' : 'Inactive',
            'subscriptionType' : '',
            'subscriptionDetails' : [],
            'myWatchList' : [{'TvShows' : []}, {'Movies' : []}, {'WebShows' : []}],
            'continueWatching' : [{'TvShows' : []}, {'Movies' : []}, {'WebShows' : []}],
            'watchedMovies' : [],
            'password' : password
        }
        # print(userDetail)
        db['userDetails'].insert_one(userDetail)
        return {'Registration' : 'success', 'comment' : f'welcome {firstPart.upper()} to HomeTheater. ENJOY!!!'}
    else:
        return {'Registration' : 'success', 'comment' : 'Mobile Number Already Exists'}


@app.route('/hometheater/userLogin', methods = ['POST'])
def getLoginDetails():
    data = request.json
    key = data.get('loginType')
    value = data.get('firebaseUserData')
    query = db['userDetails'].find_one({key : value}, {'userId' : 1})
    return {'userId' : query['userId']}


        
    # dataList = dict(dataList)
    # if category == 'ShowsList' :
    #     dataList.update({"AIRING TODAY" : list(airingTodayList.values())})

    # return jsonify(dataList)

@app.route('/hometheater/videoOptions/<collection>', methods = ['POST'])
def videoOptions(collection):
    data = request.json
    key = data.get('key', None)
    value = data.get('value', None)
    limit = data.get('limit', None)
    query_filter = {key : value}
    query = db[collection].find(query_filter, {'_id' : 0})
    if limit:
        query.limit(int(limit))
    return jsonify(list(query))



@app.route('/hometheater/video/resolve', methods = ['POST'])
def resolve_Url():
    # print('i am in')
    data = request.json
    videoUrl = data.get('url')
    if "hls.tvlogy" in videoUrl:
        tvlogyInstance = tvlogy()
        (host, id) = tvlogyInstance.get_host_and_id(videoUrl)
        m3ufile = tvlogyInstance.get_media_url(host=host, media_id=id)
        playUrl = tvlogyInstance.refineTvlogyUrl(TvlogyUrl=m3ufile)
        # print(playUrl)
        return playUrl
    if "vkprime" in videoUrl:
        vkUrl = vkprimeResolve(videoUrl)
        print(vkUrl)
        return vkUrl
    
    if "gofile" in videoUrl:
        vkUrl = findHostandMediaId(videoUrl)
        return vkUrl['playlink']
    
    if isinstance(videoUrl, dict):
        validPlayLink = resolveUrl(**videoUrl)
        print('the playlink is', validPlayLink['playlink'])
        return validPlayLink['playlink']
        # urlForCookie = f'https://multiup.io/{videoUrl['mediaId']}'
        # cookieId = soupObject(url=urlForCookie, cookie=True).cookies.values()[0]
        # multiupLink = f"https://multiup.io/en/mirror/{videoUrl['mediaId']}"
        # headers = {
        #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        #     'Cookie' : f'timezone=Asia/Calcutta; _locale=en; welcome_message_1=true; cf_clearance=4bwh9tWVE_raBsfmpVkZpmnE_ZGNwrCiJnD47EjhNq0-1733284196-1.2.1.1-RDrANoQwgBDuTzVq6cNRVmBDWuraM7jTrrAPt6gKGTdODe4jgVMy.O.WU8wBJK3n8libfa4JSLnPmljYZemyoAWVea.V.draGussdqgdPG0O2qGAwUuvnhYjkjloVPSpnhY6TivdvM8ylsGA.45kv9I.aLEMd.N838Cn5gASWuANihV7zaK8ylzHs7ykl3WzANdnBYjpzPJRe7ScoBZmPkWinlX1wxx1Nvvw2k6QKP3GlobEszEp2pdmhs.FE2hZwmwYvqkwMGFv1sgJiS4bU7R.Tp5E7Dt6Dm_Jf52R4Q.tZ4tUxScSwTI4JaPMdpeRY2V7ymSbfCGgOvSxwn4PGeMyrfX.R9aHpfK4jR13wjQrj30czWowxkd4vo9ax1WRb06kELc8V0wsGPVbzlCm3W3Mhm9sd7tzdGRewZz3vzB1ZK3R07BqBgcNn94iuG7G; PHPSESSID={cookieId}',
        #     # 'Referer' : 'https://multiup.io/en/mirror/8efefd46bf04cc74e57ab64d70821c7d?__cf_chl_tk=UvufR86u7TFZmbMdcZgxK2iaVjqUasMOkkxv3W7u6CI-1733200845-1.0.1.1-zA8dd2UMANEBNr_u9vf_C9Yb_bADSKVyX6__4U6w9kg',
        #     'Origin' : 'https://multiup.io'
        # }
        # print(multiupLink)
        # findGofileLink = soupObject(url=multiupLink, strainer=".mfp-welcome", headers=headers)
        # gofileLink = findGofileLink.select_one('section>header:-soup-contains("Gofile.io")')
        # if gofileLink:
        #     gofileLink = gofileLink.findNextSibling('footer').select_one('a')
        #     gofileLink = gofileLink['href'] if gofileLink['validity'] == 'valid' else None
        #     gofileMediaId = gofileLink.split('/')[-1]
        #     print(gofileMediaId)
        # playUrl, mxheader = gofileResolver(gofileMediaId)
        # return {'playlink' : playUrl, 'header' : mxheader}


@app.route('/hometheater/videoTest/resolve', methods = ['POST'])
def resolve_Url_Test():
    data = request.json
    videoUrl = data.get('url')
    print("video data is", videoUrl)
    validPlayLink = None
    # return {'playlink':url} if validateUrl(url) == True else None
    if isinstance(videoUrl, str) and ('.mp4' in videoUrl or '.mkv' in videoUrl or 'pixeldra' in videoUrl):
        # videoUrlStatus = validateUrl(videoUrl)
        validPlayLink = {'playlink':videoUrl}
    elif isinstance(videoUrl, list):
        validPlayLink = next((getLink(url) for url in videoUrl), None)
    elif isinstance(videoUrl, str) :
        print('inside isdigit')
        urlId = list(db['botallenPlaylist'].find({'tvg-id' : videoUrl}, {'_id' : 0, 'urlId' : 1}))
        print("urlId", urlId[0]['urlId'])
        botallenLink = f"https://botallen.live/live/346016/057944/{urlId[0]['urlId']}.m3u8"
        validPlayLink = {'playlink':botallenLink}
    return validPlayLink
    # if "hls.tvlogy" in videoUrl:
    #     tvlogyInstance = tvlogy()
    #     (host, id) = tvlogyInstance.get_host_and_id(videoUrl)
    #     m3ufile = tvlogyInstance.get_media_url(host=host, media_id=id)
    #     playUrl = tvlogyInstance.refineTvlogyUrl(TvlogyUrl=m3ufile)
    #     # print(playUrl)
    #     return playUrl
    # if "vkprime" in videoUrl:
    #     vkUrl = vkprimeResolve(videoUrl)
    #     print(vkUrl)
    #     return vkUrl
    # if isinstance(videoUrl, dict) and videoUrl['host'] == 'gofile':
    #     urlForCookie = f'https://multiup.io/{videoUrl['mediaId']}'
    #     cookieId = soupObject(url=urlForCookie, cookie=True).cookies.values()[0]
    #     multiupLink = f"https://multiup.io/en/mirror/{videoUrl['mediaId']}"
    #     headers = {
    #         'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    #         'Cookie' : f'timezone=Asia/Calcutta; _locale=en; welcome_message_1=true; cf_clearance=4bwh9tWVE_raBsfmpVkZpmnE_ZGNwrCiJnD47EjhNq0-1733284196-1.2.1.1-RDrANoQwgBDuTzVq6cNRVmBDWuraM7jTrrAPt6gKGTdODe4jgVMy.O.WU8wBJK3n8libfa4JSLnPmljYZemyoAWVea.V.draGussdqgdPG0O2qGAwUuvnhYjkjloVPSpnhY6TivdvM8ylsGA.45kv9I.aLEMd.N838Cn5gASWuANihV7zaK8ylzHs7ykl3WzANdnBYjpzPJRe7ScoBZmPkWinlX1wxx1Nvvw2k6QKP3GlobEszEp2pdmhs.FE2hZwmwYvqkwMGFv1sgJiS4bU7R.Tp5E7Dt6Dm_Jf52R4Q.tZ4tUxScSwTI4JaPMdpeRY2V7ymSbfCGgOvSxwn4PGeMyrfX.R9aHpfK4jR13wjQrj30czWowxkd4vo9ax1WRb06kELc8V0wsGPVbzlCm3W3Mhm9sd7tzdGRewZz3vzB1ZK3R07BqBgcNn94iuG7G; PHPSESSID={cookieId}',
    #         # 'Referer' : 'https://multiup.io/en/mirror/8efefd46bf04cc74e57ab64d70821c7d?__cf_chl_tk=UvufR86u7TFZmbMdcZgxK2iaVjqUasMOkkxv3W7u6CI-1733200845-1.0.1.1-zA8dd2UMANEBNr_u9vf_C9Yb_bADSKVyX6__4U6w9kg',
    #         'Origin' : 'https://multiup.io'
    #     }
    #     print(multiupLink)
    #     findGofileLink = soupObject(url=multiupLink, strainer=".mfp-welcome", headers=headers)
    #     gofileLink = findGofileLink.select_one('section>header:-soup-contains("Gofile.io")')
    #     if gofileLink:
    #         gofileLink = gofileLink.findNextSibling('footer').select_one('a')
    #         gofileLink = gofileLink['href'] if gofileLink['validity'] == 'valid' else None
    #         gofileMediaId = gofileLink.split('/')[-1]
    #         print(gofileMediaId)
    #     playUrl, mxheader = gofileResolver(gofileMediaId)
    #     return {'playlink' : playUrl, 'header' : mxheader}
    
@app.route('/hometheater/getVideoLink', methods = ['POST'])
def get_video_link():
    data = request.json
    userId = data.get('name', None)
    dataType = data.get('dataType', None)
    addParams = data.get('addParams', None)
    query_filter = dict(parse_qsl(addParams))
    validPlayLink = {'status' : False}
    print('the query filter is', query_filter)
    
    print(userId)
    if not userId:
        return validPlayLink
    else:
        subscription, subscriptiontype = db.userDetails.find_one({"userId" : userId}, {"subscription" : 1, "subscriptionType" : 1, "_id" : 0}).values()
        if subscription in ['Admin','Active']:
            playLinkdb = db[collection[dataType]].find_one(query_filter, {"_id" : 0, playLinkKeys[dataType] : 1})
            print('collection', collection[dataType], playLinkdb)
            videoUrl = next(iter(playLinkdb.values()))
            print('the video url is', videoUrl, playLinkdb)
            if videoUrl:
                validPlayLink = getVideoLink(db=db, validPlayLink=validPlayLink, videoUrl=videoUrl)
            else:
                validPlayLink.update({'errorMessage' : 'Video Not Found'})
        else:
            validPlayLink.update({'errorMessage' : 'Not Subscribed. Purchase a valid subscription'})
    print("the validPlayLink is", validPlayLink)
    return validPlayLink
    # return {'playlink' : 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'}


@app.route('/hometheater/getData/<dataType>/<query>', methods = ['POST'])
def getMongodata(dataType, query):
    parseQuery = dict(parse_qsl(query))
    collectionName = parseQuery.get('collectionId')
    findData = parseQuery.get('findData')
    getData = parseQuery.get('getData')
    if dataType == 'mongoData':
        data = db[collectionName].find(findData, )
        


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

##### THIS IS CODE TO EFFICIENTLY FETCH THE MOVIES OR TVSHOWS USING PIPELINE
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
# db = client["your_database_name"]  # Replace with your database name
# collection = db["your_collection_name"]  # Replace with your collection name

# # Define platforms
# platforms = ["HOTSTAR", "SONYLIV", "NETFLIX"]

# # Aggregation pipeline to get 10 latest movies from each platform
# pipeline = [
#     {"$match": {"moviePlatform": {"$in": platforms}}},  # Filter movies by platform
#     {"$sort": {"movieReleaseDate": -1}},  # Sort by release date (latest first)
#     {"$group": {
#         "_id": "$moviePlatform",
#         "latestMovies": {"$push": "$$ROOT"}  # Store all movies in an array per platform
#     }},
#     {"$project": {
#         "_id": 1,
#         "latestMovies": {"$slice": ["$latestMovies", 10]}  # Limit to 10 movies per platform
#     }}
# ]

# # Execute the query
# result = collection.aggregate(pipeline)

# # Print results
# for platform_data in result:
#     print(f"\nPlatform: {platform_data['_id']}")
#     for movie in platform_data["latestMovies"]:
#         print(f"{movie['movieName']} - {movie['movieReleaseDate']}")

    
