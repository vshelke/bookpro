import requests, json
from config import FlipkartConfig

def flipkart(s):
    token = FlipkartConfig.token
    aff_id = FlipkartConfig.aff_id
    headers = {
        'Fk-Affiliate-Id': aff_id,
        'Fk-Affiliate-Token': token,
    }
    params = {
        'query': s + ' book',
        'resultCount': 10,
    }
    endpoint = FlipkartConfig.endpoint
    r = requests.get(endpoint, params=params, headers=headers)
    data_dict = json.loads(r.text)

    # with open('flipkart_data.json', 'w') as f:
    #     json.dump(data_dict, f, indent=4)

    if len(data_dict['productInfoList']) <= 0:
        return None

    data = data_dict['productInfoList']
    comp = []
    for product in data:
        title = ''
        author = ''
        ISBN = ''
        offer_link = ''
        image = ''
        price = None
        link = ''
        if 'productBaseInfoV1' in product:
            base = product['productBaseInfoV1']
            title = base['title'] if 'title' in base else ''
            link = base['productUrl'] if 'productUrl' in base else ''
            if 'imageUrls' in base:
                image = base['imageUrls']['400x400'] if '400x400' in base['imageUrls'] else ''
            if 'flipkartSpecialPrice' in base and base['flipkartSpecialPrice']:
                price = float(base['flipkartSpecialPrice']['amount']) if 'amount' in base['flipkartSpecialPrice'] else None
            if 'offers' in base:
                offer_link = base['offers'] if len(base['offers']) > 0 else ''
        if 'categorySpecificInfoV1' in product:
            base2 = product['categorySpecificInfoV1']
            if 'booksInfo' in base2:
                author = ','.join(base2['booksInfo']['authors']) if 'authors' in base2['booksInfo'] else ''
            if 'keySpecs' in base2:
                ISBN = '<br>'.join(base2['keySpecs'])
        comp.append({
            'title': title,
            'author': author,
            'offer_link': offer_link,
            'link': link,
            'image': image,
            'price': price,
            'ISBN': ISBN,
            'provider': 'https://www.underconsideration.com/brandnew/archives/flipkart_logo_detail.jpg'
        })
    return comp
