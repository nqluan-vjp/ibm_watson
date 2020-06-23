'''
Created on 2020/06/18

@author: DXG
'''
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_waston import settings
from ibm_watson import ApiException

def get_discovery():
    authenticator = IAMAuthenticator(settings.DISCOVERY_API_KEY)
    discovery = DiscoveryV1(
        version=settings.DISCOVERY_VERSION,
        authenticator=authenticator
    )
    discovery.set_service_url(settings.DISCOVERY_API_URL)
    return discovery

def get_environments():   
    discovery = get_discovery()
    environments = discovery.list_environments().get_result()
    system_environments = [x for x in environments['environments'] if x['name'] == 'Watson System Environment']
    system_environment_id = system_environments[0]['environment_id']
    return system_environment_id
   

def get_collections():
    try:
        discovery = get_discovery()
        system_environment_id = get_environments()
        collections = discovery.list_collections(system_environment_id).get_result()
        system_collections = [x for x in collections['collections']]
        return system_collections
    except ApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message
               )
def search_news (language,search,count):
    try:
        discovery = get_discovery()
        system_environment_id = get_environments()
        data = discovery.query(system_environment_id, language, query = search,count = count)
        return data
    except ApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message) 
        
def trending_news ():
    try:
        discovery = get_discovery()
        system_environment_id = get_environments()
        return_ = 'enriched_title.entities.text'
        aggregation = 'term(enriched_title.entities.text).top_hits(10)'
        filter = 'crawl_date>=now-1day'
        data = discovery.query(system_environment_id, 'news-ja',aggregation = aggregation ,filter=filter)
        return data
    except ApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message) 
    