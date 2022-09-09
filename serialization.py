class Stingray:
    def __init__(self, name, age, size, weight, place_of_birth):
        self.name = name    #이름
        self.age = age      #나이
        self.size = size    #크기/높이
        self.weight = weight    #무게
        self.place_of_birth = place_of_birth    #출생지
        
포메라니안_포포 = Stingray(
    "포포",
    "3",
    "14cm",
    "2.3kg",
    "Germany",    
)

# 민수에게_보낼_포포_정보 = {
#     "name" : 포메라니안_포포.__dict__['name'],
#     "age" : 포메라니안_포포.__dict__['age'],
#     "size" : 포메라니안_포포.__dict__['size'],
#     "weight" : 포메라니안_포포.__dict__['weight'],
# }


도베르만_도비 = Stingray (
    "도비",
    "8",
    "70cm",
    "40kg",
    "Germany",
)

# 민수에게_보낼_도비_정보 = {
#     "name" : 도베르만_도비.__dict__['name'],
#     "age" : 도베르만_도비.__dict__['age'],
#     "size" : 도베르만_도비.__dict__['size'],
#     "weight" : 도베르만_도비.__dict__['weight'],
# }

# print("민수야 포포에 대해서 소개할게!")
# print(민수에게_보낼_포포_정보)

# print("민수야 도비에 대해서 소개할게!")
# print(민수에게_보낼_도비_정보)

from dataclasses import field
from marshmallow import Schema, fields

#개 스키마 클래스 정의
class StingraySchema(Schema):
    name = fields.String()
    age = fields.String()
    size = fields.String()
    weight = fields.String()
    
개정보_변환기 = StingraySchema()

포포_정보 = 개정보_변환기.dump(포메라니안_포포)
도비_정보 = 개정보_변환기.dump(도베르만_도비)

# import json

# print(json.dumps(포포_정보))
# print(json.dumps(도비_정보))

# print(포포_정보)
# print(도비_정보)