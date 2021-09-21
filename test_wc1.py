import pytest
from works.wc1 import NewsScrapper


def test_newsscrapper_keyword():
    test_keyword = 'python'

    t = NewsScrapper(keyword=test_keyword)
    info = t.info()

    assert test_keyword == info['keyword'], "search keyword must be equal"


def test_newsscrapper_maximum():
    test_keyword = 'python'
    test_max_page = 100

    t = NewsScrapper(keyword=test_keyword, maxpages=test_max_page)
    info = t.info()

    assert test_keyword == info['keyword']
    assert info['maximum'] == 50 if test_max_page > 50 else test_max_page, "search maximum not greater than 50"


def test_newsscrapper_gather():
    NEWS_PER_PAGE = 10
    test_max_page = 1

    t = NewsScrapper(keyword='test', maxpages=test_max_page)
    news_count = len(t.gather())

    assert NEWS_PER_PAGE * test_max_page == news_count, "news count = 10 * maximum page"
