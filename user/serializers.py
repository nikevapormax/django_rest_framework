from rest_framework import serializers

from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .models import Hobby as HobbyModel

from blog.serializers import ArticleSerializer, CommentSerializer
from product.serializers import ProductSerializer, ReviewSerializer
# class UserSignupSerializer(serializers.ModelSerializer):
#     def create(self, *args, **kwargs):
#         user = super().create(*args, **kwargs)
#         p = user.password
#         user.set_password(p)
#         user.save()
#         return user
    
#     def update(self, *args, **kwargs):
#         user = super().create(*args, **kwargs)
#         p = user.password
#         user.set_password(p)
#         user.save()
#         return user
    
#     class Meta:
#         model = UserModel
#         fields = '__all__' # UserModel의 모든 것을 필드로 사용
        

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
    hobby = HobbySerializer(many=True, read_only=True) # QuerySet (ManyToMany 관계)
    get_hobbys = serializers.ListField(required=False)
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birth", "age", "hobby", "get_hobbys"]

class UserSerializer(serializers.ModelSerializer):
    user_detail = UserProfileSerializer(source="userprofile") # object (OneToOne 관계)
    articles = ArticleSerializer(many=True, source="article_set", read_only=True)
    comments = CommentSerializer(many=True, source="comment_set", read_only=True)
    products = ProductSerializer(many=True, source="product_set", read_only=True)
    reviews = ReviewSerializer(many=True, source="review_set", read_only=True)
    # custom validator
    # 기존의 validator와 같이 쓰임
    def validate(self, data):
        if not data.get("email", "").endswith("@naver.com"):
            raise serializers.ValidationError(
                detail={"error": "네이버 이메일만 가입할 수 있습니다."}
            )
        return data
    
    # custom creator
    # 기존의 creator의 기능을 덮어쓰며, 이것을 만들면 기존의 creator는 작동하지 않음
    def create(self, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")
        
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        
        user_profile = UserProfileModel.objects.create(user=user, **user_profile)
        user_profile.hobby.add(*get_hobbys)
        
        return user
    
    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()
        
        user_profile_obj = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_obj, key, value)
        user_profile_obj.save()
        user_profile_obj.hobby.set(get_hobbys)
        
        return instance
        
    class Meta:
        # 내가 serializer에서 어떤 모델을 쓰겠다는 것을 선언하는 것!(중요)
        model = UserModel
        # join_data 같은 경우는 시스템에서 자동으로 등록해주는 것으로 기본적으로 read_only임
        fields = ["username", "password", "email", "name", "join_data", 
                  "user_detail", "articles", "comments", "products", "reviews"]
        
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            }
