class DataObj:
    def create(self, item):
        self.data = self.db.create(item)
        self.key = self.data.key
        return self

    def insert(self, key, item):
        self.key = key
        self.data = self.db.insert(key, item)
        return self

    def load(self, key):
        self.key = key
        self.data = self.db.get(key)
        # print("Load",self.data,flush=True)
        return self

    def get(self):
        return self.data

    def get_key(self, key):
        self.data = self.db.get(key)
        # print("Load",self.data,flush=True)
        return self.data

    def delete(self):
        self.db.delete(self.key)

    def update(self, changes):
        # print(".............Load................:",self.key,flush=True)
        self.data = self.db.update(self.key, changes)
        return self