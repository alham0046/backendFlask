from resolveurl.urlResolver import findHostandMediaId, resolveUrl
from urllib.parse import quote

def getLink(url):
    if isinstance(url, dict):
        return resolveUrl(**url)
    elif isinstance(url, str):
        return findHostandMediaId(url)

def getVideoLink(db, videoUrl, validPlayLink):
    if isinstance(videoUrl, str) and 'gofile' in videoUrl:
        playLinkCheck = getLink(videoUrl)
        if playLinkCheck:
            validPlayLink.update(playLinkCheck)
            validPlayLink.update({'status' : True})
    elif isinstance(videoUrl, str) and ('.mp4' in videoUrl or '.mkv' in videoUrl or 'pixeldra' in videoUrl):
        # videoUrlStatus = validateUrl(videoUrl)
        validPlayLink.update({'playlink':quote(videoUrl, safe=":/?"), 'status' : True})
        print('entering video 1', validPlayLink)
        # validPlayLink = {'playlink':videoUrl}
    elif isinstance(videoUrl, list):
        print('entering video 2')
        # playLinkCheck = next((getLink(url) for url in videoUrl), None)
        playLinkCheck = next((getLink(url) for url in videoUrl if url.get('mediaId')), None)
        if playLinkCheck:
            validPlayLink.update(playLinkCheck)
            validPlayLink.update({'status' : True})
    elif isinstance(videoUrl, str) :
        print('inside isdigit', videoUrl)
        urlId = list(db['botallenPlaylist'].find({'urlId' : videoUrl}, {'_id' : 0, 'urlId' : 1}))
        botallenLink = f"https://botallen.live/live/346016/057944/{urlId[0]['urlId']}.m3u8"
        validPlayLink.update({'playlink':botallenLink, 'status' : True})
    return validPlayLink
    # print('playlink is', validPlayLink)