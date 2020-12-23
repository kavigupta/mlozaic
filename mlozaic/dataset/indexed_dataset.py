import os

import pickle
import shelve


class IndexedDataset:
    def __init__(self, path):
        self.path = path
        try:
            os.makedirs(self.path)
        except FileExistsError:
            pass
        self.f_data = open(self.path + "/dat", "w+b")
        self.index = shelve.open(self.path + "/ind", "c")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.f_data.close()
        self.index.close()

    def __len__(self):
        return len(self.index)

    def __getitem__(self, idx):
        location = self.index[str(idx)]
        self.f_data.seek(location)
        return pickle.load(self.f_data)

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def append(self, item):
        self.f_data.seek(0, 2)
        self.index[str(len(self))] = self.f_data.tell()
        pickle.dump(item, self.f_data)
