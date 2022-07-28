from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
from selenium.common.exceptions import StaleElementReferenceException


class WebKitFeatureStatusTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.binary_location = '/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta'
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.close()

    def test_1_login_to_personal_account(self):
        """При успешной аутентификации проиcходит вход в личный кабинет"""

        self.driver.get("https://eduexp.ru/")

        username = 'con.t2012@yandex.ru'
        password = 'oc27T9G!'

        self.driver.find_element(By.CLASS_NAME, 'stm_lms_log_in').click()
        self.driver.find_element(By.NAME, 'login').clear()
        self.driver.find_element(By.NAME, 'login').send_keys(username)
        self.driver.find_element(By.NAME, 'password').clear()
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div/div/div[1]/div[2]/div[3]/a").click()
        welcome_message = self.driver.find_element(By.ID, 'dLabel').is_displayed()

        self.assertEqual(welcome_message, True)

    def test_2_invalid_password(self):
        """При вводе неверного пароля появляется предупреждающая надпись.
        Вход в личный кабинет не произойдет"""

        self.driver.get("https://eduexp.ru/")

        username = 'con.t2012@yandex.ru'
        password = '1111'

        self.driver.find_element(By.CLASS_NAME, 'stm_lms_log_in').click()
        self.driver.find_element(By.NAME, 'login').clear()
        self.driver.find_element(By.NAME, 'login').send_keys(username)
        self.driver.find_element(By.NAME, 'password').clear()
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div/div/div[1]/div[2]/div[3]/a").click()
        error_message = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[10]/div[2]/div/div/div[1]/div[3]').is_displayed()

        self.assertEqual(error_message, True)

    def test_3_link_free_education(self):
        """При клике на 'Бесплатное обучение' происходит переход на нужную страницу"""

        self.driver.get("https://eduexp.ru/")

        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/a') \
            .click()
        link_free_workers = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div['
                                                               '2]/div/div[2]/a').is_displayed()

        self.assertEqual(link_free_workers, True)

    def test_4_add_course_in_basket(self):
        """Проверка возможности добавления товара в корзину (авторизованный режим)"""

        self.driver.get("https://eduexp.ru/")

        username = 'con.t2012@yandex.ru'
        password = 'oc27T9G!'

        self.driver.find_element(By.CLASS_NAME, 'stm_lms_log_in').click()
        self.driver.find_element(By.NAME, 'login').clear()
        self.driver.find_element(By.NAME, 'login').send_keys(username)
        self.driver.find_element(By.NAME, 'password').clear()
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div/div/div[1]/div[2]/div[3]/a").click()
        self.driver.execute_script("window.scrollTo(0,1000)")
        try:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[3]/div[2]/div[2]/div/section[6]/div/div/div/div/div/div/div/div['
                                     '1]/div[1]/div/div[4]/div/div/div[2]/div[2]/a').click()
        except StaleElementReferenceException:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div[3]/div[2]/div[2]/div/section[6]/div/div/div/div/div/div/div/div['
                                     '1]/div[1]/div/div[5]/div/div/div[1]/a/div/div/img').click()
        self.driver.find_element(By.CSS_SELECTOR,
                                 '#main > div.stm-lms-wrapper > div > div > div.col-md-3 > div > '
                                 'div.stm-lms-buy-buttons.stm-lms-buy-buttons-mixed.stm-lms-buy-buttons-mixed-pro > '
                                 'div > div.kkkkkkkk.buy-button.btn.btn-default.btn_big.heading_font').click()
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div[3]/div[2]/a').click()
        course_in_basket = self.driver.find_element(By.CSS_SELECTOR,
                                                    '#main > div.container > div.post_type_exist.clearfix > '
                                                    'div.woocommerce > form > div.table-responsive > table > tbody > '
                                                    'tr.woocommerce-cart-form__cart-item.cart_item > td.product-name '
                                                    '> picture > img').is_displayed()

        self.assertEqual(course_in_basket, True)


if __name__ == "__main__":
    unittest.main()
