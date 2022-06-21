from rest_framework import serializers

from .models import Article as ArticleModel
from .models import Comment as CommentModel
#  from .models import Category as CatogoryModel

# class CategorySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = CatogoryModel
#         fields = ["name", "category"]

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username
    
    class Meta:
        model = CommentModel
        fields = ["username", "comment"]

class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    # related_name을 작성했다면 source는 쓸 필요가 없음
    comments = CommentSerializer(many=True, source='comment_set', read_only=True)
    
    # 카테고리를 리스트로 받아오기 위해 다음과 같이 작성
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    
    class Meta:
        model = ArticleModel
        fields = ["author", "title", "content", "comments", "exposure_start", "exposure_end", "category"]
        
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'author': {'write_only': True}, # default : False
            'title': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '제목을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '제목이 이상해요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': True # default : True
                    },
            }
