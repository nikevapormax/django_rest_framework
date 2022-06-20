from rest_framework import serializers

from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .models import Hobby as HobbyModel

from blog.serializers import ArticleSerializer, CommentSerializer
class UserSignupSerializer(serializers.ModelSerializer):
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user
    
    def update(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user
    
    class Meta:
        model = UserModel
        fields = '__all__' # UserModel의 모든 것을 필드로 사용
        

class HobbySerializer(serializers.ModelSerializer):
    same_hobby_user = serializers.SerializerMethodField()
    def get_same_hobby_user(self, obj):
        user_list = []
        user = self.context["request"].user
        
        for user_profile in obj.userprofile_set.exclude(user=user):
            user_list.append(user_profile.user.username)
        return user_list
    
        # 위의 for문을 리스트 컴프리헨션을 통해 줄일 수 있음!
        # return [user_profile.user.username for user_profile in obj.userprofile_set.all()]
    
    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_user"]

class UserProfileSerializer(serializers.ModelSerializer):
    # input data가 QuerySet일 경우 many=True를 입력해주어야 한다. 
    hobby = HobbySerializer(many=True) # QuerySet (ManyToMany 관계)
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birth", "age", "hobby"]

class UserSerializer(serializers.ModelSerializer):
    user_detail = UserProfileSerializer(source="userprofile") # object (OneToOne 관계)
    articles = ArticleSerializer(many=True, source="article_set")
    comments = CommentSerializer(many=True, source="comment_set")
    
    class Meta:
    
        # 내가 serializer에서 어떤 모델을 쓰겠다는 것을 선언하는 것!(중요)
        model = UserModel
        fields = ["username", "email", "name", "join_data", "user_detail", "articles", "comments"]
