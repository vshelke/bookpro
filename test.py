
import time, datetime, base64, hmac, requests, urllib
from hashlib import sha256



secret_key = "wYUj3/mnVIkHyrCm4RqM6U2Pwm+6CbMv8wZzJe1P"
a = "AWSAccessKeyId=AKIAJKBJSCFX6V2ODHAA&AssociateTag=bookpro3301-21&Keywords=zero%20to%20one&Operation=ItemSearch&ResponseGroup=Images%2CItemAttributes%2COffers&SearchIndex=Books&Service=AWSECommerceService&Timestamp=2017-12-12T14%3A30%3A32.000Z"
signature = "vKv1DSGyCP21%2FTubfv6%2FlCQjYRkhPjwJv26f34yWpg0%3D"

endpoint = "webservices.amazon.in"
uri = "/onca/xml"

payload = {
    'AWSAccessKeyId': 'AKIAJKBJSCFX6V2ODHAA',
    'AssociateTag': 'bookpro3301-21',
    'Keywords': 'zero to one',
    'Operation': 'ItemSearch',
    'ResponseGroup': 'Images,ItemAttributes,Offers',
    'SearchIndex': 'Books',
    'Service': 'AWSECommerceService',
    'Timestamp': '2017-12-12T14:30:32.000Z',
}
x = urllib.parse.urlencode(payload).replace('+', '%20')
print (a)
print (x)
string_to_sign = "GET\n"+endpoint+"\n"+uri+"\n"+x
dig = hmac.new( bytes(secret_key,'ascii'), msg=bytes(string_to_sign, 'ascii'), digestmod=sha256)
sig = base64.b64encode(dig.digest())
print (sig)
print (signature)
