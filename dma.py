#!/usr/bin/python3

#sudo docker pull scrapinghub/splash
#sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
#To reclaim some RAM send a POST request to "curl -X POST http://localhost:8050/_gc"
#To ping Splash instance send a GET request to "curl http://localhost:8050/_ping"

import datetime
import requests
from random import choice
import csv

startTime = datetime.datetime.now()

splash_host_port = 'http://localhost:8050'

user_agents = [
    'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
    'Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)',
    'Opera/9.52 (X11; Linux i686; U; en)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 GTB7.1'
]


def ping():
    random_user_agent = choice(user_agents)
    headers = {'User-Agent': random_user_agent}
    response = requests.get(splash_host_port + '/_ping', headers=headers, timeout=30)
    return response.json()


def remove_protocols(string):
    string_replaced = string.replace('http://', '').replace('https://', '').replace('www.', '').replace('//', '')
    return string_replaced


def scrape(domain):

    params = {"url": domain, "wait": 0.1, "with_timeout": 30, "har": 1, "html": 1, "iframes ": 1}

    random_user_agent = choice(user_agents)
    headers = {'User-Agent': random_user_agent}

    data = {}
    try:
        response_json = requests.get(splash_host_port + '/render.json', params=params, headers=headers, timeout=30)
        data = response_json.json()
        data['domain'] = remove_protocols(domain)
        data['status_code'] = response_json.status_code
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        data['domain'] = remove_protocols(domain)
        data['status_code'] = 0
        pass

    #pprint.pprint(data)
    #f = open("logs/" + remove_protocols(domain) + "_log.json", "w")
    #f.write(str(data))
    #f.close()

    return data


if __name__ == '__main__':

    with open("lists/top-1m.csv", "r") as f:
        reader = csv.reader(f)
        ping = ping()
        print(ping)
        i = 1
        for row in reader:
            if i <= 100 and ping['status'] == 'ok':
                domain = str(row[1])
                result = scrape('http://' + domain)
                status_code = str(result['status_code'])
                runTime = datetime.datetime.now()
                runtime = str(runTime - startTime)[0:7]
                avg_runtime = str((runTime - startTime) / i)[0:7]
                print(str(i) + ' | ' + runtime + ' | ' + avg_runtime + ' | ' + status_code + ' | ' + domain)
                i += 1
            else:
                exit(0)



