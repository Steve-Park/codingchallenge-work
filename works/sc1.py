from urllib import parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from datetime import datetime
import os
import ssl
import time


class ImageScrapper:
    def __init__(self, keyword, maximages=100, location='', debug_mode: bool = True):
        """다음 이미지 스크래퍼 생성사 - 초기 설정

        Args:
            keyword ([str]): [검색어]
            maximages (int, optional): [최대 스크래핑 이미지 수]. Defaults to 100.
            location (str, optional): [스크래핑 이미지 저장 위치]. Defaults to ''.
            debug_mode (bool, optional): [디버그 로그 출력 여부]. Defaults to True.
        """
        self.baseurl = f'https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q={parse.quote(keyword)}'
        self.keyword = keyword
        self.current = 0
        self.maximum = 100 if maximages > 100 else maximages
        self.max_images_per_pages = 80
        self.location = os.path.abspath(
            location) if location else os.path.abspath(f'./{keyword}')
        self.start = None
        self.end = None
        self.debug_mode = debug_mode

    def gather(self):
        """이미지 스크래핑 및 저장

        Raises:
            e: [진행 중 발생하는 Exception]
        """
        browser = None
        chrome_options = Options()

        # selenium object 초기화
        if not self.debug_mode:
            # hide selenium
            chrome_options.add_argument('--headless')
        else:
            # avoid selenium closing
            # chrome_options.add_experimental_option("detach", True)
            pass

        browser = webdriver.Chrome(
            executable_path='./webdriver/chromedriver', options=chrome_options)
        # browser.maximize_window()

        # implicit wait time = 5 초
        browser.implicitly_wait(5)

        # requests.urlretrieve 실행 시 ssl 오류 수정
        ssl._create_default_https_context = ssl._create_unverified_context

        # 저장 위치 존재 여부 확인 및 재구성
        if self.debug_mode and os.path.exists(self.location):
            for f in os.listdir(self.location):
                os.remove(os.path.join(self.location, f))
            os.rmdir(self.location)

        os.mkdir(self.location)

        start = time.perf_counter()
        self.start = datetime.now()

        try:
            # 검색 대상 페이지 오픈 및 한 페이지 당 80개의 이미지만 있으므로 하단 버튼 클릭하여 80개 더 확보
            browser.get(self.baseurl)

            for idx in range(1, (self.maximum // self.max_images_per_pages) + 2):
                # 아래의 XPATH 객체는 non clickable object error 발생으로 implicit wait + scroll down 으로 변경
                # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="imgColl"]/div[5]/a[1]'))).click()
                time.sleep(5)
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                browser.execute_script(f"window.scrollTo(0, {5000 * idx});")

            # HTML parsing
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            images = soup.find_all('img', class_='thumb_img')

            # 이미지 저장
            for image in images:
                file_name = f'{self.location}/{self.current:03d}.jpeg'
                urlretrieve(image['src'], file_name)
                self.current += 1
                self.debug_mode and print(
                    f"\t[gather] url: {image['src']} -> file: {file_name}")

                if self.current >= self.maximum:
                    break
        except Exception as e:
            self.debug_mode and print(f"\t[gather] error : {e}")
            raise e
        finally:
            browser.quit()
            self.debug_mode and print(
                f'\t[gather] elipsed time: {time.perf_counter() - start:0.2f} seconds')
            self.end = datetime.now()

    def info(self):
        """환경 설정 확인용 함수
        """
        info = {
            'baseurl': self.baseurl,
            'keyword': self.keyword,
            'location': self.location,
            'current': self.current,
            'maximum': self.maximum,
            'start': self.start,
            'end': self.end
        }

        if self.debug_mode:
            print(f'[imagescrapper-info]')
            for key, value in info.items():
                print(f'\t{key} : {value}')

        return info


if __name__ == '__main__':
    scrapper = ImageScrapper(keyword='아이유', maximages=10, debug_mode=False)

    scrapper.gather()
    # print(scrapper.info())
