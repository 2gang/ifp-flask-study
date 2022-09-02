class Stringray:
    def __init__(self, name, age, size, weight, place_of_birth):
        self.name = name    #이름
        self.age = age      #나이
        self.size = size    #크기/높이
        self.weight = weight    #무게
        self.place_of_birth = place_of_birth    #출생지
        
포메라니안_포포 = Stringray(
    "포포",
    "3",
    "14cm",
    "2.3kg",
    "Germany",    
)


print(포메라니안_포포.__dict__)