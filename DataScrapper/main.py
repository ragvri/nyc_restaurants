import db_handler, nycopen, yelp, es_handler
import json
from decimal import *

def populate_aws(es_info, limit=1, offset=0, boro='Manhattan'):
    """populate aws dynamodb and create json for ElasticSearch"""

    requried_col = set(['boro', 'zipcode', 'inspection_date',
                        'violation_description', 'score', 'grade',
                        'latitude', 'longitude', 'image_url', 'url',
                        'rating', 'price', 'location', 'categories',
                        'phone', 'name'])
    phones = nycopen.get_unique_phones(limit=limit, offset=offset, boro=boro)
    for phone in phones:
        phone = phone['phone']
        reviews = nycopen.get_review(phone, limit=1)
        info_list = yelp.get_info(phone)
        mapping = {}
        if info_list:
            for key in reviews[0]:
                if key in requried_col:
                    mapping[key] = reviews[0].get(key)
            for key in info_list[0]:
                if key in requried_col:
                    mapping[key] = info_list[0].get(key)
            if mapping['categories']:
                temp = []
                for cat in mapping['categories']:
                    temp.append(cat.get('alias'))
                    temp.append(cat.get('title'))
                mapping['categories'] = temp
            if mapping['location']:
                mapping['address'] = mapping.get('location').get('display_address')
            mapping.pop('location')

            mapping['latitude'] = Decimal(mapping['latitude'])
            mapping['longitude'] = Decimal(mapping['longitude'])
            mapping['rating'] = Decimal(mapping['rating'])
            mapping['score'] = int(mapping['score'])

            db_handler.add_item(mapping)
            es_handler.update_restaurants(es_info, mapping)
    return es_info

if __name__ == '__main__':
    offset = 0
    for i in range(4):
        es_info = populate_aws([], limit=1000, offset=i*1000)
        es_handler.info2json(es_info, filename=str(i))
