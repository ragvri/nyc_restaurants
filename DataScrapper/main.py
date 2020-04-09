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
        if info_list:
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

            db_handler.add_item(mapping)
            es_handler.update_restaurants(es_info, mapping)
    return es_info

if __name__ == '__main__':
    offset = 0
    for i in range(4):
        es_info = populate_aws([], limit=1000, offset=i*1000)
        es_handler.info2json(es_info, filename=str(i))
