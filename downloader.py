headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_series_link(series):
    pass


def get_season_link(series_link):
    pass


def episode_link(season_link):
    pass


def get_download_link(season_link):
    pass


def get_download_link(download_link):
    pass


def download(series, season, episode):
    r = requests.get('https://google.com/search',
                     params={'q': 'site:o2tvseries.com the originals'})
