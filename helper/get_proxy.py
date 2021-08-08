import requests
from lxml.html import fromstring

def get_proxies():
    url = 'https://free-proxy-list.net/'

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print ("Connection Error")
        # print (e)
        return
      
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:80]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def refresh_proxy():
    proxies = get_proxies()

    if (proxies==None):
        print("No proxy. Using old ones")
        return


    with open('db/proxies.txt', 'w') as the_file:
        for p in proxies:
            the_file.write( p +'\n')

    print("Got",len(proxies),"proxy")