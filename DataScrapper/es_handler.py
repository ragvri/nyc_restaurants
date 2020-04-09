import json

def update_restaurants(restaurants, new_rest):
    requried_col = set(['boro', 'zipcode', 'inspection_date', 'score', 'grade',
                        'latitude', 'longitude', 'rating', 'price', 'categories',
                        'phone', 'name'])
    for key in list(new_rest.keys()):
        if key not in requried_col:
            new_rest.pop(key)
        if key == 'rating':
            new_rest[key] = float(new_rest[key])
        if key in ('latitude', 'longitude'):
            # json can't handle Decimal
            new_rest[key] = str(new_rest[key])
    restaurants.append({"index": {"_index": 'restaurants', '_id': len(restaurants),
                                  '_type': 'Restaurant'}})
    restaurants.append(new_rest)
    return restaurants

def info2json(restaurants, filename=''):
    with open('ESinfo-{}.json'.format(filename), 'w') as f:
        for row in restaurants:
            json.dump(row, f)
