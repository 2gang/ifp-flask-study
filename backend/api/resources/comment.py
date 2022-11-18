from flask_restful import Resource, request
from api.models.post import PostModel
from api.models.comment import CommentModel
from api.schemas.comment import CommentSchema
from api.models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

comment_list_schema = CommentSchema(many=True)
comment_schema = CommentSchema()

class CommentList(Resource):
    @classmethod
    def get(cls, post_id):
        post = PostModel.find_by_id(post_id)
        ordered_comment_list = post.comment_set.order_by(CommentModel.id.desc())
        
        return comment_list_schema.dump(ordered_comment_list)
    
    @classmethod
    @jwt_required()
    def post(cls, post_id):
        comment_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        try:
            new_comment = comment_schema.load(comment_json)
            new_comment.author_id = author_id
            new_comment.post_id = post_id
        except ValidationError as err:
            return err.messages, 400
        try:
            new_comment.save_to_db()
        except:
            return {"Error" : "저장에 실패하였습니다."}, 500
        return comment_schema.dump(new_comment), 201
    
    
class CommentDetail(Resource):
    @classmethod
    @jwt_required()
    def put(cls, post_id, comment_id):
        comment_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        comment = CommentModel.find_by_id(comment_id)
        post = PostModel.find_by_id(post_id)
        # 댓글의 존재 여부를 먼저 체크한다.
        if not comment:
            return {"Error": "댓글을 찾을 수 없습니다."}, 404
        if post.id == post_id and comment.author_id == author_id:
            comment.update_to_db(comment_json)
        else:
            return { "Error" : "댓글은 작성자만 수정할 수 있습니다."}, 403
        
        return comment_schema.dump(comment), 200


    
    @classmethod
    @jwt_required()
    def delete(cls, post_id, comment_id):
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        post = PostModel.find_by_id(post_id)
        comment = CommentModel.find_by_id(comment_id)
        # 댓글의 존재 여부를 먼저 체크한다.
        if not comment:
            return {"Error": "댓글을 찾을 수 없습니다."}, 404

        if post.id == post_id and comment.author_id == author_id:
            comment.delete_from_db()
        else:
            return {"Error": "댓글은 작성자만 삭제할 수 있습니다."}, 403
        
        return {"message" : "댓글이 성공적으로 삭제되었습니다."}, 200