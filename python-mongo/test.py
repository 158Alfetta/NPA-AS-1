import json
from mongoengine import connect,Document, ListField, StringField, URLField,EmbeddedDocument,EmbeddedDocumentListField
with open('output.txt') as json_file:
    data = json.load(json_file)
# print(data["gathered"])
print(json.dumps(data["gathered"]["gathered"], indent=4, sort_keys=True))
connect(db="nettysight", host="localhost", port=27017)

class Interface (EmbeddedDocument):
    ip_address  = StringField()
    name = StringField()
    vlan = StringField()
    oper_status = StringField()

class Devices(EmbeddedDocument):
    device_id = StringField()

class Config(Document):
     hostname = StringField(required=True)
     interfaces  = EmbeddedDocumentListField(Interface)

class Device(Document):
    username = StringField()
    password = StringField()
    ip_address = StringField()
    device_type = StringField()

class Group(Document):
    name = StringField()
    devices = EmbeddedDocumentListField(Devices)

config = Config(
    hostname="test",
    interfaces =[{"ip_address":"a","name":"as","vlan":"1","oper_status":"asd"},
    {"ip_address":"b","name":"as","vlan":"1","oper_status":"asd"}],
)
device = Device(
    username = "test",
    password = "test",
    ip_address = "1.1.1.1",
    device_type = "cisco"
)
group = Group(
    name = "test",
    devices = [{"device_id":"tes1"},{"device_id":"test2"}]
)
print(config.save())
print(device.save())
print(group.save())

'''
device
+username
+password
+ip_address
+device_type'''
'''
group
+ name
+ devices
device_id

'''