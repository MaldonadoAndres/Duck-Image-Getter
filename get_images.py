import requests
import re
import json
import time
import logging
import urllib
import os
import glob
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

current_path = "/home/amaldonado/dev/mamamoo_nn/"


def search(keywords, max_results):
    search_term = keywords.split(" ")
    new_current_path = current_path + "{}/".format(search_term[0])
    try:
        dir_name = search_term[0]
        os.makedirs(dir_name)
        print("Directory ", dir_name,  " Created ")
    except FileExistsError:
        print("Directory ", dir_name,  " already exists")
    url = 'https://duckduckgo.com/'
    params = {
        'q': keywords
    }

    logger.debug("Hitting DuckDuckGo for Token")

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)

    if not searchObj:
        logger.error("Token Parsing Failed !")
        return -1

    logger.debug("Obtained Token")

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js"

    logger.debug("Hitting Url : %s", requestUrl)
    while True:
        counter = len(glob.glob1(new_current_path, "*.jpg")) + 1
        while True:
            try:
                res = requests.get(requestUrl, headers=headers, params=params)
                data = json.loads(res.text)
                break
            except ValueError as e:
                logger.debug(
                    "Hitting Url Failure - Sleep and Retry: %s", requestUrl)
                time.sleep(5)
                continue

        logger.debug("Hitting Url Success : %s", requestUrl)
        printJson(data["results"], path=new_current_path,
                  max_results=max_results)
        if "next" not in data:
            logger.debug("No Next Page - Exiting")
            exit(0)
        if counter > max_results:
            logger.debug("Maximum results reached")
            break

        requestUrl = url + data["next"]


def printJson(objs, path, max_results):
    for obj in objs:
        try:
            counter = len(glob.glob1(path, "*.jpg")) + 1
            if(counter > max_results):
                break
            file_path = "{}000{}.jpg".format(path, counter)
            print(file_path)
            urllib.request.urlretrieve(
                obj["image"], filename=file_path)
            print("Downloading Image...")

        except Exception as exception:
            print("Error downloading Caused by -> {}".format(exception))


girls = ["yeri red velvet", "wendy red velvet",
         "irene red velvet", "joy red velvet", "seulgi red velvet"]
for girl in girls:
    search(girl, max_results=1000)
