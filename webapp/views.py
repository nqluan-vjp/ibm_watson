from django.shortcuts import render
from webapp.services import watson_discovery
from webapp.utils import convert_csv_to_json
import csv
import os 
from django.http import HttpResponse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_FOLDER = os.path.join(BASE_DIR, "resources",'csv')
def index(request):
    return render(request, 'webapp/index.html')

def search_data(request):
    collections = watson_discovery.get_collections()
    if request.method == 'GET':
        return render(request, 'webapp/search.html' ,{'collections': collections} )
    if request.method == 'POST':
        language = request.POST["language"]
        if language == "Language":
            language = 'news-ja' 
        search = request.POST["search"]
        data = watson_discovery.search_news(language,search,50)
        return render(request, 'webapp/search.html' ,
                       {'data' : data.result['results'] ,
                        'collections': collections ,
                        'language' : language ,
                        'search' : search ,
                        'matching_results' : data.result['matching_results']})

def trending_topic(request):
    data = watson_discovery.trending_news()
    return render(request, 'webapp/trending.html',{'data' : data.result['results']})


def export_csv(request):
    data,matching_results = watson_discovery.search_news_tesla()
    write_csv_file(data,matching_results)
    with open(CSV_FOLDER + '/' + 'data.csv',encoding="utf-8_sig" ,newline='') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'
    return response


def export_csv_news(request):
    data,matching_results = watson_discovery.search_news_to_csv(request.POST["search"])
    write_csv_file(data,matching_results)
    with open(CSV_FOLDER + '/' + 'data.csv',encoding="utf-8_sig" ,newline='') as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=data.csv'
    return response



def write_csv_file(data,matching_results):
    with open(CSV_FOLDER + '/' + 'data.csv', mode='w' ,encoding="utf-8_sig" ,newline='') as csv_file:
        fieldnames = ['matching_results','id', 'publication_date', 'text' , 'title','enriched_text.relations.type',
                      'enriched_text.relations.sentence',
                      'enriched_text.relations.score',
                      'enriched_text.relations.arguments.0.location.0',
                      'enriched_text.relations.arguments.0.location.1',
                      'enriched_text.relations.arguments.0.entities.type',
                      'enriched_text.relations.arguments.0.entities.text',
                      'enriched_text.relations.arguments.1.location.0',
                      'enriched_text.relations.arguments.1.location.1',
                      'enriched_text.relations.arguments.1.entities.type',
                      'enriched_text.relations.arguments.1.entities.text'
                      ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for obj in data:
            for item in obj['data']:
                if 'enriched_text' in item and 'relations' in item['enriched_text']:
                    for relation in item['enriched_text']['relations']:
                        writer.writerow({'matching_results' :matching_results ,'id': item['id'], 'publication_date': item['publication_date'], 'text': item['text'] , 'title' : item['title'],
                                         'enriched_text.relations.type' : relation['type'],
                                         'enriched_text.relations.sentence' :relation['sentence'],
                                         'enriched_text.relations.score' : relation['score'] ,
                                         'enriched_text.relations.arguments.0.location.0' : relation['arguments'][0]['location'][0],
                                         'enriched_text.relations.arguments.0.location.0' : relation['arguments'][0]['location'][1],
                                         'enriched_text.relations.arguments.0.entities.type' : relation['arguments'][0]['entities'][0]['type'],
                                         'enriched_text.relations.arguments.0.entities.text' : relation['arguments'][0]['entities'][0]['text'] ,
                                         'enriched_text.relations.arguments.1.location.0' : relation['arguments'][1]['location'][0] ,
                                         'enriched_text.relations.arguments.1.location.1' : relation['arguments'][1]['location'][1] ,
                                         'enriched_text.relations.arguments.1.entities.type' : relation['arguments'][1]['entities'][0]['type'],
                                         'enriched_text.relations.arguments.1.entities.text' : relation['arguments'][1]['entities'][0]['text']})
                        

def convert_csv(request):
    convert_csv_to_json()
    with open(CSV_FOLDER + '/' + 'data.json',encoding="utf-8_sig" ,newline='') as myfile:
        response = HttpResponse(myfile, content_type='text/json')
        response['Content-Disposition'] = 'attachment; filename=data.json'
    return response

                        
            
    