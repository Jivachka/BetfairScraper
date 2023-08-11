from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BetfairScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.driver.implicitly_wait(20)  # Ждать до 10 секунд перед каждым поиском элемента
        self.wait = WebDriverWait(self.driver, 20)
        self.odds_all = 'label.Zs3u5.AUP11.Qe-26[ng-if="!$ctrl.isSp"]'

    def open_browser(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        try:
            cookie_button = self.wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
            cookie_button.click()
        except:
            print("Cookie button not found")

    def get_total_matched(self):
        element = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "span.total-matched[ng-bind='ctrl.data.marketMatched.totalMatched']"
        )))
        return element.text

    def get_odds(self):
        time.sleep(2)
        element_home_back = self.wait.until(EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                self.odds_all
            )
        ))
        return [element.text for element in element_home_back]


    def wait_for_dom(self, *args):
        return self.driver.execute_script("return document.readyState === 'complete';")

    def click_goals_button(self):
        goals_buttons = self.driver.find_elements_by_css_selector('a.tab-heading')
        for i in goals_buttons:
            if i.text == 'Goals' or i.text == 'Голы':
                i.click()

    def close_browser(self):
        self.driver.quit()

if __name__ == "__main__":
    url2= 'https://www.betfair.com/exchange/plus/en/football/vietnamese-v-league/ho-chi-minh-city-v-binh-duong-betting-32547615'
    url = "https://www.betfair.com/exchange/plus/en/football/finnish-veikkausliiga/haka-v-ifk-mariehamn-betting-32525861"
    scraper = BetfairScraper(url2)
    scraper.open_browser()
    scraper.accept_cookies()

    total_matched = scraper.get_total_matched()
    print("Total Matched:", total_matched)

    scraper.click_goals_button()
    odds_list = scraper.get_odds()
    print("Odds List:", odds_list)

    scraper.close_browser()
