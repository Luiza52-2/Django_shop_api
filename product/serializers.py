from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg  # чтобы считать среднее


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.product_set.count()
    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название категории должно быть минимум 3 символа.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    def validate_stars(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'  # или перечисли: ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        average = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return round(average, 1) if average else None
    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название должно быть минимум 3 символа.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value
class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        total = sum([r.stars for r in reviews if r.stars])
        count = len([r for r in reviews if r.stars])
        return round(total / count, 2) if count > 0 else None
