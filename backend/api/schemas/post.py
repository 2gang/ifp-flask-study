from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel
from api.schemas.user import AuthorSchema
from marshmallow import fields

class PostSchema(ma.SQLAlchemyAutoSchema):
    
    image = fields.String(required=True)
    
    created_at = fields.DateTime(format="%Y-%m=%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m=%d,%H:%M:%S")
    
    author = fields.Nested(AuthorSchema)
    
    liker_count = Method("get_liker_count")
    is_like = Method("get_is_like")
    
    def get_liker_count(Self, obj):
        return obj.get_liker_count()
    
    def get_is_like(self, obj):
        if self.context.get("user"):
            return obj.is_like(self.context["user"])
    
    def get_author_name(self, obj):
        return obj.author.username
    
    
    class Meta:
        model = PostModel
        #보기 전용 필드들을 정의
        # dump_only = [
        #     "author_name",
        # ]
        # #쓰기 전용 필드들을 정의
        # load_only = [
        #     "author_id",
        # ]
        exclude = ("author_id",)
        dump_only = "is_like",
        include_fk = True       #외래 키 포함 여부
        load_instance = True    #모델 객체를 로드할지에 대한 여부
        ordered = True