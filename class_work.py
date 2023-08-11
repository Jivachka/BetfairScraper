import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация драйвера. Убедитесь, что у вас установлен chromedriver и он доступен по пути ниже.
driver = webdriver.Chrome(executable_path='chromedriver.exe')
odds_all = 'label.Zs3u5.AUP11.Qe-26[ng-if="!$ctrl.isSp"]'

# Переходим на сайт
url = "https://www.betfair.com/exchange/plus/football/market/1.216829196"
driver.get(url)

# Устанавливаем явное ожидание
wait = WebDriverWait(driver, 10)  # увеличено до 20 секунд

# Принимаем куки
try:
    cookie_button = wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
    cookie_button.click()
except:
    print("Cookie button not found")

# Ожидаем появления интересующих элементов
element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    "span.total-matched[ng-bind='ctrl.data.marketMatched.totalMatched']"
    )))
element_home_back = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, odds_all)))

print(element.text)
list_odds = []
for i in element_home_back:
    list_odds.append(i.text)

print(list_odds[2])

# Находим кнопку по её селектору и кликаем по ней
try:
    goals_button = driver.find_element_by_css_selector('a.tab-heading h4.tab-label[title="Голы"]')
    goals_button.click()
except:
    print("Goals button not found")

def wait_for_dom(driver):
    return driver.execute_script("return document.readyState === 'complete';")


try:
    wait.until(wait_for_dom)
    time.sleep(2)
    res = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'label[ng-if="!$ctrl.isSp"].Zs3u5.AUP11.Qe-26')))
    for i in res:
        print(i.text)
except:
    print("Updated odds not found")

# Закрываем браузер
# driver.quit()
