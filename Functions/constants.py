collection = {
    "Movies": "moviesList",
    "TvShows": "ShowsList",
    "LiveTv": "botallenPlaylist",
    "TvEpisodes": "episodeList",
    "WebShows": "showOnWeb",
    "WebEpisodes": "webEpisodes",
}
playLinkKeys = {
    "Movies": "moviePlayLink",
    "LiveTv": "urlId",
    "TvEpisodes": "episodeUrl",
    "WebEpisodes" : "webEpisodePlayLink"
}

ottPlatformKeys = {
    "Movies": "moviePlatform",
    "TvShows": "channelName",
    "TvEpisodes": "channelName",
    "WebShows": "ottPlatform",
}

searchFieldKeys = {"Movies": "movieName", "TvShows": "showName", 'WebShows' : 'seriesName'}

excludePlayLink = {
    collection["LiveTv"]: "urlId",
    collection["Movies"]: "moviePlayLink",
    collection["TvEpisodes"]: "episodeUrl",
    collection["WebEpisodes"]: "webEpisodePlayLink",
}
