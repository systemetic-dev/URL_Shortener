from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.shortener.models import URL
from .serializers import ShortenURLSerializer,RegisterSerializer,URLListSerializer


from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class ShortenURLView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ShortenURLSerializer(data=request.data)

        if serializer.is_valid():

            url = serializer.save(user=request.user)

            short_url = f"http://localhost:8000/{url.short_code}"

            return Response({
                "short_code": url.short_code,
                "short_url": short_url
            })
            
class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyURLsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        urls = URL.objects.filter(user=request.user).order_by("-created_at")
        
        paginator = PageNumberPagination()
        paginated_urls = paginator.paginate_queryset(urls, request)

        serializer = URLListSerializer(urls, many=True)

        return paginator.get_paginated_response(serializer.data)