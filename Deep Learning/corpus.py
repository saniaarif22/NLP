import json

class Corpus:
    def __init__(self, filename):
        with open(filename) as f:
            data = json.load(f)
        self.data = data
        
    @property
    def train(self):
        return self.data['train']

    @property
    def dev(self):
        return self.data['dev']

    @property
    def devtest(self):
        return self.data['devtest']

    @property
    def test(self):
        return self.data['test']

    @property
    def datasets(self):
        return self.train,self.dev,self.devtest,self.test
