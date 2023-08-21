from selenium import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.myfxbook.com/members/Nicholas54/bullbear-bot-lite/4392701'
options = webdriver.ChromeOptions()
us = UserAgent()
# options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (
# KHTML, ' 'like Gecko) Chrome/67.0.3396.81 Mobile Safari/537.36')
# каждый запуск будет со случайным юзер агентом
options.add_argument(f"user-agent={us.random}")
# скрываем работу драйвера хром
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=options)
# result_dict = {'open_date': [], 'close_date': [], 'symbol': [], 'action': [], 'lots': [], 'open_price': [],
#               'close_price'
#             : [], 'pips': [], 'profit_usd': [], 'duration': [], 'gain': []}
result_dict = dict()
file_result = 'result.csv'

try:
    driver.maximize_window()  # делаем большое окно браузера
    driver.get(url=url)  # загружаем страницу
    time.sleep(5)  # даем время загрузиться
    # соглашаемся со всеми куками
    driver.find_element(By.XPATH, '//*[@id="dismissGdprConsentBannerBtn"]').click()
    time.sleep(5)
    # сдвигаем на нужный фрагмент ресурса
    driver.execute_script('window.scrollBy(0, 1450)')
    # выжидаем время
    time.sleep(5)
    # жмем на всплывающее окно
    # driver.find_element(By.XPATH, '//*[@id="blockContinueLink"]').click()
    # time.sleep(5)
    # выбираем вкладку history
    driver.find_element(By.NAME, 'history').click()
    time.sleep(5)
    # скрываем нижнее всплывающее окно
    driver.find_element(By.XPATH, '//*[@id="hideToolbarBtn"]/i').click()
    time.sleep(2)
    i = 1
    count = 0
    for i in range(1819):
        requiredHtml = driver.page_source  # получаем объект html
        soup = BeautifulSoup(requiredHtml, 'lxml')
        string_one = soup.find_all('tr', class_='commentRow')
        for item in string_one:
            string_one_one = item.find_all('td')
            for item_item in string_one_one:
                i += 1
                # print(i)
                if i > 143:
                    text_item = item_item.text.strip()
                    if text_item is not None:
                        count += 1
                        result_dict [count] = [text_item]
                # print(item_item.text.strip())
        # жмем на next
        driver.find_element(By.XPATH, '//*[@id="historyCont"]/div[2]/div/ul[1]/li[9]/a/i').click()
        time.sleep(1)

except Exception as ex:
    print(ex)
finally:
    driver.close()  # закрываем драйвер
    driver.quit()
    df = pd.DataFrame(data=result_dict)
    df.to_csv('result.csv')
