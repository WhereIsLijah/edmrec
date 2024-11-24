from django.urls import path
from .views import MetadataListView, EmbeddingListView, QueryListView, QueryResultListView, QueryProcessingView

urlpatterns = [
    path('datasets/', MetadataListView.as_view(), name='datasets-list'),
    path('embeddings/', EmbeddingListView.as_view(), name='embedding-list'),
    path('queries/', QueryListView.as_view(), name='query-list'),
    path('query-results/', QueryResultListView.as_view(), name='query-result-list'),
    path('query/', QueryProcessingView.as_view(), name='query-processing'),
]