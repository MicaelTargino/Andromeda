from django.shortcuts import render
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.conf import settings
from .utils import get_es_client

INDEX_NAME = settings.INDEX_NAME

# Create your views here.
def search(request, search_query: str, skip: int = 0, limit: int = 10) -> dict: 
    if request.method == 'POST':
        return HttpResponseBadRequest("Wrong method called")
    
    es = get_es_client(max_retries=50, sleep_time=5)
    response = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": ["title", "explanation"]
                }
            },
            "from": skip,
            "size": limit
        },
        filter_path=["hits.hits._source,hits.hits._score"]
    )
    hits = response["hits"]["hits"]
    return JsonResponse({"hits": hits})