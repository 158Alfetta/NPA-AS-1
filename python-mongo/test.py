import json
from mongoengine import connect,Document, ListField, StringField, URLField, EmbeddedDocument,EmbeddedDocumentListField
# with open('output.txt') as json_file:
#     data = json.load(json_file)
# print(data["gathered"])
# print(json.dumps(data["gathered"]["gathered"], indent=4, sort_keys=True))

con = connect(db="FSWD-TEST-UDOMEAK", host="mongodb+srv://cluster0.szzhk.mongodb.net", port=5001, username='PRioUS', password='@goO(-fW8Hv%', authentication_source='admin')

class Interface(EmbeddedDocument):
    ip_address  = StringField()
    name = StringField()
    vlan = StringField()
    oper_status = StringField()

class Config(Document):
    hostname = StringField(required=True)
    interfaces  = EmbeddedDocumentListField(Interface)

class Devices(Document):
    username = StringField()
    password = StringField()
    ip_address = StringField()
    type = StringField()
    meta = {'strict': False}

for config in Devices.objects:
    print(config.ip_address)
    print(config.username)
    print(config.password)
    print(config.type)