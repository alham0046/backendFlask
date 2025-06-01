from resolveurl import gofile, tvlogy, vkprime, qiwi
import re
from Functions.validUrl import validateUrl, is_video_link_working

RESOLVERS = {
    'gofile': gofile.gofileResolver,
    'vkprime': vkprime.vkprimeResolve,
    'qiwi' : qiwi.Qiwigg
    # 'tvlogy': tvlogy  # Assuming tvlogy is callable as is
}

def resolveUrl(host, mediaId):
    if not mediaId:
        return None
    resolver_function = RESOLVERS.get(host)
    getVideoDetail = resolver_function(mediaId)
    # print(f'the host is {host} and mediaId is {mediaId}')
    # if host == 'gofile':
    #     getVideoDetail = gofile.gofileResolver(mediaId)
    # elif host == 'vkprime':
    #     getVideoDetail = vkprime.vkprimeResolve(mediaId)
    # elif host == 'tvlogy':
    #     pass
    if getVideoDetail:
        print("the video detail at backend in urlresolver is",getVideoDetail)
        return getVideoDetail if isinstance(getVideoDetail, dict) else {'playlink' : getVideoDetail}
    else:
        print("video link not found at backend in urlresolver")
        return None

def findHostandMediaId(url:str):
    if ('.mp4' in url or '.mkv' in url):
        return {'playlink':url}
    else:
        ## this regex is for gofile.io and vkprime.com
        regex = r"^(https:\/\/(?P<host>.*)(?:\.com|\.io)\/(?:embed-|d\/)?(?P<mediaId>[a-zA-Z0-9]+)(?:\.html)?)$"
        compare = re.match(regex, url)
        host = compare.group('host')
        mediaId = compare.group('mediaId')
        return resolveUrl(host=host, mediaId=mediaId)
        # print(f'host is {host} and media id is {mediaId}')

# findHostandMediaId('https://vkprime.com/embed-q3z4hz8axkbo.html')
# findHostandMediaId('https://gofile.io/d/X2rFNu')
