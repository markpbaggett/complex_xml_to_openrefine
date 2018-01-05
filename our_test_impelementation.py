import xmltodict
import json
from record import Record

file = open("test.xml", 'r')
read = file.read()
json_string = json.dumps(xmltodict.parse(read))
real_json = json.loads(json_string)
our_list_of_records = real_json['modsCollection']['mods']
results = []
i = 1
for each_record in our_list_of_records:
    current_record = Record(each_record)
    record_split = current_record.split()
    json_string = json.dumps(record_split)
    jsonized_record_split = json.loads(json_string)
    results.append(jsonized_record_split)
    i += 1
output = open("temp.json", 'w')
new_our_data = json.dumps(results)
output.write(new_our_data)
output.close()
