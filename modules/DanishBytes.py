from colorama import Fore
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

class DanishBytes():
    def __init__(self, session=None, api_key=None):
        self.s = requests.Session()
        if session != None:
            self.session = session
            self.s.cookies.update({"db_session": self.session})
        if api_key != None:
            self.api_key = api_key
        self.s.headers.update({"User-Agent": "DenGladeFilmMand x DBy Film Søger Script | Fork af Turra"})
        pass
    
    def set_api(self, api_key):
        self.api_key = api_key
        return
    
    def set_session(self, session):
        self.session = session
        self.s.cookies.update({"db_session": self.session})
        return
    
    def authenticate(self):
        options = Options()
        options.headless = False
        driver = webdriver.Firefox(options=options)
        driver.get("https://danishbytes.club/login")
        user = ""
        while user == "":
            try:
                driver.find_element_by_id('partials_userbar')
                user = driver.execute_script('''return document.getElementById('partials_userbar').querySelector('.badge-user strong').innerHTML;''')
            except Exception:
                time.sleep(2)
                pass
        session = driver.get_cookie('db_session')['value']
        driver.close()
        self.session = session
        self.s.cookies.update({"db_session": self.session})
        return [self.session, user]

    def get_api(self):
        headers = {
            "Host": "danishbytes.club",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://danishbytes.club/",
            "DNT": "1",
            "Alt-Used": "danishbytes.club",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        r = self.s.get("https://danishbytes.club/users/Turra/settings/security", headers=headers)
        if r.status_code == 200:
            api_key = BeautifulSoup(r.text, 'html.parser').find(class_='current_api').get_text()
            self.api_key = api_key
            return api_key
        return False

    def find_movie(self, search_name):
        r = self.s.get(f"https://danishbytes2.org/api/torrents/filter?_token=&search={search_name}&uploader=&imdb=&tvdb=&view=list&tmdb=&mal=&igdb=&categories%5B%5D=1&categories%5B%5D=2&categories%5B%5D=5&categories%5B%5D=4&categories%5B%5D=3&categories%5B%5D=8&types%5B%5D=34&types%5B%5D=30&types%5B%5D=1&types%5B%5D=2&types%5B%5D=3&types%5B%5D=4&types%5B%5D=5&types%5B%5D=6&types%5B%5D=33&types%5B%5D=7&types%5B%5D=8&types%5B%5D=9&types%5B%5D=10&types%5B%5D=19&types%5B%5D=14&types%5B%5D=16&types%5B%5D=17&types%5B%5D=18&types%5B%5D=11&types%5B%5D=20&types%5B%5D=21&types%5B%5D=22&types%5B%5D=12&types%5B%5D=13&types%5B%5D=23&types%5B%5D=24&types%5B%5D=25&types%5B%5D=26&types%5B%5D=27&types%5B%5D=28&types%5B%5D=29&types%5B%5D=31&types%5B%5D=32&types%5B%5D=15&resolutions%5B%5D=1&resolutions%5B%5D=2&resolutions%5B%5D=3&resolutions%5B%5D=4&resolutions%5B%5D=5&resolutions%5B%5D=6&resolutions%5B%5D=7&resolutions%5B%5D=8&resolutions%5B%5D=9&resolutions%5B%5D=10&resolutions%5B%5D=11&language_codes%5B%5D=gb&language_codes%5B%5D=dk&language_codes%5B%5D=xx&language_codes%5B%5D=se&language_codes%5B%5D=no&language_codes%5B%5D=fi&language_codes%5B%5D=de&language_codes%5B%5D=es&language_codes%5B%5D=fr&language_codes%5B%5D=is&language_codes%5B%5D=jp&language_codes%5B%5D=it&language_codes%5B%5D=ru&language_codes%5B%5D=cn&language_codes%5B%5D=kr&language_codes%5B%5D=in&language_codes%5B%5D=ae&language_codes%5B%5D=th&language_codes%5B%5D=nl&language_codes%5B%5D=pt&language_codes%5B%5D=ba&language_codes%5B%5D=gr&language_codes_subs%5B%5D=gb&language_codes_subs%5B%5D=dk&language_codes_subs%5B%5D=xx&language_codes_subs%5B%5D=se&language_codes_subs%5B%5D=no&language_codes_subs%5B%5D=fi&language_codes_subs%5B%5D=de&language_codes_subs%5B%5D=es&language_codes_subs%5B%5D=fr&language_codes_subs%5B%5D=is&language_codes_subs%5B%5D=jp&language_codes_subs%5B%5D=it&language_codes_subs%5B%5D=ru&language_codes_subs%5B%5D=cn&language_codes_subs%5B%5D=kr&language_codes_subs%5B%5D=in&language_codes_subs%5B%5D=ae&language_codes_subs%5B%5D=th&language_codes_subs%5B%5D=nl&language_codes_subs%5B%5D=pt&language_codes_subs%5B%5D=ba&language_codes_subs%5B%5D=gr&page=1&qty=25&api_token={self.api_key}")
        if len(r.json()) > 0:
            return r.json()
        r = self.s.get(f"https://danishbytes2.org/api/torrents/filter?_token=&search=&uploader=&imdb={search_name}&tvdb=&view=list&tmdb=&mal=&igdb=&categories%5B%5D=1&categories%5B%5D=2&categories%5B%5D=5&categories%5B%5D=4&categories%5B%5D=3&categories%5B%5D=8&types%5B%5D=34&types%5B%5D=30&types%5B%5D=1&types%5B%5D=2&types%5B%5D=3&types%5B%5D=4&types%5B%5D=5&types%5B%5D=6&types%5B%5D=33&types%5B%5D=7&types%5B%5D=8&types%5B%5D=9&types%5B%5D=10&types%5B%5D=19&types%5B%5D=14&types%5B%5D=16&types%5B%5D=17&types%5B%5D=18&types%5B%5D=11&types%5B%5D=20&types%5B%5D=21&types%5B%5D=22&types%5B%5D=12&types%5B%5D=13&types%5B%5D=23&types%5B%5D=24&types%5B%5D=25&types%5B%5D=26&types%5B%5D=27&types%5B%5D=28&types%5B%5D=29&types%5B%5D=31&types%5B%5D=32&types%5B%5D=15&resolutions%5B%5D=1&resolutions%5B%5D=2&resolutions%5B%5D=3&resolutions%5B%5D=4&resolutions%5B%5D=5&resolutions%5B%5D=6&resolutions%5B%5D=7&resolutions%5B%5D=8&resolutions%5B%5D=9&resolutions%5B%5D=10&resolutions%5B%5D=11&language_codes%5B%5D=gb&language_codes%5B%5D=dk&language_codes%5B%5D=xx&language_codes%5B%5D=se&language_codes%5B%5D=no&language_codes%5B%5D=fi&language_codes%5B%5D=de&language_codes%5B%5D=es&language_codes%5B%5D=fr&language_codes%5B%5D=is&language_codes%5B%5D=jp&language_codes%5B%5D=it&language_codes%5B%5D=ru&language_codes%5B%5D=cn&language_codes%5B%5D=kr&language_codes%5B%5D=in&language_codes%5B%5D=ae&language_codes%5B%5D=th&language_codes%5B%5D=nl&language_codes%5B%5D=pt&language_codes%5B%5D=ba&language_codes%5B%5D=gr&language_codes_subs%5B%5D=gb&language_codes_subs%5B%5D=dk&language_codes_subs%5B%5D=xx&language_codes_subs%5B%5D=se&language_codes_subs%5B%5D=no&language_codes_subs%5B%5D=fi&language_codes_subs%5B%5D=de&language_codes_subs%5B%5D=es&language_codes_subs%5B%5D=fr&language_codes_subs%5B%5D=is&language_codes_subs%5B%5D=jp&language_codes_subs%5B%5D=it&language_codes_subs%5B%5D=ru&language_codes_subs%5B%5D=cn&language_codes_subs%5B%5D=kr&language_codes_subs%5B%5D=in&language_codes_subs%5B%5D=ae&language_codes_subs%5B%5D=th&language_codes_subs%5B%5D=nl&language_codes_subs%5B%5D=pt&language_codes_subs%5B%5D=ba&language_codes_subs%5B%5D=gr&page=1&qty=25&api_token={self.api_key}")
        if len(r.json()) > 0:
            return r.json()
        r = self.s.get(f"https://danishbytes2.org/api/torrents/filter?_token=&search=&uploader=&imdb=&tvdb={search_name}&view=list&tmdb=&mal=&igdb=&categories%5B%5D=1&categories%5B%5D=2&categories%5B%5D=5&categories%5B%5D=4&categories%5B%5D=3&categories%5B%5D=8&types%5B%5D=34&types%5B%5D=30&types%5B%5D=1&types%5B%5D=2&types%5B%5D=3&types%5B%5D=4&types%5B%5D=5&types%5B%5D=6&types%5B%5D=33&types%5B%5D=7&types%5B%5D=8&types%5B%5D=9&types%5B%5D=10&types%5B%5D=19&types%5B%5D=14&types%5B%5D=16&types%5B%5D=17&types%5B%5D=18&types%5B%5D=11&types%5B%5D=20&types%5B%5D=21&types%5B%5D=22&types%5B%5D=12&types%5B%5D=13&types%5B%5D=23&types%5B%5D=24&types%5B%5D=25&types%5B%5D=26&types%5B%5D=27&types%5B%5D=28&types%5B%5D=29&types%5B%5D=31&types%5B%5D=32&types%5B%5D=15&resolutions%5B%5D=1&resolutions%5B%5D=2&resolutions%5B%5D=3&resolutions%5B%5D=4&resolutions%5B%5D=5&resolutions%5B%5D=6&resolutions%5B%5D=7&resolutions%5B%5D=8&resolutions%5B%5D=9&resolutions%5B%5D=10&resolutions%5B%5D=11&language_codes%5B%5D=gb&language_codes%5B%5D=dk&language_codes%5B%5D=xx&language_codes%5B%5D=se&language_codes%5B%5D=no&language_codes%5B%5D=fi&language_codes%5B%5D=de&language_codes%5B%5D=es&language_codes%5B%5D=fr&language_codes%5B%5D=is&language_codes%5B%5D=jp&language_codes%5B%5D=it&language_codes%5B%5D=ru&language_codes%5B%5D=cn&language_codes%5B%5D=kr&language_codes%5B%5D=in&language_codes%5B%5D=ae&language_codes%5B%5D=th&language_codes%5B%5D=nl&language_codes%5B%5D=pt&language_codes%5B%5D=ba&language_codes%5B%5D=gr&language_codes_subs%5B%5D=gb&language_codes_subs%5B%5D=dk&language_codes_subs%5B%5D=xx&language_codes_subs%5B%5D=se&language_codes_subs%5B%5D=no&language_codes_subs%5B%5D=fi&language_codes_subs%5B%5D=de&language_codes_subs%5B%5D=es&language_codes_subs%5B%5D=fr&language_codes_subs%5B%5D=is&language_codes_subs%5B%5D=jp&language_codes_subs%5B%5D=it&language_codes_subs%5B%5D=ru&language_codes_subs%5B%5D=cn&language_codes_subs%5B%5D=kr&language_codes_subs%5B%5D=in&language_codes_subs%5B%5D=ae&language_codes_subs%5B%5D=th&language_codes_subs%5B%5D=nl&language_codes_subs%5B%5D=pt&language_codes_subs%5B%5D=ba&language_codes_subs%5B%5D=gr&page=1&qty=25&api_token={self.api_key}")
        if len(r.json()) > 0:
            return r.json()
        r = self.s.get(f"https://danishbytes2.org/api/torrents/filter?_token=&search=&uploader=&imdb=&tvdb=&view=list&tmdb={search_name}&mal=&igdb=&categories%5B%5D=1&categories%5B%5D=2&categories%5B%5D=5&categories%5B%5D=4&categories%5B%5D=3&categories%5B%5D=8&types%5B%5D=34&types%5B%5D=30&types%5B%5D=1&types%5B%5D=2&types%5B%5D=3&types%5B%5D=4&types%5B%5D=5&types%5B%5D=6&types%5B%5D=33&types%5B%5D=7&types%5B%5D=8&types%5B%5D=9&types%5B%5D=10&types%5B%5D=19&types%5B%5D=14&types%5B%5D=16&types%5B%5D=17&types%5B%5D=18&types%5B%5D=11&types%5B%5D=20&types%5B%5D=21&types%5B%5D=22&types%5B%5D=12&types%5B%5D=13&types%5B%5D=23&types%5B%5D=24&types%5B%5D=25&types%5B%5D=26&types%5B%5D=27&types%5B%5D=28&types%5B%5D=29&types%5B%5D=31&types%5B%5D=32&types%5B%5D=15&resolutions%5B%5D=1&resolutions%5B%5D=2&resolutions%5B%5D=3&resolutions%5B%5D=4&resolutions%5B%5D=5&resolutions%5B%5D=6&resolutions%5B%5D=7&resolutions%5B%5D=8&resolutions%5B%5D=9&resolutions%5B%5D=10&resolutions%5B%5D=11&language_codes%5B%5D=gb&language_codes%5B%5D=dk&language_codes%5B%5D=xx&language_codes%5B%5D=se&language_codes%5B%5D=no&language_codes%5B%5D=fi&language_codes%5B%5D=de&language_codes%5B%5D=es&language_codes%5B%5D=fr&language_codes%5B%5D=is&language_codes%5B%5D=jp&language_codes%5B%5D=it&language_codes%5B%5D=ru&language_codes%5B%5D=cn&language_codes%5B%5D=kr&language_codes%5B%5D=in&language_codes%5B%5D=ae&language_codes%5B%5D=th&language_codes%5B%5D=nl&language_codes%5B%5D=pt&language_codes%5B%5D=ba&language_codes%5B%5D=gr&language_codes_subs%5B%5D=gb&language_codes_subs%5B%5D=dk&language_codes_subs%5B%5D=xx&language_codes_subs%5B%5D=se&language_codes_subs%5B%5D=no&language_codes_subs%5B%5D=fi&language_codes_subs%5B%5D=de&language_codes_subs%5B%5D=es&language_codes_subs%5B%5D=fr&language_codes_subs%5B%5D=is&language_codes_subs%5B%5D=jp&language_codes_subs%5B%5D=it&language_codes_subs%5B%5D=ru&language_codes_subs%5B%5D=cn&language_codes_subs%5B%5D=kr&language_codes_subs%5B%5D=in&language_codes_subs%5B%5D=ae&language_codes_subs%5B%5D=th&language_codes_subs%5B%5D=nl&language_codes_subs%5B%5D=pt&language_codes_subs%5B%5D=ba&language_codes_subs%5B%5D=gr&page=1&qty=25&api_token={self.api_key}")
        if len(r.json()) > 0:
            return r.json()
        return None
    
    def get_torrent(self, id):
        return self.s.get(f"https://danishbytes2.org/api/torrents/{id}?api_token={self.api_key}").json()

    def download_torrent(self, link):
        r = self.s.get(link)
        torrent = b''
        for data in r.iter_content(chunk_size=4096):
            torrent += data
        return torrent