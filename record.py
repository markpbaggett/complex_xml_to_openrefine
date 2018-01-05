import collections

class Record:
    def __init__(self, full_record):
        self.record = full_record
        self.payload = {}
        self.ordered_payload = collections.OrderedDict()

    def __str__(self):
        return "{}".format(self.record)

    def split(self):
        for k, v in self.record.items():
            if type(v) is str:
                self.payload.update({k : v})
            elif type(v) is dict:
                dictionary_to_decipher = RecordChunk(v, k)
                x = dictionary_to_decipher.split()
                if x is not None:
                    for item in x:
                        self.payload.update(item)
            elif type(v) is list:
                i = 0
                for thing in v:
                    key = "{}.{}".format(k, i)
                    if type(thing) is str:
                        self.payload.update({key: thing})
                    elif type(thing) is dict:
                        dictionary_to_decipher = RecordChunk(thing, key)
                        x = dictionary_to_decipher.split()
                        if x is not None:
                            for item in x:
                                self.payload.update(item)
                    elif type(thing) is list:
                        print(thing)
                        # this needs to be implemented i think
                    i += 1
        return self.payload

    def ordered_split(self):
        for k, v in self.record.items():
            if type(v) is str:
                self.ordered_payload.update({k : v})
            elif type(v) is dict:
                dictionary_to_decipher = RecordChunk(v, k)
                x = dictionary_to_decipher.split()
                if x is not None:
                    for item in x:
                        self.ordered_payload.update(item)
            elif type(v) is list:
                i = 0
                for thing in v:
                    key = "{}.{}".format(k, i)
                    if type(thing) is str:
                        self.ordered_payload.update({key: thing})
                    elif type(thing) is dict:
                        dictionary_to_decipher = RecordChunk(thing, key)
                        x = dictionary_to_decipher.split()
                        if x is not None:
                            for item in x:
                                self.ordered_payload.update(item)
                    elif type(thing) is list:
                        print(thing)
                        # this needs to be implemented i think
                    i += 1
        return self.ordered_payload



class RecordChunk:
    def __init__(self, data_fragment, current_path=""):
        self.fragment = data_fragment
        self.path = current_path
        self.payload = []

    def __str__(self):
        return "{}".format(self.fragment)

    def type(self):
        return type(self.fragment)

    def split(self):
        for k, v in self.fragment.items():
            if type(v) is str:
                self.payload.append({"{}{}".format(self.path, k): v})
            elif type(v) is dict:
                dictionary_to_decipher = RecordChunk(v, "{}.{}".format(self.path, k))
                x = dictionary_to_decipher.split()
                if x is not None:
                    for item in x:
                        self.payload.append(item)
            elif type(v) is list:
                i = 0
                for thing in v:
                    key = "{}.{}.{}".format(self.path,k, i)
                    if type(thing) is str:
                        self.payload.append({key: thing})
                    elif type(thing) is dict:
                        dictionary_to_decipher = RecordChunk(thing, key)
                        x = dictionary_to_decipher.split()
                        if x is not None:
                            for item in x:
                                self.payload.append(item)
                    elif type(thing) is list:
                        print(thing)
                        # this needs to be implemented?
                    i += 1
        return self.payload


