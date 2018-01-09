import collections
import json
from lxml import etree


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
                self.payload.update({k: v})
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
                self.ordered_payload.update({k: v})
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

    def jsonize(self):
        json_string = json.dumps(self.ordered_payload)
        return collections.OrderedDict(json.loads(json_string))


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
                    key = "{}.{}.{}".format(self.path, k, i)
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


class RecordCollection:
    def __init__(self, name, export_format="json", number_of_records=0):
        self.total_records = number_of_records
        self.results = []
        self.output_name = name
        self.output_type = "xml"
        self.export_format = export_format

    def __str__(self):
        return "This record set includes {} records.".format(self.total_records)

    def add_record(self, new_record):
        self.total_records += 1
        self.results.append(new_record)

    def jsonize(self):
        file = open(self.output_name, 'w')
        file.write(json.dumps(self.results))
        file.close()

    def convert_to_xml(self):
        record = etree.Element('openrefine')
        document = etree.ElementTree(record)
        for x in self.results:
            new_record = etree.SubElement(record, 'record')
            for k, v in x.items():
                key = escape_keys(k)
                new_element = etree.SubElement(new_record, key)
                new_element.text = v
        file = open(self.output_name, 'wb')
        document.write(file)
        file.close()

    def determine_export_format(self):
        if self.export_format == "xml":
            self.convert_to_xml()
        else:
            self.jsonize()


def escape_keys(key):
    key = key.replace('@', "_AT_")
    key = key.replace('#', "_HASH_")
    key = key.replace(':', "_COLON_")
    return key
