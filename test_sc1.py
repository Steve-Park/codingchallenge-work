import pytest
from works.sc1 import ImageScrapper
import os


def test_imagescrapper_keyword():
    test_keyword = 'python'

    t = ImageScrapper(keyword=test_keyword)
    info = t.info()

    assert test_keyword == info['keyword'], "search keyword must be equal"


def test_imagescrapper_maximum():
    test_keyword = 'python'
    test_max_images = 10

    t = ImageScrapper(keyword=test_keyword, maximages=test_max_images)
    info = t.info()

    assert test_keyword == info['keyword']
    assert info['maximum'] == 100 if test_max_images > 100 else test_max_images, "search maximum not greater than 100"


def test_newsscrapper_gather():
    test_keyword = 'python'
    test_max_images = 10

    t = ImageScrapper(keyword=test_keyword,
                      maximages=test_max_images, debug_mode=False)
    t.gather()
    info = t.info()

    assert len(os.listdir(info['location'])) == test_max_images

    if os.path.exists(info['location']):
        for f in os.listdir(info['location']):
            os.remove(os.path.join(info['location'], f))
        os.rmdir(info['location'])
