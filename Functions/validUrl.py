from Functions.soupObject import soupObject
from typing import TypedDict, Optional, NotRequired, Union

def validateUrl(url, headers = None):
    soup_obj_args = {'url' : url, 'rawResponse' : True}
    if headers is not None:
        soup_obj_args['headers'] = headers
    response = soupObject(**soup_obj_args)
    status = response.status_code
    elapsedTime = response.elapsed.total_seconds()
    # print('elapsed is', elapsedTime)

    if status==200 and elapsedTime < 2:
        return True
    else:
        return False
    
# valid = validateUrl('https://www.yodesitv.cc/')
# print(valid)

#### From Chat GPT and is working perfectly fine
def is_video_link_working(videoObject):
    url = videoObject.get('playlink')
    videoHeaders = videoObject.get('headers', None)
# try:
    # Make a HEAD request to check if the server supports range requests
    headers = {"Range": "bytes=0-1"}
    if videoHeaders:
        headers = {**headers, **videoHeaders}
    response = soupObject(url=url, checkLinkValidity=True, headers=headers, stream=True)
    # response = requests.get(url, headers=headers, stream=True, timeout=10)
    # Check for status code and Content-Type header
    if response.status_code in (200, 206):  # 206 indicates partial content
        content_type = response.headers.get("Content-Type", "").lower()
        if "video" in content_type:
            print("The video link is valid and starts streaming.")
            return True
        else:
            print("The link is valid, but it does not seem to be a video.")
            return False
    else:
        print(f"Failed with status code: {response.status_code}")
        return False
# except requests.RequestException as e:
#     print(f"Error checking video link: {e}")
#     return False