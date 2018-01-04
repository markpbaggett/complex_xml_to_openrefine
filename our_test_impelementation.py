import xmltodict
import json
from record import Record

file = open("test.xml", 'r')
read = file.read()
json_string = json.dumps(xmltodict.parse(read))
real_json = json.loads(json_string)
our_list_of_records = real_json['modsCollection']['mods']
results = []
for each_record in our_list_of_records:
    current_record = Record(each_record)
    results.append(current_record.split())
output = open("temp.json", 'w')
our_data = str(results)
output.write(our_data)
output.close()
