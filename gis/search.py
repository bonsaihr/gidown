import json
from imghdr import what
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from gis.advanced import QuerySettings


class GoogleSearchImage:

    def __init__(self, google_json_dict: dict):

        self.image_url = google_json_dict["ou"]
        self.thumbnail_url = google_json_dict["tu"]

        self.source_page_url = google_json_dict["ru"]
        self.source_domain = google_json_dict["isu"]

        self.title = "pt"
        self.description = "s"

        self.width = google_json_dict["ow"]
        self.height = google_json_dict["oh"]

        self.small_width = google_json_dict["tw"]
        self.small_height = google_json_dict["th"]
        self.type = google_json_dict["ity"]
        self.thumbnail_type = google_json_dict["ity"]

        self.image = None
        self.thumbnail = None

    def __eq__(self, other):
        if not hasattr(other, "image_url"):
            return False
        return self.image_url == other.image_url

    def __hash__(self):
        return hash(self.image_url)

    def __str__(self):
        return "Downloadable {} at {}".format(self.type, self.image_url)

    def download(self, download_all=False) -> None:
        self.image = requests.get(self.image_url).content
        if download_all:
            self.download_thumbnail()
        ext = what(None, self.image)
        self.type = ext if ext is not None else self.type

    def download_thumbnail(self) -> None:
        self.thumbnail = requests.get(self.thumbnail_url).content
        ext = what(None, self.image)
        self.thumbnail_type = ext if ext is not None else self.thumbnail_type

    def _save(self, img_data, filename):
        with open(filename, "wb") as fout:
            fout.write(img_data)

    def save(self, filename, auto_extension=False):
        if self.image is None:
            self.download()

        if auto_extension:
            filename = "{}.{}".format(filename, self.type)
        self._save(self.image, filename)

    def save_thumbnail(self, filename, auto_extension=False):
        if self.thumbnail is None:
            self.download_thumbnail()

        if auto_extension:
            filename = "{}.{}".format(filename, self.thumbnail_type)
        self._save(self.thumbnail, filename)


class Request:
    _user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

    def __init__(self):
        self._url = "https://www.google.hr/search"
        self._headers = {'User-Agent': Request._user_agent}

    def _generate_url(self, query, settings, autocorrect=False):
        q = {"tbm": "isch",
             "tbs": QuerySettings(settings).urlencode(),
             "q": quote_plus(query.strip()),
             "source": "lnms"}
        if not autocorrect:
            q["nfpr"] = 1
        return "{}?{}".format(self._url, "&".join("{}={}".format(k, v) for k, v in q.items()))

    def _fetch_html(self, url):
        req = requests.get(url, headers=self._headers)
        html_doc = req.text
        return html_doc

    def image_query(self, query, *settings, autocorrect=False):
        url = self._generate_url(query, settings, autocorrect)
        html = self._fetch_html(url)

        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.find_all("div", {"class": "rg_meta"})

        return list(set(GoogleSearchImage(json.loads(div.text)) for div in divs))
