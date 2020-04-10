import json, os, requests

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
            f.write('\n')

def merge(path):
    """
    merge all ESinfo
    """
    temp = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)) and f[:6] == 'ESinfo':
            with open(os.path.join(path, f), 'r') as file_:
                for line in file_:
                    temp.append(json.loads(line))

    with open('ESinfo-final.json', 'w') as f:
        for i, line in enumerate(temp):
            if 'index' in line and '_id' in line['index']:
                line['index']['_id'] = i // 2
            json.dump(line, f)
            f.write('\n')

def post(fn):
    """
    post data to Elastic search
    """
    url = "https://search-nyc-restaurants-inspection-oksmivk4fqfcwxeprrwjvp32ii.us-east-1.es.amazonaws.com/_bulk"
    headers = {'Content-Type': 'application/json'}
    with open(fn, 'r') as f:
        req = requests.post(url, data=f, headers=headers)
        print(req.text)
        print(req.status_code)
        print(req.headers)
