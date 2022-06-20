from tkinter import Y
from django.db import models
from user.models import User as UserModel

class Category(models.Model):
    name = models.CharField("카테고리 이름", max_length=50)
    desc = models.TextField("카테고리 설명")
    
    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(UserModel, verbose_name="글쓴이", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=100)
    category = models.ManyToManyField(Category, verbose_name="카테고리")
    content = models.TextField("내용")
    exposure_start = models.DateTimeField("노출시작일자", null=True)
    exposure_end = models.DateTimeField("노출종료일자", null=True)
    
    def __str__(self):
        return f'{self.author} -> {self.title}'
    
    
class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, verbose_name="작성자", on_delete=models.CASCADE)
    comment = models.TextField("내용")
    
    def __str__(self):
        return f'{self.article} | ({self.user}) {self.comment}'