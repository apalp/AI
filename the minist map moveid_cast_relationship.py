nodes = {
    "nolan":        {"label": "Person", "name": "诺兰",       "born": 1970},
    "interstellar": {"label": "Movie",  "name": "星际穿越",   "year": 2014, "rating": 8.7},
    "matthew":      {"label": "Person", "name": "马修·麦康纳","country": "美国"},
    "scifi":        {"label": "Genre",  "name": "科幻"},
}

# 定义关系（三元组列表）
edges = [
    ("nolan",        "DIRECTED", "interstellar"),
    ("matthew",      "ACTED_IN", "interstellar"),
    ("interstellar", "IN_GENRE", "scifi"),
]

#  查询：诺兰执导了哪些电影？
def query_directed_by(director_id):
    return [
        nodes[target]["name"]
        for src, rel, target in edges
        if src == director_id and rel == "DIRECTED"
    ]

print(query_directed_by("nolan"))  # ['星际穿越']

def query_movie_info(movie_id):
    cast = [nodes[s]["name"] for s, r, t in edges if t== movie_id and r == "ACTED_IN"]
    genres = [nodes[t]["name"] for s, r, t in edges if s == movie_id and r == "IN_GENRE"]
    return {"cast": cast, "genres": genres, **nodes[movie_id]}

print(query_movie_info("interstellar"))
# {'cast': ['马修·麦康纳'], 'genres': ['科幻'], 'label': 'Movie',
#  'name': '星际穿越', 'year': 2014, 'rating': 8.7}
