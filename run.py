import xmltodict
import json
from record import Record, RecordCollection
import argparse

argument_parser = argparse.ArgumentParser(description='Use the following to create flat JSON from Complex XML.')
argument_parser.add_argument("-f", "--file", dest="filename",
                             help="Specify path to file to read. Defaults to sample_data/text.xml.", required=False)
argument_parser.add_argument("-x", "--export", dest="export_filename",
                             help="Specify exported JSON filename. Defaults to export.json.")
argument_parser.add_argument("-r", "--root", dest="root_node",
                             help="Specify path to the record root of your collection. Defaults to modsCollection/mods")
argument_parser.add_argument("-xf", "--export_format", dest="export_format", help="Specify the export format."
                                                                                  "Choose xml, csv, or json."
                                                                                  "Defaults to json.")
argument_parser.add_argument("-d", "--delimiter", dest="csv_delimiter", help="Use to specify a delimiter if exporting"
                                                                             "to csv.  Default is |.")
arguments = argument_parser.parse_args()

# Default variables
if arguments.filename:
    filename = arguments.filename
else:
    filename = "sample_data/test.xml"
if arguments.export_filename:
    export_file = arguments.export_filename
else:
    export_file = "export.json"
if arguments.root_node:
    root_node = arguments.root_node
else:
    root_node = "/modsCollection/mods"
if arguments.export_format:
    export_format = arguments.export_format
else:
    export_format = "json"
if arguments.csv_delimiter:
    csv_delimiter = arguments.csv_delimiter
else:
    csv_delimiter = "|"


def convert_root_node(node):
    if node.startswith("/"):
        node = node.replace('/', '', 1)
    path = node.split('/')
    return path


if __name__ == "__main__":
    file = open(filename, 'r')
    read = file.read()
    json_string = json.dumps(xmltodict.parse(read))
    real_json = json.loads(json_string)
    full_path = convert_root_node(root_node)
    real_json_call = real_json
    for x in full_path:
        real_json_call = real_json_call[x]
    our_list_of_records = real_json_call
    results = RecordCollection(export_file, export_format)
    for each_record in our_list_of_records:
        current_record = Record(each_record)
        current_record.ordered_split()
        results.add_record(current_record.jsonize())
    results.determine_export_format(csv_delimiter)
    print("\n\tAdded {} records from {} to {}".format(str(results.total_records), filename, export_file))
