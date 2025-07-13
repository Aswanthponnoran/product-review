from django.shortcuts import render,redirect
from books.models import Book,Review
from django.contrib.auth.decorators import login_required

from books.serializers import BookSerializer, ReviewSerializer

from rest_framework import viewsets

# views.py

from rest_framework import generics, permissions

# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.AllowAny]


def hom(request):
    return render(request,"hom.html")
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class BookView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated,]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# from django.db.models import Q
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
#
# class Searchview(APIview):
#     def get(self,request):
#         querry=self.request.querry_params.get('search')
#         if querry:
#             b=Book.objects.filter(Q(title__icontains=querry))|Q(author__icontains=querry)|Q(languae__icotains=querry)
#             books=BookSerializer(b,many=True)
#             return Response(b.data,status.status.HTTP_200_ok)
#

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('search')  # Corrected typo
        if query:
            b = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(language__icontains=query)  # Fixed typo
            )
            if not b.exists():
                return Response({"message": "No SEARCH query provided"}, status=status.HTTP_200_OK)

            books = BookSerializer(b, many=True,context={"request":request})
            return Response(books.data, status=status.HTTP_200_OK)  # Corrected status
        else:
            return Response({"message": "No search QUERYY provided"}, status=status.HTTP_200_OK)


#Filter by price

class filterbyprice(APIView):
    def get(self, request):
        query = request.query_params.get('price')  # Corrected typo
        if query:
            b = Book.objects.filter(
                Q(title__le=query)
             )
            if not b.exists():
                return Response({"message": "No search query provided"}, status=status.HTTP_200_OK)

            books = BookSerializer(b, many=True)
            return Response(books.data, status=status.HTTP_200_OK)  # Corrected status
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_200_OK)



#Filter by title
class filterbytitle(APIView):
    def get(self, request):
        query = request.query_params.get('title')  # Corrected typo
        if query:
            b = Book.objects.filter(
                Q(title__icontains=query)
             )
            if not b.exists():
                return Response({"message": "No search query provided"}, status=status.HTTP_200_OK)

            books = BookSerializer(b, many=True)
            return Response(books.data, status=status.HTTP_200_OK)  # Corrected status
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_200_OK)


#Filter by description
class filterbydescription(APIView):
    def get(self, request):
        query = request.query_params.get('description')  # Corrected typo
        if query:
            b = Book.objects.filter(Q(author__icontains=query))
            if not b.exists():
                return Response({"message": "No search query provided"}, status=status.HTTP_200_OK)

            books = BookSerializer(b, many=True)
            return Response(books.data, status=status.HTTP_200_OK)  # Corrected status
        else:
            return Response({"message": "No search query provided"}, status=status.HTTP_200_OK)




# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
#
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         # Delete the user's token
#         self.request.user.auth_token.delete()
#         return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
#


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can access this

    def post(self, request):
        try:
            request.auth.delete()  # Deletes the user's token
            return Response({"detail": "Successfully logged out from this account."}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({"error": "Invalid token or user not logged in."}, status=status.HTTP_400_BAD_REQUEST)




from books.serializers import UserSerializer
from django.contrib.auth.models import User
class UserAPI(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated,]

    queryset = User.objects.all()
    serializer_class = UserSerializer





