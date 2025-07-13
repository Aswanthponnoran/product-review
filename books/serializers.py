from rest_framework import serializers
# class StudentSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=30)
#     age = serializers.IntegerField()
#     place = serializers.CharField(max_length=30)

from books.models import Book,Review
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'feedback', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        if Review.objects.filter(user=user, book=data['book']).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        return data
class BookSerializer(serializers.ModelSerializer):#To implement serialization in Rest api application
    images=serializers.ImageField(required=False)
    images_url = serializers.SerializerMethodField('get_images_url')
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model=Book
        fields='__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None

    def get_images_url(self,obj):
        request = self.context.get('request')
        photo_url = obj.images.url
        return request.build_absolute_uri(photo_url)


from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','email','first_name','last_name']



    def create(self,validated_data):
      u=validated_data['username']
      p=validated_data['password']
      e=validated_data['email']
      f=validated_data['first_name']
      l=validated_data['last_name']
      u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
      u.save()
      return u