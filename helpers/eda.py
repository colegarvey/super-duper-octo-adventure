import pandas as pd

class EDA:
    def __init__(self, path):
        self.data = pd.read_csv(path)
    
    def get_data(self):
        return self.data

    def head(self, n=5):
        return self.data.head(n)