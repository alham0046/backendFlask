def pipeLineQuery(platforms, limit, exclusion, category):
    # sort_by_platform =
    if category == "moviesList":
        MoviePipeline = [
            {
                "$match": {
                    "moviePlatform": {"$in": platforms},
                    # "movieReleaseDate": {"$gt": "2024-08-01"},
                }
            },  # Filter movies by platform
            {"$sort": {"movieReleaseDate": -1}},  # Sort by release date (latest first)
            {"$project": exclusion},  # Exclude 'moviePlayLink' field
            {
                "$group": {
                    "_id": "$moviePlatform",
                    "latestMovies": {
                        "$push": "$$ROOT"
                    },  # Store all movies in an array per platform
                }
            },
            {
                "$project": {
                    # "_id": 1,
                    "platform": "$_id",
                    "latestMovies": {
                        "$slice": ["$latestMovies", limit]
                    },  # Limit to 10 movies per platform
                }
            },
            {
                "$addFields": {"sortOrder": {"$indexOfArray": [platforms, "$platform"]}}
            },  # Assign an index based on the predefined platforms order
            {"$sort": {"sortOrder": 1}},  # Sort by this index
            {"$project": {"sortOrder": 0}},  # Remove the extra field
        ]
        return MoviePipeline
    elif category == "showOnWeb":
        MoviePipeline = [
            {
                "$match": {
                    "ottPlatform": {"$in": platforms},
                    # "movieReleaseDate": {"$gt": "2024-08-01"},
                }
            },  # Filter movies by platform
            {"$sort": {"lastSeasonAiringDate": -1}},  # Sort by release date (latest first)
            # {"$project": exclusion},  # Exclude 'moviePlayLink' field
            {
                "$group": {
                    "_id": "$ottPlatform",
                    "latestWebShows": {
                        "$push": "$$ROOT"
                    },  # Store all movies in an array per platform
                }
            },
            {
                "$project": {
                    # "_id": 1,
                    "platform": "$_id",
                    "latestWebShows": {
                        "$slice": ["$latestWebShows", limit]
                    },  # Limit to 10 movies per platform
                }
            },
            {
                "$addFields": {"sortOrder": {"$indexOfArray": [platforms, "$platform"]}}
            },  # Assign an index based on the predefined platforms order
            {"$sort": {"sortOrder": 1}},  # Sort by this index
            {"$project": {"sortOrder": 0}},  # Remove the extra field
        ]
        return MoviePipeline
    elif category == "ShowsList":
        TvShowPipeline = [
            {
                "$match": {"channelName": {"$in": platforms}, "showStatus": "Airing"}
            },  # Filter movies by platform
            {"$project": exclusion},  # Exclude 'moviePlayLink' field
            {
                "$group": {
                    "_id": "$channelName",
                    "latestTvShows": {
                        "$push": "$$ROOT"
                    },  # Store all movies in an array per platform
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "platform": "$_id",
                    "latestTvShows": "$latestTvShows",  # Store all movies in an array per platform
                }
            },
            {
                "$addFields": {"sortOrder": {"$indexOfArray": [platforms, "$platform"]}}
            },  # Assign an index based on the predefined platforms order
            {"$sort": {"sortOrder": 1}},  # Sort by this index
            {"$project": {"sortOrder": 0}},  # Remove the extra field
        ]
        # print(TvShowPipeline)
        return TvShowPipeline


# pipeline = [
#     {"$group": {
#         "_id": "$moviePlatform",
#         "movies": {"$push": "$$ROOT"}
#     }},
#     {"$unset": "movies._id"},
#     {"$project": {
#         "_id": 0,
#         "moviePlatform": "$_id",
#         "movies": {"$slice": ["$movies", 10]}
#     }}
# ]

# def pipeLineQuery(platforms, limit, exclusion, category):
#     if category == "Movies":
#         query_filter = {
#             "moviePlatform": {"$in": platforms},
#             "movieReleaseDate": {"$gt": "2024-08-01"},
#         }
#         sortby = "movieReleaseDate"
#     pipeline = [
#         {"$match": query_filter},  # Filter movies by platform
#         {"$sort": {sortby: -1}},  # Sort by release date (latest first)
#         {"$project": exclusion},  # Exclude 'moviePlayLink' field
#         {
#             "$group": {
#                 "_id": "$moviePlatform",
#                 "latestMovies": {
#                     "$push": "$$ROOT"
#                 },  # Store all movies in an array per platform
#             }
#         },
#         # {
#         #     "$project": {
#         #         "_id": 1,
#         #         "latestMovies": {
#         #             "$slice": ["$latestMovies", limit]
#         #         },  # Limit to 10 movies per platform
#         #     }
#         # },
#     ]
#     return pipeline
