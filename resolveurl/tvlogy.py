"""
    Plugin for ResolveURL
    Copyright (C) 2016 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import random
import json
from six.moves import urllib_parse
from resolveurl.net import Net
# from net import Net
import requests



class tvlogy:
    name = 'TVLogy'
    domains = ['tvlogy.to']
    net = Net()
    FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
    pattern = r'(?://|\.)((?:hls\.|flow\.)?tvlogy\.to)/(?:embed/|watch\.php\?v=|player/index.php\?data=)?([0-9a-zA-Z/]+)'
    def get_media_url(self, host, media_id):
        embeds = ['http://bestarticles.me/', 'http://tellygossips.net/', 'http://tvarticles.org/']
        # web_url = "https://hls.tvlogy.to/player/index.php?data=ef73ec53114d6a24308544f5e70cb8ca&do=getVideo"
        web_url = f'https://{host}/player/index.php?data={media_id}&do=getVideo'
        headers = {'User-Agent': self.FF_USER_AGENT}
        if 'hls.' in web_url:
            headers.update({'X-Requested-With': 'XMLHttpRequest'})
            pdata = {'hash': media_id,
                     'r': 'https://{0}/'.format(host)}
            resp = json.loads(self.net.http_POST(web_url, form_data=pdata, headers=headers).content)
            str_url = resp.get('videoSource')
            if str_url:
                headers.pop('X-Requested-With')
                return str_url + '|%s' % '&'.join(['%s=%s' % (key, urllib_parse.quote_plus(headers[key])) for key in headers])
    def get_host_and_id(self, url):
        """
        The method that converts a host and media_id into a valid url

        Args:
            url (str): a valid url on the host this resolver resolves

        Returns:
            host (str): the host the link is on
            media_id (str): the media_id the can be returned by get_host_and_id
        """
        r = re.search(self.pattern, url, re.I)
        if r:
            print("the r is", r)
            print("the r group is", r.groups())
            return r.groups()
        else:
            return False
    def refineTvlogyUrl(self, TvlogyUrl):
        url, headers = TvlogyUrl.split('|')
        headers = {
            "User-Agent": headers.split('=')[1]
        }
        print(headers)
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            videoLink = response.text.splitlines()[-1]
            if requests.get(videoLink, headers=headers).status_code == 200:
                return videoLink
            else:
                return False
        else:
            print(f"Failed to access the URL, status code: {response.status_code}")
            return False
        


# tvlogyInstance = tvlogy()
# (host, id) = tvlogyInstance.get_host_and_id("https://hls.tvlogy.to/player/index.php?data=05b4defdee45c6f2a4307c7392d9193d")
# getsomething = tvlogyInstance.get_media_url(host=host, media_id=id)
# playUrl = tvlogyInstance.refineTvlogyUrl(TvlogyUrl=getsomething)
# print(playUrl)

# print(hostandid)