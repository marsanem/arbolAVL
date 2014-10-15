class Avl:
    original = []
    current = []
    lstSorted = []
    
    def __init__(self, unordered_list):
        self.original = unordered_list

    def question(self):
        self.current.append(self.original.pop(0))
        self.current.append(self.original.pop(0))
        return "Que prefieres '{}' o '{}'?".format(self.current[0], self.current[1])

    def insert(self, resp):
        self.lstSorted.append(resp)

    def answer(self, resp):
        self.insert(resp)

    def sorted(self):
        return ', '.join(self.lstSorted)
