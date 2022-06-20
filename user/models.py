from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model
class User(AbstractBaseUser):
    
    # "사용자 계정"은 admin 페이지에서 나오는 메뉴의 이름 / unique=True를 설정해 단 하나의 값만 입력할 수 있도록 함
    username = models.CharField("사용자 계정", max_length=50, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일", max_length=100)
    name = models.CharField("이름", max_length=20)
    # auto_now_add : 최초 생성 시의 시간을 자동으로 입력해줌.(그 후 업데이트에 대한 시간 기록은 x) 주로 가입일, 최초 생성일 등에 사용함
    join_data = models.DateTimeField("가입일자", auto_now_add=True) # DateField로 해 다시할때
    
    # 사용자 계정이 활성화 되었는지(False이면 비활성화)
    is_active = models.BooleanField(default=True)
    # admin 권한을 사용할 것인지(is_staff에서 해당 값 사용)
    is_admin = models.BooleanField(default=True)
    
    # 사용자가 로그인할 때 사용하는 id로 어떤 것을 사용할래? 라는 것에 지정을 해준 것.
    # 물론 다른 값으로도 사용 가능하다!! 
    USERNAME_FIELD = 'username'
    
    # 슈퍼계정을 생성할 때 입력해야 할 값들을 지정할 수 있음.
    # 아래와 같이 사용하지 않아도 되지만, 선언은 해야 함
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin
    
# Hobby model
class Hobby(models.Model):
    name = models.CharField("취미 이름", max_length=50)    
    
    def __str__(self):
        return self.name

# User Profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="사용자", on_delete=models.CASCADE)
    introduction = models.TextField("자기소개")
    birth = models.DateField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField(Hobby, verbose_name="취미")
    
    def __str__(self):
        return f'{self.user.username} 님의 프로필'    
    
