from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Metadata, Embedding, Query, QueryResult
from .serializers import MetadataSerializer, EmbeddingSerializer, QuerySerializer, QueryResultSerializer
from .query_processing.process_query import process_query

class MetadataListView(APIView):
    def get(self, request):
        metadatas = Metadata.objects.all()
        serializer = MetadataSerializer(metadatas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MetadataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmbeddingListView(APIView):
    def get(self, request):
        embeddings = Embedding.objects.all()
        serializer = EmbeddingSerializer(embeddings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmbeddingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QueryListView(APIView):
    def get(self, request):
        queries = Query.objects.all()
        serializer = QuerySerializer(queries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QueryResultListView(APIView):
    def get(self, request):
        query_results = QueryResult.objects.all()
        serializer = QueryResultSerializer(query_results, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QueryResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QueryProcessingView(APIView):
    def post(self, request):
        query_text = request.data.get('query')
        if not query_text:
            return Response({"error": "Query text is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        results = process_query(query_text)
        return Response(results, status=status.HTTP_200_OK)