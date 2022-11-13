from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel
from marshmallow import fields

class PostSchema(ma.SQLAlchemyAutoSchema):
    
    image = fields.String(required=True)
    
    created_at = fields.DateTime(format="%Y-%m=%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m=%d,%H:%M:%S")
    
    author_name = Method("get_author_name")
    
    def get_author_name(self, obj):
        return obj.author.username
    
    
    class Meta:
        model = PostModel
        #보기 전용 필드들을 정의
        dump_only = [
            "author_name",
        ]
        # #쓰기 전용 필드들을 정의
        # load_only = [
        #     "author_id",
        # ]
        exclude = ("author_id",)
        include_fk = True       #외래 키 포함 여부
        load_instance = True    #모델 객체를 로드할지에 대한 여부
        ordered = True