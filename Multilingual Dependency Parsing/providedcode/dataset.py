from dependencycorpusreader import DependencyCorpusReader
import os

BASE_PATH = '/home/coms4705/Homework2/data/'

def get_swedish_train_corpus():
    root = os.path.join(BASE_PATH, 'swedish/')
    files = ['train.conll']
    return DependencyCorpusReader(root, files)

def get_swedish_dev_corpus():
    root = os.path.join(BASE_PATH, 'swedish/')
    files = ['dev.conll']
    return DependencyCorpusReader(root, files)

def get_swedish_dev_blind_corpus():
    root = os.path.join(BASE_PATH, 'swedish/')
    files = ['dev_blind.conll']
    return DependencyCorpusReader(root, files)

def get_swedish_test_corpus():
    root = os.path.join(BASE_PATH, 'swedish/')
    files = ['test.conll']
    return DependencyCorpusReader(root, files)

def get_swedish_test_blind_corpus():
    root = os.path.join(BASE_PATH, 'swedish/')
    files = ['test_blind.conll']
    return DependencyCorpusReader(root, files)

def get_danish_train_corpus():
    root = os.path.join(BASE_PATH, 'danish/')
    files = ['train.conll']
    return DependencyCorpusReader(root, files)

def get_danish_dev_corpus():
    root = os.path.join(BASE_PATH, 'danish/')
    files = ['dev.conll']
    return DependencyCorpusReader(root, files)

def get_danish_dev_blind_corpus():
    root = os.path.join(BASE_PATH, 'danish/')
    files = ['dev_blind.conll']
    return DependencyCorpusReader(root, files)

def get_danish_test_corpus():
    root = os.path.join(BASE_PATH, 'danish/')
    files = ['test.conll']
    return DependencyCorpusReader(root, files)

def get_danish_test_blind_corpus():
    root = os.path.join(BASE_PATH, 'danish/')
    files = ['test_blind.conll']
    return DependencyCorpusReader(root, files)

def get_english_train_corpus():
    root = os.path.join(BASE_PATH, 'english/')
    files = ['train.conll']
    return DependencyCorpusReader(root, files)

def get_english_dev_corpus():
    root = os.path.join(BASE_PATH, 'english/')
    files = ['dev.conll']
    return DependencyCorpusReader(root, files)

def get_english_dev_blind_corpus():
    root = os.path.join(BASE_PATH, 'english/')
    files = ['dev_blind.conll']
    return DependencyCorpusReader(root, files)

def get_english_test_corpus():
    root = os.path.join(BASE_PATH, 'english/')
    files = ['test.conll']
    return DependencyCorpusReader(root, files)

def get_english_test_blind_corpus():
    root = os.path.join(BASE_PATH, 'english/')
    files = ['test_blind.conll']
    return DependencyCorpusReader(root, files)

def get_korean_train_corpus():
    root = os.path.join(BASE_PATH, 'korean/')
    files = ['train.conll']
    return DependencyCorpusReader(root, files)

def get_korean_dev_corpus():
    root = os.path.join(BASE_PATH, 'korean/')
    files = ['dev.conll']
    return DependencyCorpusReader(root, files)

def get_korean_dev_blind_corpus():
    root = os.path.join(BASE_PATH, 'korean/')
    files = ['dev_blind.conll']
    return DependencyCorpusReader(root, files)

def get_korean_test_corpus():
    root = os.path.join(BASE_PATH, 'korean/')
    files = ['test.conll']
    return DependencyCorpusReader(root, files)

def get_korean_test_blind_corpus():
    root = os.path.join(BASE_PATH, 'korean/')
    files = ['test_blind.conll']
    return DependencyCorpusReader(root, files)
