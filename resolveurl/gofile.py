import requests
from urllib.parse import urlencode

# from bs4 import BeautifulSoup

# headers = {
#     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
# }

# def gofileResolver(url):
#     if 'gofile' in url:
#         link = requests.get(url, headers=headers)
#         # soup = BeautifulSoup(link.text, 'html.parser')
#         print(link.content)
#     else :
#         pass

# gofileResolver("https://gofile.io/d/Jm5JVn")

def gofileResolver(mediaId):
    print("the mediaId is", mediaId)
    BASE_API = "https://api.gofile.io"
    BASE_URL = "https://gofile.io"

    # Create an account to get a token
    account_response = requests.post(
        f"{BASE_API}/accounts",
        headers={
            "origin": BASE_URL,
            "referer": f"{BASE_URL}/",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
        },
        json={}  # Body as an empty JSON object
    )

    acc = account_response.json()
    # print(acc)
    token = acc["data"]["token"]

    # Fetch the content using the token
    # query_params = urlencode({"wt": "4fd6sg89d7s6"})
    ## 2) Get website token as query param support is removed. use the below code to get X-Website-Token if below code breaks
    #try:
    #    res = session.get("https://gofile.io/dist/js/config.js", headers=headers)
    #    line = [x for x in res.text.split("\n") if "appdata.wt" in x][0]
    #    website_token = line.split('wt = ')[-1].split('"')[1]
    #except:
    #    website_token = "4fd6sg89d7s6"
    content_response = requests.get(
        f"{BASE_API}/contents/{mediaId}?cache=true",
        headers={
            "origin": BASE_URL,
            "referer": f"{BASE_URL}/",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
            "authorization": f"Bearer {token}",
            "X-Website-Token": "4fd6sg89d7s6",
        },
    )
    content = content_response.json()
    if content["status"] == "ok":
        child = content["data"]["children"]
        first_child = next(iter(child.values()))
        playLink = first_child["link"]
        print(f"got the gofile Link as {playLink} and sending with headers")
        headers: dict[str, str] = {
            "Cookie": f"accountToken={token}",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Referer": BASE_URL,
            "Origin": BASE_URL,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        return {"playlink": playLink, "headers": headers}
    else:
        print("not found")
        return None


# gofileResolver("0Yc9um")

# # header is {'Cookie': 'accountToken=PJE5fldb4iQhPAyHNhuWLLI57etR7C6o', 'Accept-Encoding': 'gzip, deflate, br', 'User-Agent': 'Mozilla/5.0', 'Accept': '*/*', 'Referer': 'https://store5.gofile.io/download/web/fdc0aa09-a394-4bef-80d6-a3e456e73a8e/Advocate%20Anjali%20Awasthi%203rd%20December%202024.mp4/', 'Origin': 'https://store5.gofile.io/download/web/fdc0aa09-a394-4bef-80d6-a3e456e73a8e/Advocate%20Anjali%20Awasthi%203rd%20December%202024.mp4', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}\
# # https://gofile.io/d/0Yc9um
# #  (NOBRIDGE) LOG  the resolved gofile link is {"header": {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Cache-Control": "no-cache", "Connection": "keep-alive", "Cookie": "accountToken=VBfWEW1fzhNT1Gtg8mLTHBODuUelrSMF", "Origin": "https://store8.gofile.io/download/web/a4212d92-a976-49c5-94e1-55bc83dffcd6/Shaitani%20Rasmein%203rd%20December%202024.mp4", "Pragma": "no-cache", "Referer": "https://store8.gofile.io/download/web/a4212d92-a976-49c5-94e1-55bc83dffcd6/Shaitani%20Rasmein%203rd%20December%202024.mp4", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "User-Agent": "Mozilla/5.0"}, "playlink": "https://store8.gofile.io/download/web/a4212d92-a976-49c5-94e1-55bc83dffcd6/Shaitani%20Rasmein%203rd%20December%202024.mp4"}


# import requests

# def get_gofile_direct_link(url: str) -> str:
#     # Extract Content ID
#     content_id = (
#         url.replace("https://", "")
#            .replace("http://", "")
#            .replace("gofile.io/d/", "")
#            .split("/")[0]
#     )

#     session = requests.Session()

#     # 1) Get account token
#     headers = {
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Connection": "keep-alive"
#     }

#     res = session.post("https://api.gofile.io/accounts", headers=headers)
#     token = res.json()["data"]["token"]

#     # 2) Get website token
#     try:
#         res = session.get("https://gofile.io/dist/js/config.js", headers=headers)
#         line = [x for x in res.text.split("\n") if "appdata.wt" in x][0]
#         website_token = line.split('wt = ')[-1].split('"')[1]
#     except:
#         website_token = "4fd6sg89d7s6"

#     # 3) Request content info
#     headers.update({
#         "Authorization": f"Bearer {token}",
#         "X-Website-Token": website_token
#     })

#     res = session.get(f"https://api.gofile.io/contents/{content_id}?cache=true",
#                       headers=headers)

#     data = res.json()["data"]["children"]

#     # Extract first child file info
#     for key, value in data.items():
#         return value["link"]     # Direct download URL

#     raise Exception("No downloadable links found.")

# print(get_gofile_direct_link("https://gofile.io/d/0Yc9um"))
