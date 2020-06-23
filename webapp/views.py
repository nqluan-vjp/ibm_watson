from django.shortcuts import render
from webapp.services import watson_discovery
import json
def index(request):
    return render(request, 'webapp/index.html')

def search_data(request):
    collections = watson_discovery.get_collections()
    if request.method == 'GET':
        return render(request, 'webapp/search.html' ,{'collections': collections} )
    if request.method == 'POST':
        language = request.POST["language"]
        search = request.POST["search"]
        data = watson_discovery.search_news(language,search,50) 
        return render(request, 'webapp/search.html' ,
                       {'data' : data.result['results'] ,
                        'collections': collections ,
                        'language' : language ,
                        'search' : search})

def trending_topic(request):
    data = watson_discovery.trending_news()
    print(json.dumps(data.result['results']))
    return render(request, 'webapp/trending.html',{'data' : data.result['results']})