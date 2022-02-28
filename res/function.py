import ast
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# ast.literal_eval() converts a string into list,tuple,set.
class Convert_data:

    @staticmethod
    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    @staticmethod
    def convert5(obj):
        L = []
        count =0
        for i in ast.literal_eval(obj):
            if count != 5:
                L.append(i['name'])
                count = count+1
        return L

    @staticmethod
    def find_director(obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L

    @staticmethod
    def stem(text):
        y = []

        for i in text.split():
            y.append(ps.stem(i))

        return " ".join(y)

    @staticmethod
    def lower(text):
        y = []
        for i in text:
            y.append(i.lower())
        return y

    @staticmethod
    def join(text):
        y = []
        for i in text:
            y.append(" ".join(i))

        return y

    # @staticmethod
    # def recommend(movie):
    #     movie_index = db[db['title'] == movie].index[0]
    #     distances = similarity[movie_index]
    #     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    #
    #     for i in movie_list:
    #        print(i[0])




