import os

import requests
from tqdm import *

import settings


def download_file(url):
    # get the file name from the url
    filename = os.path.basename(url)
    # stream url data
    with requests.get(url, stream=True) as req:
        # raise http error if exists
        req.raise_for_status()
        # try to open the file name, catch any exceptions for incorrect
        # filename, this is likely due to the url ending in `/` or not a direct file download
        try:
            with open(filename, 'wb') as file:
                # start progress bar, set total from content length header and description from filename
                bar = tqdm(total=int(req.headers['Content-Length']), desc=filename)
                # chunk the request and loop the data
                for chunk in req.iter_content(chunk_size=8192):
                    # write this chunk to file
                    file.write(chunk)
                    # update progress bar
                    bar.update(len(chunk))
        except FileNotFoundError:
            print('Invalid download url [%s], please make sure it\'s a direct link to the file.' % url)
        except OSError:
            print('Invalid download url [%s], please make sure it\'s a direct link to the file.' % url)


if __name__ == '__main__':
    if settings.INSTALL_REQ:
        os.system('pip install -r requirements.txt')

    with open('download.txt', 'r') as downloads:
        for download in downloads.read().split('\n'):
            download_file(download)
