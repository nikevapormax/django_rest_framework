from django.db import models
from django.forms import BooleanField
from user.models import User as UserModel

from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    thumbnail = models.FileField("썸네일", upload_to="product/", null=True)
    desc = models.TextField("설명")
    created_at = models.DateTimeField("등록일자", auto_now_add=True)
    exposure_start = models.DateField("노출시작일")
    exposure_end = models.DateField("노출종료일")
    price = models.IntegerField("가격", default=0)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    activate = models.BooleanField("활성화여부", default=True)
    
    def __str__(self):
        return f'{self.user} -> {self.title} | {self.desc}'
    

class Review(models.Model):
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="상품", on_delete=models.CASCADE)
    content = models.TextField("내용")
    rate = models.IntegerField("평점(0~5 이내 정수)",validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    
    def __str__(self):
        return f'{self.user} : {self.product}에 대한 리뷰'