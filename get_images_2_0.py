import requests
import re
import json
import time
import logging
import coloredlogs
import urllib
import os
import glob
import pathlib
import utils as Utils


def search(keyword, max_results):
    dir_name = Utils.getDirName(keyword)
    download_path = "{}/{}/".format(current_path, dir_name)
    try:
        os.makedirs(dir_name)
    except Exception as exception:
        logger.error("This directory alredy exists -> {}".format(dir_name))
    params = {'q': keyword}
    logger.info("Hitting DuckDuckGo for Token")
    res = requests.post(URL, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M | re.I)
    if not searchObj:
        logger.error("Token Parsing Failed !")
        return -1
    logger.info("Obtained Token")
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
    # TODO Remove .gif from petition
    params = {
        'l': 'us_en',
        'o': 'json',
        'q': keyword,
        'vqd': searchObj.group(1),
        'f': ',,,',
        'p': '-1',
        'v7exp': 'a'
    }
    request_url = URL+'i.js'
    logger.info("Hitting Url : {}".format(request_url))
    while True:
        downloaded_files_count = len(glob.glob1(download_path, "*.jpg"))
        json_data = request_json(request_url=request_url,
                                 headers=headers, params=params)
        if max_results is not None and downloaded_files_count > max_results:
            logger.info("Max results reached moving to next one main loop")
            break
        else:
            download_images(
                images=json_data["results"], download_path=download_path)

        if "next" not in json_data:
            logger.info(
                "No more images for query -> {} moving to next one".format(girl))
            break
        request_url = URL + json_data["next"]
        logger.info("Getting next batch of images")
    pass
    logger.info("Continuing to next girl")


def request_json(request_url, headers, params):
    while True:
        try:
            res = requests.get(url=request_url, headers=headers, params=params)
            res.url
            print(res.url)
            data = json.loads(res.text)
            return data
        except Exception as exception:
            logger.error(
                "Getting URL -> {} Failed by -> {}".format(request_url, exception))
            logger.info(
                "Retrying in 5 seconds")
            time.sleep(5)
            continue
        pass


def download_images(images, download_path):
    for image in images:
        files_count = len(glob.glob1(download_path, "*.jpg"))
        if max_results is not None and files_count > max_results:
            logger.info(
                "Max results reached moving to next one download_images")
            break
            pass
        try:
            filename = "{}000{}.jpg".format(
                download_path, files_count)
            urllib.request.urlretrieve(image["image"], filename)
            logger.info(
                "Downloading file ->{} Title -> {}".format(filename, image["title"]))
        except Exception as exception:
            logger.error(
                "Error downloading image. Caused by -> {}".format(exception))
    pass


if __name__ == "__main__":
    URL = 'https://duckduckgo.com/'
    max_results = None
    logging.basicConfig(filename='test_logs.log',
                        filemode='w', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)
    current_path = pathlib.Path(__file__).parent.absolute()
    girls = ["yeri red velvet", "wendy red velvet",
             "irene red velvet", "joy red velvet", "seulgi red velvet"]
    for girl in girls:
        search(girl, max_results=max_results)
    pass
