
class Generator:
    def __init__(self, func):
        self.func = func

    def __iter__(self):
        return Iterator(self)
    
class Iterator:
    def __init__(self, generator):
        self.generator = generator

    def __next__(self):
        

