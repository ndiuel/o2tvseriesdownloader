import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from errors import *

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = None


headers = {'authority': 'o2tvseries.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_series_link(series):
    r = requests.get('https://google.com/search',
                     params={'q': f'site:o2tvseries.com {series}'})
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        first_tag = soup.select('.kCrYT > a')[0]
        link = first_tag['href'].split("=")[1].split("&")[0]
        return link
    except:
        raise SeriesNotFound(f"could not find {series}")


def get_season_link(series_link, season):
    r = requests.get(series_link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    for l in soup.select('.data'):
        num = int(l.text.split(" ")[1])
        if num == season:
            try:
                return l.select('a')[0]['href']
            except:
                pass 
    raise SeasonNotFound(f"season {season} not found")


def get_episode_link(season_link, episode):
    def _episode_link(soup):
        for l in soup.select('.data'):
            num = int(l.text.split(" ")[1])
            if num == episode:
                try:
                    return l.select('a')[0]['href']
                except:
                    pass

    r = requests.get(season_link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    pages = [l['href'] for l in soup.select(".pagination a")]
    link = _episode_link(soup)

    if link:
        return link

    for p in pages:
        r = requests.get(p, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        link = _episode_link(soup)
        if link:
            return link
    
    raise EpisodeNotFound(f"episode {episode} not found")


def get_captcha_link(episode_link):
    r = requests.get(episode_link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        url = [l for l in soup.select('.data a') if l['href'] != "#"][-2]['href']
        r = requests.get(url, headers=headers)
        return r.url
    except:
        raise CaptchaLinkNotFound("could not find captcha")


def _get_download_link(captcha_link):
    global driver
    driver = driver or webdriver.Firefox(options=options)
    driver.get("https://o2tvseries.com/areyouhuman.php?fid=54646")
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe")))
    try:
        driver.find_element_by_tag_name('span').click()
    except:
        pass
    driver.switch_to.default_content()
    content = driver.find_element(By.CSS_SELECTOR, value="form>img")
    content.screenshot('content.png')
    answer = solve_captcha('content.png').replace(" ", "")    
    s = requests.Session()
    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)
    r = s.post(captcha_link, data={'captchainput': answer, 'submit': 'Continue Download'}, headers=headers, allow_redirects=True, stream=True)
    return r.url


def get_download_link(captcha_link):
    for _ in range(15):
        try:
            url = _get_download_link(captcha_link)
            arr = url.replace('http://', "")
            if arr.startswith('d'):
                return url
        except Exception as e:
            print(e)
    
    raise DownloadLinkNotFound("could not find download link")


def download_video(download_link, filename):
    r = requests.get(download_link, stream = True) 
    with open(filename, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk) 
    

def solve_captcha(file):
    image = cv2.imread(file)
    return pytesseract.image_to_string(image, lang="eng", config="--psm 6")


def download(series, season, episode):
    series_link = get_series_link(series)
    season_link = get_season_link(series_link, season)
    episode_link = get_episode_link(season_link, episode)
    captcha_link = get_captcha_link(episode_link)
    download_link = get_download_link(captcha_link)
    download_video(download_link, f'{series.capitalize()}-Season {season}- Episode {episode}.mp4')


def download_link(series, season, episode):
    series_link = get_series_link(series)
    season_link = get_season_link(series_link, season)
    episode_link = get_episode_link(season_link, episode)
    captcha_link = get_captcha_link(episode_link)
    download_link = get_download_link(captcha_link)
    return download_link



