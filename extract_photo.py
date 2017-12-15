import argparse
import re
import requests

from os import path
from urllib.parse import urlparse

pattern = re.compile(r'\"display_url\":\s\"(https:\/\/[\w.\/-]+)\"')


class InstagramPhotoExtractor:
    def __init__(self, url):
        self.url = url

    def execute(self):
        response = requests.get(self.url)
        match = pattern.search(response.text)
        if match and match.group(1):
            self.photo_url = match.group(1)
            response = requests.get(match.group(1))

            self.save_file(response.content)

    def save_file(self, data):
        url_components = urlparse(self.photo_url)
        filename = path.basename(url_components.path)
        with open(filename, 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', type=str, required=True,
                        help='Instagram Post URL')

    args = parser.parse_args()

    backup = InstagramPhotoExtractor(**vars(args))
    backup.execute()
