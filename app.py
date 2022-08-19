from flask import Flask, jsonify

app = Flask(__name__)


shop_list = [
    {
        'name' : 'Smith flower store',
        'items' : [
            {
                'name' : '물망초',
                'price' : '1200',
            }
        ]
    },
]
'''
서버의 입장에서,
POST -  클라이언트가 보낸 데이터를 받는 데에 사용한다.
GET  -  데이터를 다시 돌려주는 데에만 사용한다.
'''

# 아래에서 다룰 리소스들 : shop, item

# POST /shop -> name 이라는 데이터를 받아서, 새로운 shop을 생성함
@app.route('/shop', methods=['POST'])
def create_shop():
    pass

# GET  /shop/<string:shop_name> -> name 에 맞는 shop 을 보여줌
@app.route('/shop/<string:shop_name>', methods=['GET'])
def get_shop_detail():
    return jsonify(shop_list)

# GET  /shop -> shop의 목록들을 보여줌
@app.route('/shop', methods=['GET'])
def get_shop_list():
    pass

# POST /shop/<string:shop_name>/item -> item_name, price 를 받아서, name에 맞는 shop에 새로운 item을 추가
@app.route('/shop/<string:shop_name>/item', methods=['POST'])
def create_item_in_shop():
    pass

# GET  /shop/<string:shop_name>/item -> shop에 들어있는 item들의 목록을 반환
@app.route('/shop/<string:shop_name>/item', methods=['GET'])
def get_item_list_in_shop(shop_name):
    pass

if __name__ == '__main__':
    app.run()