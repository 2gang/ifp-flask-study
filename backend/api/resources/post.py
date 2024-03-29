from xml.dom import ValidationErr
from flask_restful import Resource, request
from api.models.post import PostModel, db
from api.schemas.post import PostSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.user import UserModel

post_schema = PostSchema()
post_list_schema = PostSchema(many=True)

class Post(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            user = UserModel.find_by_username(get_jwt_identity())
            _post_schema = PostSchema(context={"user": user})
            return _post_schema.dump(post), 200
        else:
            return {"Error": "게시물을 찾을 수 없습니다."}, 404 
    
    @classmethod
    @jwt_required()
    def put(cls, id):
        """
        게시물의 전체 내용을 받아서 게시물을 수정
        없는 리소스를 수정하려고 한다면 HTTP 404 상태 코드와 에러 메시지를,
        그렇지 않은 경우라면 수정을 진행
        """
        post_json = request.get_json()
        # first-fail 을 위한 입력 데이터 검증
        validate_result = post_schema.validate(post_json)
        if validate_result:
            return validate_result, 400
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        post = PostModel.find_by_id(id)
        # 게시물의 존재 여부를 먼저 체크한다.
        if not post:
            return {"Error": "게시물을 찾을 수 없습니다."}, 404

        # 게시물의 저자와, 요청을 보낸 사용자가 같다면 수정을 진행할 수 있다.
        if post.author_id == author_id:
            post.update_to_db(post_json)
        else:
            return {"Error": "게시물은 작성자만 수정할 수 있습니다."}, 403

        return post_schema.dump(post), 200
    
    @classmethod
    @jwt_required()
    def delete(cls, id):
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        post = PostModel.find_by_id(id)
        # 게시물의 존재 여부를 먼저 체크한다.
        if not post:
            return {"Error": "게시물을 찾을 수 없습니다."}, 404

        # 게시물의 저자와, 요청을 보낸 사용자가 같다면 삭제를 진행할 수 있다.
        if post.author_id == author_id:
            post.delete_from_db()
        else:
            return {"Error": "게시물은 작성자만 삭제할 수 있습니다."}, 403
        return {"message" : "게시물이 성공적으로 삭제되었습니다."}, 200
    
class PostList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        # 사용자, 페이지네이션 할 페이지 정의
        user = UserModel.find_by_username(get_jwt_identity())
        page = request.args.get("page", type=int, default=1)

        # 내부에서만 사용할 schema 정의
        _post_list_schema = PostSchema(context={"user": user}, many=True)
        
        #사용자가 팔로우하고 있는 모든 사용자들을 정의
        followed = user.followed.all()
        print(followed)

        # 사용자가 팔로우하고 있는 모든 사용자들의 게시물들을 가져옴
        ordered_posts = PostModel.filter_by_followed(
            followed_users=followed, request_user=user)

        # 클라이언트로부터 검색어 얻어오기
        search_querystring = f'%%{request.args.to_dict().get("search")}%%'

        # 검색어가 존재한다면, ordered_posts 재할당
        if request.args.to_dict().get("search"):
            ordered_posts = PostModel.filter_by_string(
                search_querystring
            ).order_by(PostModel.id.desc())

        pagination = ordered_posts.paginate(
            page=page, per_page=10, error_out=False
        )

        return _post_list_schema.dump(pagination.items)
    
    @classmethod
    @jwt_required()
    def post(cls):
        post_json = request.get_json()  #json 데이터를 받아옴
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        try:         
            new_post = post_schema.load(post_json)  #게시물 인스턴스로 변환
            new_post.author_id = author_id
        except ValidationErr as err:
            return err.messages, 400
        try:
            new_post.save_to_db()   #변환한 것을 데이터베이스에 저장
        except:
            return {"Error" : "저장에 실패하였습니다."}, 500
        return post_schema.dump(new_post), 201
    
class PostLike(Resource):
    @classmethod
    @jwt_required()
    def put(cls, id):
        """
        id 로 특정되는 게시물에 좋아요를 누릅니다.
        """
        # 사용자, 게시물을 특정
        user = UserModel.find_by_username(get_jwt_identity())
        post = PostModel.find_by_id(id)
        if not user or not post:
            return {"Error": "잘못된 요청입니다."}, 400
        post.do_like(user)
        return post.get_liker_count(), 200

    @classmethod
    @jwt_required()
    def delete(cls, id):
        """
        id 로 특정되는 게시물에 좋아요를 취소합니다.
        """
        # 사용자, 게시물을 특정
        user = UserModel.find_by_username(get_jwt_identity())
        post = PostModel.find_by_id(id)
        if not user or not post:
            return {"Error": "잘못된 요청입니다."}, 400
        post.cancel_like(user)
        return post.get_liker_count(), 200