from rest_framework import serializers

from datetime import datetime

from .models import Product as ProductModel, Review
from .models import Review as ReviewModel

class ReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ReviewModel
        fields = ["content", "rate"]
        
class ProductSerializer(serializers.ModelSerializer):
    last_review = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
        
    def get_last_review(self, obj):
        review_list = []
        
        for reviews in obj.review_set.all():
            if reviews.content:
                review_list.append(reviews.content)
        
        if len(review_list) != 0:
            return review_list[-1]
        
        return ""
        
    def get_avg_rate(self,obj):
        review_list = []
        
        for reviews in obj.review_set.all():
            if reviews.content:
                review_list.append(reviews.rate)
        
        if len(review_list) != 0:
            return sum(review_list) / len(review_list)
        
        return 0
    
    class Meta:
        model = ProductModel
        fields = ["user", "title", "thumbnail", "desc", "created_at", "exposure_start",
                  "exposure_end", "price", "updated_at", "activate", "last_review", "avg_rate"]
        
        read_only_fields = ["created_at", "updated_at"]
    
    # 노출 종료 일자가 현재보다 더 이전 시점이라면 상품을 등록할 수 없도록
    def validate(self, data):
        print(1, data)
        today = datetime.now().date()
        
        if today > data["exposure_end"]:
            raise serializers.ValidationError(
                detail={"error": "노출 종료 일자가 너무 이릅니다."}
            )
        return data
    
    # 상품 설명의 마지막에 "<등록 일자>에 등록된 상품입니다." 라는 문구를 추가
    def create(self, validated_data):
        desc = validated_data.pop("desc")
        product = ProductModel(**validated_data)
        product.save()
        
        create_time = product.created_at
        new_desc = f'{desc} {create_time.date()}에 등록된 상품입니다.'

        product_change = ProductModel.objects.get(id=product.id)
        product_change.desc = new_desc
        product_change.save()
      
        return product_change
    
    # update 됐을 때 상품 설명의 가장 첫줄에 "<수정 일자>에 수정되었습니다." 라는 문구를 추가
    # 수정할 때마다 문구가 붙는 문제 고쳐야함
    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        desc = validated_data.pop("desc")
    
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        new_desc = f'{instance.updated_at.date()}에 수정되었습니다. {desc}'
        instance.desc = new_desc
        instance.save()
        
        return instance
    
    

    
    
    
    