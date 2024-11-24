from django.contrib import admin
from .models import Metadata, Embedding, Query, QueryResult

admin.site.register(Metadata)
admin.site.register(Embedding)
admin.site.register(Query)
admin.site.register(QueryResult)