import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HENDLESS=False

# Logger class
class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

# Random sleep functionality
class RandomSleeper:
    def sleep_randomly(self, min_seconds=1, max_seconds=3):
        sleep_time = random.uniform(min_seconds, max_seconds)
        time.sleep(sleep_time)

# Web browser management
class WebDriverManager:
    def __init__(self, driver_path, headless=HENDLESS):
        self.logger = Logger()
        self.sleeper = RandomSleeper()
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")  # Пример размера окна
        else:
            chrome_options.add_argument("--start-maximized")  # Открывает браузер в полноэкранном режиме
            
        try:
            self.driver = webdriver.Chrome(driver_path, options=chrome_options)
            self.logger.log_info("WebDriver успешно инициализирован.")
        except Exception as e:
            self.logger.log_error(f"Ошибка при инициализации WebDriver: {e}")

    def open_page(self, url):
            try:
                self.driver.get(url)
                self.sleeper.sleep_randomly()
                self.handle_cookies_popup()  # Обработка всплывающего окна с куками
                self.sleeper.sleep_randomly()
                self.logger.log_info(f"Страница {url} успешно открыта.")
            except Exception as e:
                self.logger.log_error(f"Ошибка при открытии страницы {url}: {e}")

    def handle_cookies_popup(self):
            try:
                # Ждем и нажимаем на кнопку для настройки куков
#                 settings_button = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.ID, 'onetrust-pc-btn-handler')) #id="onetrust-pc-btn-handler"
#                 )
                settings_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'onetrust-pc-btn-handler'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", settings_button)

                settings_button.click()

                # Ждем, пока прогрузится следующее окно
                self.sleeper.sleep_randomly()

                # Ждем и нажимаем на кнопку для отказа от всех куков
                refuse_all_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'ot-pc-refuse-all-handler'))
                )
                refuse_all_button.click()

                # Ждем, чтобы убедиться, что всплывающее окно закрылось
                self.sleeper.sleep_randomly()
                self.logger.log_info("Все куки были успешно отклонены.")
            except Exception as e:
                self.logger.log_error(f"Ошибка при обработке всплывающего окна с куками: {e}")
        
    def click_selected_option(self):
        try:
            selected_option_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'selected-option'))
            )
            selected_option_button.click()
            self.logger.log_info("Кнопка 'selected-option' была нажата.")
        except Exception as e:
            self.logger.log_error(f"Ошибка при нажатии на кнопку 'selected-option': {e}")

    def select_matched_amount_option(self):
        try:
            option_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'option-list-item'))
            )
            for option in option_list:
                if option.text == "Matched Amount":
                    option.click()
                    self.logger.log_info("Опция 'Matched Amount' выбрана.")
                    break
        except Exception as e:
            self.logger.log_error(f"Ошибка при выборе опции 'Matched Amount': {e}")
            
    def extract_mod_links_data(self):
        data_list = []
        try:
            coupon_table = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'coupon-table'))
            )
            mod_links = coupon_table.find_elements(By.CLASS_NAME, 'mod-link')
            
            for link in mod_links:
                data = {
                    'data-market-id': link.get_attribute('data-market-id'),
                    'href': link.get_attribute('href'),
                    'data-event-or-meeting-id': link.get_attribute('data-event-or-meeting-id'),
                    'data-competition-or-venue-name': link.get_attribute('data-competition-or-venue-name'),
                    'data-event-or-meeting-name': link.get_attribute('data-event-or-meeting-name'),
                    'matched-amount-value': None
                }
                
                # Обработка 'matched-amount-value'
                matched_amount_elements = link.find_elements(By.CLASS_NAME, 'matched-amount-value')
                if matched_amount_elements:
                    matched_amount_value = matched_amount_elements[0].text.strip()
                    processed_value = self.process_matched_amount_value(matched_amount_value)
                    data['matched-amount-value'] = processed_value
                else:
                    data['matched-amount-value'] = None

                data_list.append(data)

            self.logger.log_info("Данные с элементов 'mod-link' успешно извлечены.")
            return data_list
        except Exception as e:
            self.logger.log_error(f"Ошибка при извлечении данных с элементов 'mod-link': {e}")
            return data_list
        
    def process_matched_amount_value(self, value):
        if value and value[0] == '€':
            value = value[1:]  # Удаление символа евро
        value = value.replace(',', '')  # Удаление запятых
        try:
            return float(value)  # Преобразование в число с плавающей точкой
        except ValueError:
            return None  # В случае ошибки преобразования возвращаем None

    def open_new_tab(self, url):
        try:
            self.driver.execute_script(f"window.open('{url}');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.sleeper.sleep_randomly()
            self.logger.log_info(f"Новая вкладка с {url} открыта.")
        except Exception as e:
            self.logger.log_error(f"Ошибка при открытии новой вкладки: {e}")

    def close_current_tab(self):
        try:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.sleeper.sleep_randomly()
                self.logger.log_info("Текущая вкладка закрыта.")
            else:
                self.logger.log_info("Закрытие последней вкладки. Оставляю браузер открытым.")
        except Exception as e:
            self.logger.log_error(f"Ошибка при закрытии вкладки: {e}")

    def switch_to_tab(self, index):
        try:
            self.driver.switch_to.window(self.driver.window_handles[index])
            self.sleeper.sleep_randomly()
            self.logger.log_info(f"Переключение на вкладку с индексом {index}.")
        except Exception as e:
            self.logger.log_error(f"Ошибка при переключении на вкладку: {e}")

    def close_browser(self):
        try:
            self.driver.quit()
            self.logger.log_info("WebDriver закрыт.")
        except Exception as e:
            self.logger.log_error(f"Ошибка при закрытии WebDriver: {e}")
            
    def wait_for_page_load(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: self.driver.execute_script('return document.readyState') == 'complete'
        )
        self.logger.log_info("Страница полностью загружена.")
    
    def filter_and_display_data(self, data_list):
        try:
            # Извлечение значений matched-amount-value и исключение None значений
            valid_values = [d['matched-amount-value'] for d in data_list if d['matched-amount-value'] is not None]

            # Проверка на наличие валидных значений
            if not valid_values:
                self.logger.log_info("Нет валидных данных для анализа.")
                return

            # Вычисление среднего значения
            average_value = sum(valid_values) / len(valid_values)
            self.logger.log_info(f"Среднее значение matched-amount-value: {average_value}")

            # Вывод значений больше среднего
            for item in data_list:
                if item['matched-amount-value'] and item['matched-amount-value'] > average_value:
                    print(f'{item["matched-amount-value"]} - {item["data-competition-or-venue-name"]}')
        except Exception as e:
            self.logger.log_error(f"Ошибка в filter_and_display_data: {e}")

# Пример использования
web_driver_manager = WebDriverManager('chromedriver.exe')
web_driver_manager.open_page('https://www.betfair.com/exchange/plus/en/football-betting-1/inplay')
web_driver_manager.click_selected_option()
web_driver_manager.select_matched_amount_option()
web_driver_manager.wait_for_page_load()
data_list = web_driver_manager.extract_mod_links_data()
web_driver_manager.filter_and_display_data(data_list)
time.sleep(5)
web_driver_manager.close_browser()