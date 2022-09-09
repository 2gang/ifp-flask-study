from marshmallow import Schema, fields
from serialization import Stingray
import json

'''
어떤 데이터가 json 으로 들어왔고,
json.dumps(어떤 데이터) 를 통해서 <class dict> 가 되었다고 가정
'''

JSON_개_데이터 = {
    "name" : "common_stingray",
    "age" : "3",
    "size" : "14cm",
    "weight" : "2.3kg",
    "place_of_birth" : "Germany"
} 

#Schema 정의
class StingraySchema(Schema):
    name = fields.String()
    age = fields.String()
    size = fields.String()
    weight = fields.String()
    place_of_birth = fields.String()
    
개정보_변환기 = StingraySchema()

data = 개정보_변환기.load(JSON_개_데이터)
Stingray_객체 = Stingray(**data)

print(Stingray_객체)