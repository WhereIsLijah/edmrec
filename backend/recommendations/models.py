from django.db import models
from django.db.models import JSONField

class Metadata(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    source = models.CharField(max_length=255)
    url = models.URLField(unique=True)  # Make URL unique
    size = models.CharField(max_length=50)
    format = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Embedding(models.Model):
    dataset = models.ForeignKey(Metadata, on_delete=models.CASCADE, related_name='embeddings')
    tfidf_embedding = JSONField()
    bert_embedding = JSONField()
    combined_normalized_text = models.TextField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Embedding for {self.dataset.title}"

class Query(models.Model):
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    results = models.ManyToManyField(Metadata, through='QueryResult')

    def __str__(self):
        return self.query_text

class QueryResult(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Metadata, on_delete=models.CASCADE)