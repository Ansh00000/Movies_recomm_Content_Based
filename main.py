from res.imports import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# fetching datasets from kagel site.
movies = dc.Data.get_data("res/tmdb_5000_movies.csv")
credits = dc.Data.get_data("res/tmdb_5000_credits.csv")

# merging the 2 datasets based on title
movies = movies.merge(credits, on='title')

# picking the essentials which can be useful in recommending like
# genres , id , keyword , title, overview, cast, crew
movies = movies[['genres', 'id', 'keywords', 'title', 'overview', 'cast', 'crew']]

# checking missing data in selected attributes
# print(movies.isnull().sum())

# dropping the missing fields as they are very less <5
movies.dropna(inplace=True)
# print(movies.isnull().sum())

# checking duplicate attributes
# print(movies.duplicated().sum())

# Bringing all the genres under one title
# since the data is stored in a dictionary of list inside a string , we have to get rid of string, i.e using ast module.
movies['genres'] = movies['genres'].apply(fnc.Convert_data.convert)
# print(movies['genres'])
movies['keywords'] = movies['keywords'].apply(fnc.Convert_data.convert)
# print(movies['keywords'])
movies['cast'] = movies['cast'].apply(fnc.Convert_data.convert5)
# print(movies['cast'].head(1).values)
movies['crew'] = movies['crew'].apply(fnc.Convert_data.find_director)
# print(movies['crew'])
movies['overview'] = movies['overview'].apply(lambda x: x.split())
# print(movies['overview'])

# removing extra spaces from names, places,attributes to avoid ambiguity
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
# print(movies.head(100))

# merging database's genres,overview,keyword,cast,crew under 1 single attribute of 'tags'
movies['tags'] = movies['genres'] + movies['overview'] + movies['keywords'] + movies['cast'] + movies['crew']

# creating new merged database
db = movies[['id', 'title', 'tags']]
# print(db.info)

# joining back all the words into a single paragraph
db['tags'] = db['tags'].apply(lambda x: " ".join(x))
# print(db['tags'][0])

# converting all the words of 'tags' in lower case to avoid any case sensitiveness
db['tags'] = db['tags'].apply(lambda x: x.lower())
# print(db['tags'][0])

# using countvectorizer to creat a vector of 5000 words excluding words like to,go,in,and,are which do no contribute
# in recommendation from our 'tags' list
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(db['tags']).toarray()
# print(vectors[0])
# print(cv.get_feature_names_out())

# applying stemming to get rid of similar words
ps = PorterStemmer()

# stemming the tags to avoid look alike words like action,actions and actor,actors , etc
db['tags'] = db['tags'].apply(fnc.Convert_data.stem)
# print(db['tags'])

# using Cosine_similarity function to calculate cosine angle of each movie with another and store result in similarity
similarity = cosine_similarity(vectors)


# function to recommend movies related to choice , choosing the closest cosine_similarity for finding of related movies.
def recommend(movie):

    movie_index = db[db['title'] == movie].index[0]
    distances = similarity[movie_index]

    # sorting the cosine_score to get top 5 movies with same 'tags'
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # showing the movies title based on cosine_score
    for i in movie_list:
        print(db.iloc[i[0]].title)


# recommending movies based on specific type of movie from the list of data for example : batman, avatar ,etc
recommend('Batman')
recommend('Avatar')