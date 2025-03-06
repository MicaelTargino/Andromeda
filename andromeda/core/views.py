from django.shortcuts import render
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.conf import settings
from .utils import get_es_client

INDEX_NAME = settings.INDEX_NAME

# Create your views here.
def search(request) -> dict: 
    if request.method == 'POST':
        return HttpResponseBadRequest("Wrong method called")

    # Extract query parameters
    search_query = request.GET.get('search_query', '')
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 10))

    # Validate parameters
    if not search_query:
        return render(request, "app.html", {"search_results": []})
    
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

    cleaned_hits = []
    for hit in hits:
        cleaned_item = {key.lstrip('_'): value for key, value in hit.items()}
        cleaned_hits.append(cleaned_item)

    return render(request, "app.html", {"search_query": search_query, "search_results": cleaned_hits})

def homepage(request):
    return render(request, "app.html")