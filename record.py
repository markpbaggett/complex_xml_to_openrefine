import collections
import json
from lxml import etree
import csv
import os
import xmltodict
from xml.parsers.expat import ExpatError


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

    def determine_export_format(self, delimiter="|"):
        if self.export_format == "xml":
            self.convert_to_xml()
        elif self.export_format == 'csv':
            self.create_csv(delimiter)
        else:
            self.jsonize()

    def create_csv(self, delimiter):
        to_csv = self.results
        keys = []
        for x in to_csv:
            for k, v in x.items():
                if k not in keys:
                    keys.append(k)
        keys = sorted(keys)
        with open(self.output_name, 'w') as output_file:
            dict_writer = csv.writer(output_file, delimiter=delimiter)
            dict_writer.writerow(keys)
            i = 0
            for x in to_csv:
                x = dict(x)
                keys_in_x = []
                for k, v in x.items():
                    keys_in_x.append(k)
                new_dict = {}
                for y in keys:
                    if y not in keys_in_x:
                        new_dict[y] = "    "
                    else:
                        new_dict[y] = x[y]
                my_row = []
                for k, v in new_dict.items():
                    v = v.replace("\n", " ")
                    my_row.append(v)
                dict_writer.writerow(my_row)
                i += 1


class Batch:
    def __init__(self, directory):
        self.path_to_files = directory
        self.total_number_of_records = 0
        self.records = []

    def build(self):
        for x in os.walk(self.path_to_files):
            x = list(x)
            current_path = ""
            for y in x:
                if type(y) is str:
                    current_path = y
                if type(y) is list and len(y) > 0:
                    for potential_record in y:
                        if potential_record.endswith(".xml"):
                            path_to_potential_record = "{}/{}".format(current_path, potential_record)
                            self.add_record(path_to_potential_record)

    def add_record(self, record):
        filename = record.split("/")[-1]
        with open(record, 'r') as file:
            read = file.read()
            try:
                clean = remove_bad_stuff(read)
                json_string = json.dumps(xmltodict.parse(clean))
                real_json = json.loads(json_string)
                real_json["filename"] = filename
                self.records.append(real_json)
                self.total_number_of_records += 1
            except ExpatError:
                print(record)


def escape_keys(key):
    key = key.replace('@', "_AT_")
    key = key.replace('#', "_HASH_")
    key = key.replace(':', "_COLON_")
    return key


def remove_bad_stuff(some_bytes):
    good_string = some_bytes.replace(u'\u000B', u'')
    good_string = good_string.replace(u'\u000C', u'')
    good_bytes = good_string.encode("utf-8")
    return good_bytes
