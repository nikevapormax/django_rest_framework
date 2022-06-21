from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import F
from rest_framework import status

# 로그인 및 로그아웃에 사용
from django.contrib.auth import login, authenticate, logout

from .serializers import UserSerializer

from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .models import Hobby as HobbyModel

from django_rest_framework.permissions import MyAuthenticateOver3, IsAdminOrIsAuthenticated

# 사용자 정보 
class UserView(APIView):
    # permission_classes = [MyAuthenticateOver3]
    permission_classes = [IsAdminOrIsAuthenticated]
    
    # 사용자 정보 조회
    def get(self, request):
        # 다수의 사용자의 값을 불러올 때 사용!
        # all_user = UserModel.objects.all()
        # return Response(UserSerializer(all_user, many=True).data)
        user_serializer = UserSerializer(request.user, context={"request": request}).data
        return Response(user_serializer)
        
        # print(dir(user))
        # return Response({})
        
        # 역참조를 사용해 사용자의 취미를 불러옴
        # 그런데 우리가 위의 모델을 보면 related_name을 사용하지 않음
        # user와 user profile의 관계가 OneToOne 관계라서 그럼
        # hobbys = user.userprofile.hobby.all()
        
        # for hobby in hobbys:
            # print(dir(hobby))
            # exclude : 매칭 된 쿼리만 제외, filter와 반대
            # annotate : 필드 이름을 변경해주기 위해 사용, 이외에도 원하는 필드를 추가하는 등 다양하게 활용 가능
            # values / values_list : 지정한 필드만 리턴 할 수 있음. values는 dict로 return, values_list는 tuple로 ruturn
            # F() : 객체에 해당되는 쿼리를 생성함
            
            # print(f'1 : {hobby.userprofile_set.all()}')
            # print(f'2 : {hobby.userprofile_set.exclude(user=user)}')
            # print(f"3 : {hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username'))}")
            # print(f"4 : {hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username')}")
            # print(f"5 : {hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True)}")
            # print(f"6 : {list(hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True))}")
            # break
        
            # hobby_members = hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True)
            # hobby_members = list(hobby_members)
           
            # print(f"hobby : {hobby.name} / hobby members : {hobby_members}")
        
        # return Response({"hobbys": str(hobbys)})
    
    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data, context={"request": request})
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer = UserSignupSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"msg": "signup success!!" })
        # else:
        #     print(serializer.errors)
        #     return Response({"msg": "signup fail!!" })
       
    
    # 회원 정보 수정
    def put(self, request, obj_id):
        # user = request.user
        target_user = UserModel.objects.get(id=obj_id)
        # fields에 있는 데이터를 다 넣을 필요가 없도록 하기 위해 partial=True 사용
        user_serializer = UserSerializer(target_user, data=request.data, partial=True, context={"request": request})
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원 탈퇴
    def delete(self, request):
        return Response({"msg": "delete method!!" })


class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        
        # 변수 user에는 인증에 성공하면 user가 담기고, 인증 실패하면 None이 담기게 됨
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"error": "존재하지 않는 계정 또는 일치하지 않는 비밀번호를 입력하셨습니다."})
        login(request, user)
        return Response({"msg": "login success!!"})
    
    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"msg": "logout success!!"})