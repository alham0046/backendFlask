# from hashlib import sha256
# from time import time

# import requests
# from urllib.parse import urlencode

# # from bs4 import BeautifulSoup

# # headers = {
# #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
# # }

# # def gofileResolver(url):
# #     if 'gofile' in url:
# #         link = requests.get(url, headers=headers)
# #         # soup = BeautifulSoup(link.text, 'html.parser')
# #         print(link.content)
# #     else :
# #         pass

# # gofileResolver("https://gofile.io/d/Jm5JVn")

# userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

# def generate_website_token(account_token: str) -> str:
#     time_slot = int(time()) // 14400
#     raw = f"{userAgent}::en-US::{account_token}::{time_slot}::gf2026x"
#     return sha256(raw.encode()).hexdigest()

# def gofileResolver(mediaId):
#     print("the mediaId is", mediaId)
#     BASE_API = "https://api.gofile.io"
#     BASE_URL = "https://gofile.io"

#     # Create an account to get a token
#     account_response = requests.post(
#         f"https://server3.pd1.workers.dev/accounts",
#         headers={
#             "origin": BASE_URL,
#             "referer": f"{BASE_URL}/",
#             "user-agent": (
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                 "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#             ),
#         },
#         json={}  # Body as an empty JSON object
#     )

#     acc = account_response.json()
#     # print(acc)
#     token = acc["data"]["token"]
    
#     print("the token is", token)
    
#     webToken = generate_website_token(token)

#     # Fetch the content using the token
#     # query_params = urlencode({"wt": "4fd6sg89d7s6"})
#     ## 2) Get website token as query param support is removed. use the below code to get X-Website-Token if below code breaks
#     #try:
#     #    res = session.get("https://gofile.io/dist/js/config.js", headers=headers)
#     #    line = [x for x in res.text.split("\n") if "appdata.wt" in x][0]
#     #    website_token = line.split('wt = ')[-1].split('"')[1]
#     #except:
#     #    website_token = "4fd6sg89d7s6"
#     content_response = requests.get(
#         f"https://server3.pd1.workers.dev/contents/{mediaId}?cache=true&sortField=createTime&sortDirection=1",
#         # f"{BASE_API}/contents/{mediaId}?cache=true",
#         headers={
#             "origin": BASE_URL,
#             "referer": f"{BASE_URL}/",
#             "Cookie": f"accountToken={token}",
#             "user-agent": (
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                 "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#             ),
#             "authorization": f"Bearer {token}",
#             "X-Website-Token": webToken,
#             "X-BL": "en-US"
#         },
#     )
#     content = content_response.json()
#     print("the content is", content)
#     if content["status"] == "ok":
#         child = content["data"]["children"]
#         first_child = next(iter(child.values()))
#         playLink = first_child["link"]
#         print(f"got the gofile Link as {playLink} and sending with headers")
#         headers: dict[str, str] = {
#             "Cookie": f"accountToken={token}",
#             "Accept-Encoding": "gzip, deflate, br",
#             "User-Agent": "Mozilla/5.0",
#             "Accept": "*/*",
#             "Referer": BASE_URL,
#             "Origin": BASE_URL,
#             "Connection": "keep-alive",
#             "Sec-Fetch-Dest": "empty",
#             "Sec-Fetch-Mode": "cors",
#             "Sec-Fetch-Site": "same-site",
#             "Pragma": "no-cache",
#             "Cache-Control": "no-cache",
#         }
#         return {"playlink": playLink, "headers": headers}
#     else:
#         print("not found")
#         return None


# gofileResolver("U9hQo5")

# # # header is {'Cookie': 'accountToken=PJE5fldb4iQhPAyHNhuWLLI57etR7C6o', 'Accept-Encoding': 'gzip, deflate, br', 'User-Agent': 'Mozilla/5.0', 'Accept': '*/*', 'Referer': 'https://store5.gofile.io/download/web/fdc0aa09-a394-4bef-80d6-a3e456e73a8e/Advocate%20Anjali%20Awasthi%203rd%20December%202024.mp4/', 'Origin': 'https://store5.gofile.io/download/web/fdc0aa09-a394-4bef-80d6-a3e456e73a8e/Advocate%20Anjali%20Awasthi%203rd%20December%202024.mp4', 'Connection': 'keep-alive', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}\
# # # https://gofile.io/d/0Yc9um
# # #  (NOBRIDGE) LOG  the resolved gofile link is {"header": {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Cache-Control": "no-cache", "Connection": "keep-alive", "Cookie": "accountToken=VBfWEW1fzhNT1Gtg8mLTHBODuUelrSMF", "Origin": "https://store8.gofile.io/download/web/a4212d92-a976-49c5-94e1-55bc83dffcd6/Shaitani%20Rasmein%203rd%20December%202024.mp4", "Pragma": "no-cache", "Referer": "https://store8.gofile.io/download/web/a4212d92-a976-49c5-94e1-55bc83dffcd6/Shaitani%20Rasmein%203rd%20December%202024.mp4", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "User-Agent": "Mozilla/5.0"}, "playlink": "https://store8.gofile.io/download/web/a4212d92-a976-49c5-94e1-55bc83dffcd6/Shaitani%20Rasmein%203rd%20December%202024.mp4"}


# # import requests

# # def get_gofile_direct_link(url: str) -> str:
# #     # Extract Content ID
# #     content_id = (
# #         url.replace("https://", "")
# #            .replace("http://", "")
# #            .replace("gofile.io/d/", "")
# #            .split("/")[0]
# #     )

# #     session = requests.Session()

# #     # 1) Get account token
# #     headers = {
# #         "Accept": "*/*",
# #         "Accept-Encoding": "gzip, deflate, br",
# #         "Connection": "keep-alive"
# #     }

# #     res = session.post("https://api.gofile.io/accounts", headers=headers)
# #     token = res.json()["data"]["token"]

# #     # 2) Get website token
# #     try:
# #         res = session.get("https://gofile.io/dist/js/config.js", headers=headers)
# #         line = [x for x in res.text.split("\n") if "appdata.wt" in x][0]
# #         website_token = line.split('wt = ')[-1].split('"')[1]
# #     except:
# #         website_token = "4fd6sg89d7s6"

# #     # 3) Request content info
# #     headers.update({
# #         "Authorization": f"Bearer {token}",
# #         "X-Website-Token": website_token
# #     })

# #     res = session.get(f"https://api.gofile.io/contents/{content_id}?cache=true",
# #                       headers=headers)

# #     data = res.json()["data"]["children"]

# #     # Extract first child file info
# #     for key, value in data.items():
# #         return value["link"]     # Direct download URL

# #     raise Exception("No downloadable links found.")

# # print(get_gofile_direct_link("https://gofile.io/d/0Yc9um"))


# import requests
# from hashlib import sha256
# from time import time


# def generate_website_token(user_agent: str, account_token: str) -> str:
#     time_slot = int(time()) // 14400
#     raw = f"{user_agent}::en-US::{account_token}::{time_slot}::gf2026x"
#     return sha256(raw.encode()).hexdigest()


# def get_gofile_link(content_id: str, password: str | None = None):
#     session = requests.Session()
#     user_agent = "Mozilla/5.0"

#     session.headers.update({
#         "Accept-Encoding": "gzip",
#         "User-Agent": user_agent,
#         "Connection": "keep-alive",
#         "Accept": "*/*",
#         "Origin": "https://gofile.io",
#         "Referer": "https://gofile.io/",
#     })

#     try:
#         # Step 1: create temporary account
#         wt = generate_website_token(user_agent, "")

#         acc = session.post(
#             "https://server3.pd1.workers.dev/accounts",
#             headers={"X-Website-Token": wt, "X-BL": "en-US"},
#             timeout=15
#         ).json()

#         if acc.get("status") != "ok":
#             return None

#         token = acc["data"]["token"]

#         session.headers.update({"Authorization": f"Bearer {token}"})
#         session.cookies.set("accountToken", token)

#         # Step 2: fetch content
#         wt2 = generate_website_token(user_agent, token)

#         url = f"https://server3.pd1.workers.dev/contents/{content_id}?cache=true"

#         if password:
#             url += f"&password={sha256(password.encode()).hexdigest()}"

#         res = session.get(
#             url,
#             headers={"X-Website-Token": wt2, "X-BL": "en-US"},
#             timeout=15
#         ).json()

#         if res.get("status") != "ok":
#             return None

#         data = res["data"]

#         # handle file or folder
#         if data["type"] == "folder":
#             for child in data["children"].values():
#                 if child["type"] != "folder":
#                     return child["link"]
#         else:
#             return data["link"]

#     except Exception:
#         return None






# import requests
# from hashlib import sha256
# from time import time


# def _token(ua, acc):
#     slot = int(time()) // 14400
#     raw = f"{ua}::en-US::{acc}::{slot}::gf2026x"
#     return sha256(raw.encode()).hexdigest()


# def get_gofile_stream(content_id, password=None):
#     ua = "Mozilla/5.0"

#     headers = {
#         "User-Agent": ua,
#         "Accept": "*/*",
#         "Origin": "https://gofile.io",
#         "Referer": "https://gofile.io/",
#         "Accept-Encoding": "gzip",
#         "Connection": "keep-alive",
#     }

#     s = requests.Session()
#     s.headers.update(headers)

#     # create temporary account
#     r = s.post(
#         "https://server3.pd1.workers.dev/accounts",
#         headers={"X-Website-Token": _token(ua, ""), "X-BL": "en-US"},
#         timeout=15,
#     ).json()

#     token = r["data"]["token"]

#     s.headers["Authorization"] = f"Bearer {token}"
#     s.cookies.set("accountToken", token)

#     # fetch content
#     url = f"https://server3.pd1.workers.dev/contents/{content_id}?cache=true"
#     if password:
#         url += f"&password={sha256(password.encode()).hexdigest()}"

#     r = s.get(
#         url,
#         headers={"X-Website-Token": _token(ua, token), "X-BL": "en-US"},
#         timeout=15,
#     ).json()

#     data = r["data"]

#     if data["type"] == "folder":
#         for child in data["children"].values():
#             if child["type"] != "folder":
#                 link = child["link"]
#                 break
#     else:
#         link = data["link"]

#     return {
#         "playlink": link,
#         "headers": headers
#     }





import requests
from hashlib import sha256
from time import time


def _token(ua, acc):
    slot = int(time()) // 14400
    raw = f"{ua}::en-US::{acc}::{slot}::gf2026x"
    return sha256(raw.encode()).hexdigest()


def gofileResolver(content_id, password=None):
    ua = "Mozilla/5.0"

    base_headers = {
        "User-Agent": ua,
        "Accept": "*/*",
        "Origin": "https://gofile.io",
        "Referer": "https://gofile.io/",
        "Connection": "keep-alive"
    }

    s = requests.Session()
    s.headers.update(base_headers)

    # create temporary account
    r = s.post(
        "https://server3.pd1.workers.dev/accounts",
        headers={"X-Website-Token": _token(ua, ""), "X-BL": "en-US"},
        timeout=15
    ).json()

    token = r["data"]["token"]

    s.headers["Authorization"] = f"Bearer {token}"
    s.cookies.set("accountToken", token)

    # get content
    url = f"https://server3.pd1.workers.dev/contents/{content_id}?cache=true"

    if password:
        url += f"&password={sha256(password.encode()).hexdigest()}"

    r = s.get(
        url,
        headers={"X-Website-Token": _token(ua, token), "X-BL": "en-US"},
        timeout=15
    ).json()

    data = r["data"]

    if data["type"] == "folder":
        for child in data["children"].values():
            if child["type"] != "folder":
                link = child["link"]
                break
    else:
        link = data["link"]

    headers = {
        "User-Agent": ua,
        "Accept": "*/*",
        "Origin": "https://gofile.io",
        "Referer": "https://gofile.io/",
        "Cookie": f"accountToken={token}"
    }

    return {
        "playlink": link,
        "headers": headers
    }



# import requests
# from hashlib import sha256
# from time import time

# VIDEO_EXT = (".mp4", ".mkv", ".avi", ".mov", ".webm")
# SUB_EXT = (".srt", ".vtt", ".ass", ".ssa")

# IGNORE_WORDS = ("sample", "trailer", "preview")


# def _token(ua, acc):
#     slot = int(time()) // 14400
#     raw = f"{ua}::en-US::{acc}::{slot}::gf2026x"
#     return sha256(raw.encode()).hexdigest()


# def _scan_children(children, videos, subtitles):
#     """
#     Recursively scan gofile folder
#     """

#     for child in children.values():

#         if child["type"] == "folder":
#             if "children" in child:
#                 _scan_children(child["children"], videos, subtitles)
#             continue

#         name = child["name"].lower()

#         if any(word in name for word in IGNORE_WORDS):
#             continue

#         if name.endswith(VIDEO_EXT):
#             videos.append(child)

#         if name.endswith(SUB_EXT):
#             subtitles.append(child)


# def get_gofile_stream(content_id, password=None):

#     ua = "Mozilla/5.0"

#     base_headers = {
#         "User-Agent": ua,
#         "Accept": "*/*",
#         "Origin": "https://gofile.io",
#         "Referer": "https://gofile.io/",
#         "Connection": "keep-alive"
#     }

#     session = requests.Session()
#     session.headers.update(base_headers)

#     # create temporary account
#     r = session.post(
#         "https://server3.pd1.workers.dev/accounts",
#         headers={"X-Website-Token": _token(ua, ""), "X-BL": "en-US"},
#         timeout=15
#     ).json()

#     token = r["data"]["token"]

#     session.headers["Authorization"] = f"Bearer {token}"
#     session.cookies.set("accountToken", token)

#     url = f"https://server3.pd1.workers.dev/contents/{content_id}?cache=true"

#     if password:
#         url += f"&password={sha256(password.encode()).hexdigest()}"

#     r = session.get(
#         url,
#         headers={"X-Website-Token": _token(ua, token), "X-BL": "en-US"},
#         timeout=15
#     ).json()

#     data = r["data"]

#     videos = []
#     subtitles = []

#     if data["type"] == "folder":
#         _scan_children(data["children"], videos, subtitles)
#     else:
#         videos.append(data)

#     # sort videos by size (largest first)
#     videos.sort(key=lambda x: x.get("size", 0), reverse=True)

#     headers = {
#         "User-Agent": ua,
#         "Accept": "*/*",
#         "Origin": "https://gofile.io",
#         "Referer": "https://gofile.io/",
#         "Cookie": f"accountToken={token}"
#     }

#     video_list = [{
#         "name": v["name"],
#         "size": v.get("size"),
#         "url": v["link"]
#     } for v in videos]

#     subtitle_list = [{
#         "name": s["name"],
#         "url": s["link"]
#     } for s in subtitles]

#     return {
#         "videos": video_list,
#         "best_video": video_list[0]["url"] if video_list else None,
#         "subtitles": subtitle_list,
#         "headers": headers
#     }



    
# link = get_gofile_stream("ARznuN")

# print(link)