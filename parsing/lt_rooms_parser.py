from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
from .models import Hotel
import os

def start(d, m, y, country, nights, stars):
    chrome_driver = os.path.join(BASE_DIR, 'parsing/chromedriver')
    chrome_option = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", prefs)
    chrome_option.add_argument("headless")

    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_option)

    # class HotelWithEmptyRooms(object):
    #     def __init__(self, name, stars, country, num_empty_rooms, href):
    #         self.name = name
    #         self.stars = stars
    #         self.country = country
    #         self.num_empty_rooms = num_empty_rooms
    #         self.href = href

    hotel_urls = []

    def url_collector():
        try:
            urls = driver.find_elements_by_xpath("//div[@class='faded-link']//a")
            for h_url in urls:
                h_href = h_url.get_attribute('href')
                #  проверить если элемента нет то добавить
                if h_href not in hotel_urls:
                    hotel_urls.append(h_href)
        except StaleElementReferenceException:
            pass

    def scrolling():
        scrolling_place = True
        while scrolling_place:
            url_collector()
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(0.5)
            last_div = driver.find_elements_by_xpath("//div[@class='ReactVirtualized__Grid__innerScrollContainer']//div")[-1]
            if last_div.value_of_css_property('height') == '0px':
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.5)
                url_collector()
                scrolling_place = False

    def get_hotel(href):
        rooms = len(driver.find_elements_by_class_name('result-room-info'))
        described_rooms = len(driver.find_elements_by_class_name('with-image'))
        without_desc = rooms - described_rooms
        name = driver.find_element_by_class_name('hotel-name-value').text[7:]
        country = driver.find_element_by_class_name('destination').text
        num_stars = len(driver.find_elements_by_css_selector('.active.icon-smd-star'))
        # hotel_to_class = HotelWithEmptyRooms(name, num_stars, country, without_desc, href)
        # hotels_with_empty_rooms.append(hotel_to_class)
        id_lt = href.split('-')[0][28:]
        if Hotel.objects.filter(id_lt=int(id_lt)).exists():
            query_hotel = Hotel.objects.get(id_lt=int(id_lt))
            query_hotel.name = name
            query_hotel.stars = num_stars
            query_hotel.num_empty_rooms = without_desc
            query_hotel.href = href
            query_hotel.save()
        else:
            Hotel.objects.create(id_lt=int(id_lt), name=name, stars=int(num_stars), country=country, num_empty_rooms=int(without_desc), href=href)

    url = 'https://level.travel/search/Moscow-RU-to-Any-' + country + '-departure-' + str(d) + '.' + str(m) + '.' + str(y) + '-for-' + str(nights) + '-nights-2-adults-0-kids-1..5-stars?sort_by=price,asc'

    if stars:
        url = url + '&filter_stars=' + str(stars)

    driver.get(url)

    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hotels-list-item"))
        )
    except NoSuchElementException:
        location = driver.find_element_by_class_name('destination').text
        print(location + ': нет туров по выбранным параметрам!')
    except TimeoutException:
        print('Timeout')
    else:
        scrolling()
        print(len(hotel_urls))
        for hotel_url in hotel_urls:
            driver.get(hotel_url)
            try:
                element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='lt-hotel-results-main-content']"))
                )
            except TimeoutException:
                pass
            else:
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='lt-hotel-utils']//button"))
                    )
                except NoSuchElementException:
                    pass
                except TimeoutException:
                    pass
                else:
                    actions = ActionChains(driver)
                    button = driver.find_element_by_xpath("//div[@class='lt-hotel-utils']//button")
                    actions.click(button).perform()
                finally:
                    # t = Timer(10.0from selenium.webdriver.common.action_chains import ActionChains, empty_rooms)
                    # t.start()
                    get_hotel(hotel_url)


def update_info():
    query_set = Hotel.objects.filter(country="Доминикана")
    chrome_driver = '/Users/eivannikova/development/chromedriver'
    chrome_option = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", prefs)
#    chrome_option.add_argument("headless")

    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_option)

    for hotel in query_set:

        url = hotel.href

        driver.get(url)

        def get_hotel(href):
            rooms = len(driver.find_elements_by_class_name('result-room-info'))
            described_rooms = len(driver.find_elements_by_class_name('with-image'))
            without_desc = rooms - described_rooms
            name = driver.find_element_by_class_name('hotel-name-value').text[7:]
            num_stars = len(driver.find_elements_by_css_selector('.active.icon-smd-star'))
            id_lt = href.split('-')[0][28:]
            query_hotel = Hotel.objects.get(id_lt=int(id_lt))
            query_hotel.name = name
            query_hotel.stars = num_stars
            query_hotel.num_empty_rooms = without_desc
            query_hotel.href = href
            query_hotel.save()

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='lt-hotel-results-main-content']"))
            )
        except TimeoutException:
            pass
        else:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='lt-hotel-utils']//button"))
                )
            except NoSuchElementException:
                pass
            except TimeoutException:
                pass
            else:
                actions = ActionChains(driver)
                button = driver.find_element_by_xpath("//div[@class='lt-hotel-utils']//button")
                actions.click(button).perform()
            finally:
                # t = Timer(10.0from selenium.webdriver.common.action_chains import ActionChains, empty_rooms)
                # t.start()
                get_hotel(url)


def update_hotel_info_parse(id_lt):
    hotels = Hotel.objects.filter(id_lt=id_lt)
    chrome_driver = '/Users/eivannikova/development/chromedriver'
    chrome_option = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_option.add_experimental_option("prefs", prefs)
    # chrome_option.add_argument("headless")
    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_option)

    for hotel in hotels:
        url = hotel.href

        driver.get(url)

        def get_hotel(href):
            rooms = len(driver.find_elements_by_class_name('result-room-info'))
            described_rooms = len(driver.find_elements_by_class_name('with-image'))
            without_desc = rooms - described_rooms
            name = driver.find_element_by_class_name('hotel-name-value').text[7:]
            num_stars = len(driver.find_elements_by_css_selector('.active.icon-smd-star'))
            id_lt = href.split('-')[0][28:]
            query_hotel = Hotel.objects.get(id_lt=int(id_lt))
            query_hotel.name = name
            query_hotel.stars = num_stars
            query_hotel.num_empty_rooms = without_desc
            query_hotel.href = href
            query_hotel.save()

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='lt-hotel-results-main-content']"))
            )
        except TimeoutException:
            pass
        else:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='lt-hotel-utils']//button"))
                )
            except NoSuchElementException:
                pass
            except TimeoutException:
                pass
            else:
                actions = ActionChains(driver)
                button = driver.find_element_by_xpath("//div[@class='lt-hotel-utils']//button")
                actions.click(button).perform()
            finally:
                # t = Timer(10.0from selenium.webdriver.common.action_chains import ActionChains, empty_rooms)
                # t.start()
                get_hotel(url)









