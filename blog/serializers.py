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
    comments = CommentSerializer(many=True, source='comment_set')
    
    # 카테고리를 리스트로 받아오기 위해 다음과 같이 작성
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    
    class Meta:
        model = ArticleModel
        fields = ["title", "content", "comments", "category"]
