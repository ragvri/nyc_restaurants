from credential import Yelp
import json, requests

def get_info(phone, locale='en_US'):
    if '+1' != phone[0:2]:
        phone = '+1' + phone

    headers = {'Authorization': 'Bearer %s' % Yelp.KEY.value}
    url='https://api.yelp.com/v3/businesses/search/phone'
    params = {'phone': phone, 'locale': locale}
    req = requests.get(url, params=params, headers=headers)

    # proceed only if the status code is 200
    if req.status_code != 200:
        print('The status code is {}, please try again.'.format(req.status_code))
        return []
    # printing the text from the response
    result = json.loads(req.text)
    remaining = req.headers.get('RateLimit-Remaining')
    if remaining and int(remaining) % 100 == 0:
        print('remaining limit', remaining)
    return (result['businesses'])

if __name__ == '__main__':
    print(get_info('2129577500'))
