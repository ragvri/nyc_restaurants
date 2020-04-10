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
        yelp_list = yelp.get_info(phone)
        mapping = {}
        if yelp_list:
            mapping.update(reviews[0])
            mapping.update(yelp_list[0])
            for key in list(mapping.keys()):
                if key not in requried_col:
                    mapping.pop(key)

            if mapping['categories']:
                temp = []
                for cat in mapping['categories']:
                    temp.append(cat.get('alias'))
                    temp.append(cat.get('title'))
                mapping['categories'] = temp
            if mapping['location']:
                mapping['address'] = mapping.get('location').get('display_address')
            mapping.pop('location')

            if mapping.get('longitude') and mapping.get('latitude'):
                mapping['longitude'] = Decimal(mapping.get('longitude'))
                mapping['latitude'] = Decimal(mapping.get('latitude'))
            else:
                break
            mapping['latitude'] = Decimal(mapping['latitude'])
            mapping['longitude'] = Decimal(mapping['longitude'])
            if mapping.get('rating'):
                mapping['rating'] = Decimal(mapping.get('rating'))
            if mapping.get('score'):
                mapping['score'] = int(mapping.get('score'))

            # deal with aws ValidationException when encounter empty string
            for key in mapping:
                if not mapping[key]:
                    mapping[key] = None

            db_handler.add_item(mapping)
            es_handler.update_restaurants(es_info, mapping)
    return es_info

if __name__ == '__main__':
    """total amount of restaurants in Manhattan in nyc open data is 10049"""
    for i in range(0, 120):
        es_info = populate_aws([], limit=100, offset=i*100)
        es_handler.info2json(es_info, filename=str(i))
        print('finish downloading part', i)
