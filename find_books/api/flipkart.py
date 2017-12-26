import requests, json


def flipkart(s):
    token = '04f324321327484e85658ec6c396993b'
    aff_id = 'bookpro3301'
    headers = {
        'Fk-Affiliate-Id': aff_id,
        'Fk-Affiliate-Token': token,
    }
    params = {
        'query': s,
        'resultCount': 10,
    }
    endpoint = 'https://affiliate-api.flipkart.net/affiliate/1.0/search.json'
    r = requests.get(endpoint, params=params, headers=headers)
    data = json.loads(r.text)['productInfoList']
    if len(data) > 0:
        pass
    else:
        return -1
    data = data[0]
    comp = {
        'title': data['productBaseInfoV1']['title'],
        'author': data['categorySpecificInfoV1']['booksInfo']['authors'],
        'offer_link': '',#data['productBaseInfoV1']['offers'],
        'link': data['productBaseInfoV1']['productUrl'],
        'image': data['productBaseInfoV1']['imageUrls']['400x400'],
        'price': float(data['productBaseInfoV1']['flipkartSpecialPrice']['amount']),
        'ISBN': data['categorySpecificInfoV1']['keySpecs'],
        'provider': 'https://www.underconsideration.com/brandnew/archives/flipkart_logo_detail.jpg'
    }
    return comp
