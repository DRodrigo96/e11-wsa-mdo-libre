# ./scripts/proxies.py
# proxies provider: https://free-proxy-list.net/
# ==================================================
# standard
from urllib.request import Request, urlopen
import re
# requirements
from bs4 import BeautifulSoup
# --------------------------------------------------

def retrieve_proxies() -> None:
    
    req = Request('https://free-proxy-list.net/', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    
    soup = BeautifulSoup(webpage, 'html.parser')
    ip_tags = [tag.contents for tag in soup('td')]
    
    proxies = []
    for tag in ip_tags:
        if len(tag) == 1 and isinstance(t := tag[0], str):
            if len(vt := re.findall('^[0-9.]*$', t)) == 1:
                    proxies.append(vt[0])
            else:
                continue
        else:
            continue
    
    status = []
    for tag in ip_tags:
        if len(tag) == 1 and isinstance(t := tag[0], str):
            if ('yes' or 'no') in tag:
                status.append(tag)
    
    status = ip_tags[6::8]
    status = [x[0] for x in status]
    status = status[:-19]
    
    ips, ports = [], []
    
    for x in proxies[::2]:
        if '.' in x:
            ips.append(x)
    
    i = int()
    while True:
        ports.append(proxies[1::2][i])
        i += 1
        
        if len(ports) == len(ips):
            del i
            break
    
    my_proxies = []
    for x, y, z in zip(ips, ports, status):
        my_proxies.append(('{}:{}'.format(x,y), z))
    
    pos_proxies = [proxy for proxy, x in my_proxies if x == 'yes']
    
    with open('./temp/POS_PROXIES.txt', 'w') as proxieFile:
        for proxie in pos_proxies:
            proxieFile.write('{p}\n'.format(p=proxie))
