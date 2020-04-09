from credential import NycOpen
import json, requests

"""
Supported keywords:
$select	The set of columns to be returned, similar to a SELECT in SQL
$where	Filters the rows to be returned, similar to WHERE
$order	Column to order results on, similar to ORDER BY in SQL
$group	Column to group results on, similar to GROUP BY in SQL, must be used with $select
$having	Filters the rows that result from an aggregation, similar to HAVING
$limit	Maximum number of results to return	1000 (2.0 endpoints: maximum of 50,000; 2.1: unlimited)
$offset	Offset count into the results to start at, used for paging	0

for more information, please check https://dev.socrata.com/docs/queries/
"""

def get(**kwargs):
    url =  "https://data.cityofnewyork.us/resource/43nn-pn8j.json"
    params =  kwargs
    headers = {"X-App-Token": NycOpen.APP_TOKEN.value}
    req = requests.get(url, params=params, headers=headers)

    # proceed only if the status code is 200
    if req.status_code != 200:
        print('The status code is {}, please try again.'.format(req.status_code))
        return []
    # printing the text from the response
    result = json.loads(req.text)
    return result

def get_unique_phones(boro=None, limit=10, offset=0):
    """
    get unique phone number from NycOpen
    """
    return get(**{'BORO': boro, "$limit": limit, '$offset': offset,
               '$group': 'phone', '$order': 'phone', '$select': 'phone'})

def get_review(phone, limit=10, offset=0):
    return get(**{'phone': phone, "$limit": limit, '$offset': offset,
               '$order': 'inspection_date'})

if __name__ == '__main__':
    l = get_unique_phones()
    for i in l:
        l2 = get_review(i['phone'])
        for j in l2:
            print(j.get('violation_description'))
