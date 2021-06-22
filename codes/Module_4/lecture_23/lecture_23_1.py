# -*- coding: utf-8 -*-


import time
import requests
from hashlib import md5
from io import BytesIO
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

USERNAME = 'admin'
PASSWORD = 'admin'
CHAOJIYING_USERNAME = ''
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = 0
CHAOJIYING_KIND = 9004
if not CHAOJIYING_USERNAME or not CHAOJIYING_PASSWORD:
    print('请设置用户名和密码')
    exit(0)


def gain_driver():
    """

    :return:
    """
    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--proxy-server=http://" + "127.0.0.1:8889")
    chrome_options.add_argument("--disable-blink-features-AutomationControlled")
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36'
    )
    driver = Chrome('chromedriver', options=chrome_options)
    with open('stealth.min.js') as f:
        js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    return driver


class Chaojiying(object):

    def __init__(self, username, password, soft_id):
        """

        :param username:
        :param password:
        :param soft_id:
        """
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
        }

    def PostPic(self, im, codetype):
        """

        :param im: 图片字节
        :param codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        :return:
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {
            'userfile': ('ccc.jpg', im)
        }
        r = requests.post(
            'http://upload.chaojiying.net/Upload/Processing.php',
            data=params, files=files, headers=self.headers
        )
        return r.json()

    def ReportError(self, im_id):
        """

        :param im_id: 报错题目的图片ID
        :return:
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post(
            'http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers
        )
        return r.json()


class CrackCaptcha():
    def __init__(self):
        """

        """
        self.url = 'https://captcha3.scrape.center/'
        # self.browser = Chrome()
        self.browser = gain_driver()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def open(self):
        """
        打开网页输入用户名密码
        :return:
        """
        self.browser.get(self.url)
        #  填入用户名密码
        username = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        username.send_keys(self.username)
        password.send_keys(self.password)

    def get_captcha_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="button"]')))
        return button

    def get_captcha_element(self):
        """
        获取验证图片对象
        :return: 图片对象
        """
        #  验证码图片加载出来
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.geetest_item_img')))
        #  验证码完整节点
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_panel_box')))
        print('成功获取验证码节点')
        return element

    def get_captcha_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        element = self.get_captcha_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.save('screenshot.png')
        return screenshot

    def get_captcha_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_captcha_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_captcha(self):
        """

        :return:
        """
        image = self.get_captcha_image()
        '''由于之前已经得到验证码，直接读取即可'''
        # image = Image.open("captcha.png")
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        self.touch_click_words(self.get_points(result))
        print(result)

    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            ActionChains(self.browser).move_to_element_with_offset(
                self.get_captcha_element(), location[0], location[1]
            ).click().perform()
            time.sleep(1)


if __name__ == '__main__':
    """"""
    crackCaptcha = CrackCaptcha()
    crackCaptcha.open()
    # crackCaptcha.get_captcha_image()
    crackCaptcha.get_captcha()
