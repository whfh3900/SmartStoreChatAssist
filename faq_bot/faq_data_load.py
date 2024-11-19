import pickle

def load_faq_data(filepath):
    with open(filepath, 'rb') as file:
        faq_data = pickle.load(file)
    return faq_data
