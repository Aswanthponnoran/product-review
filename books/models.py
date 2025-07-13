from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=20)
    description = models.TextField()  # This is likely the new field
    language=models.CharField(max_length=20)
    price=models.IntegerField()
    images=models.ImageField(upload_to="images",blank=True)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')  # Prevent duplicate reviews

    def __str__(self):
        return f"{self.user} - {self.book} ({self.rating})"

    # def __str__(self):
    #     return self.title