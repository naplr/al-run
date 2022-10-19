import pickle

def read_problems():
    study = pickle.load(open('../../data/alg-study.pkl', 'rb'))
    post = pickle.load(open('../../data/alg-post.pkl', 'rb'))
    return study, post
