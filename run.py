import xmltodict
import json
from record import Record, RecordCollection, Batch
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
argument_parser.add_argument("-i", "--ingest_type", dest="ingest_type", help="Specify batch of file. File is default.")
argument_parser.add_argument("-id", "--ingest_directory", dest="ingest_directory", help="If ingest_type is batch,"
                                                                                        "specify path to "
                                                                                        "ingest_directory.")
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
if arguments.ingest_type == "batch":
    populate = "batch"
else:
    populate = "single file"
if arguments.ingest_directory:
    path_to_files = arguments.ingest_directory
else:
    path_to_files = ""


def convert_root_node(node):
    if node.startswith("/"):
        node = node.replace('/', '', 1)
    path = node.split('/')
    i = 0
    for item in path:
        if item == "":
            path.pop(i)
        i += 1
    return path


if __name__ == "__main__":
    if populate != "batch":
        my_source = filename
        file = open(filename, 'r')
        read = file.read()
        json_string = json.dumps(xmltodict.parse(read))
        real_json = json.loads(json_string)
        full_path = convert_root_node(root_node)
        real_json_call = real_json
        for x in full_path:
            real_json_call = real_json_call[x]
        our_list_of_records = real_json_call
    else:
        my_source = path_to_files
        records = Batch(path_to_files)
        records.build()
        our_list_of_records = records.records
    results = RecordCollection(export_file, export_format)
    for each_record in our_list_of_records:
        current_record = Record(each_record)
        current_record.ordered_split()
        results.add_record(current_record.jsonize())
    results.determine_export_format(csv_delimiter)
    print("\n\tAdded {} records from {} to {}".format(str(results.total_records), my_source, export_file))
    if len(records.errors) > 0:
        print(f"\n\n\tWARNING: {len(records.errors)} errors occurred:\n")
        for error in records.errors:
            print(f"\t{error}")

