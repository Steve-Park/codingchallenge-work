# codingchallenge-work
## 사이트 선정 기준
* 사이트의 Hit 수가 도움이 될 것
* 사이트에서 Scrapping 을 허용할 것 (robots.txt 파일 확인)
* 콘텐츠의 저작권 등에 문제가 없을 것
1. 네이버 뉴스 : 키워드 기반의 뉴스 기사 조회 > NewsScrapper
2. 포탈 사이트 : 키워드 기반의 이미지 검색 > ImageScrapper


## NewsScrapper
### 1. 사이트 분석
* 로그인 여부와 관계 없이 동작
* JavaScript 등을 통한 HTML 페이지 표시 후 rendering 없음
* 여러 페이지를 동시 요청 가능
* URL 구조
> https://search.naver.com/search.naver?where=news&query={검색어}&start={(page_no -1)*10+1}
* 화면 예시
![검색화면 예시](./images/naver-news-sample.png)
### 2. class 구성
* requests, urllib.parse, beautifulsoup 등 사용
  * requests: 웹 페이지 요청
  * urllib.parse: quote 를 통한 한글 검색어 처리
  * beautifulsoup: 웹 페이지 parsing, CSS Selector 사용
* `__init__` : 검색어 및 최대 스크래핑 페이지 수 (default: 20)
* 각 함수의 로그성 메시지는 화면에 표시하고 호출 단계에 따라 tab 으로 들여쓰기
* 클래스 사용 시 gather 함수를 통하여 ayncio 에 대한 사용자 고려 없이 호출하도록 구성
* 비동기 호출 구조 : gather() -> __scrap_main() -> __scrap_page()
    * `gather()` : 호출 사용자 편리성 제공
    * `__scrap_main()` : 기본 10개의 scrap_page 르 비동기 호출
    * `__scrap_page()` : 1~10초 중 임의 대기 호 1개의 패이지 스크래핑
```
def gather():
  await asyncio.run(self.__scrap_main())

async def __scrap_main():
  for page in range(start + 1, end + 1):
    scrapper.append(asyncio.create_task(self.__scrap_page(page,header)))
 
  await asyncio.gather(*scrapper)

async def __scrap_page():
  await asyncio.sleep(1000)
```
