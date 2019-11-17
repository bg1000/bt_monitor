import json
message = {
"cmd": "scan", 
"DeviceName": "Bob_Phone", 
"Address": "A0:10:81:64:E7:93"
}
my_json = json.dumps(message)
print(str(my_json))

