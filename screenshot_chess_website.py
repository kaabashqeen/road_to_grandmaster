from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

options.executable_path='/usr/local/bin/chromedriver'
# driver = webdriver.Chrome(options=options)
driver2 = webdriver.Chrome(options=options)

# Login with real
driver2.get('https://www.chess.com/')
driver2.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/a').click()
driver2.find_element_by_xpath('//*[@id="sb"]/div[2]/a[7]').click()
driver2.find_element_by_xpath('//*[@id="username"]').send_keys('road_to_gmaster')
driver2.find_element_by_xpath('//*[@id="password"]').send_keys('muhkap')
driver2.find_element_by_xpath('//*[@id="_remember_me"]').click()
driver2.find_element_by_xpath('//*[@id="login"]').click()

# Play Real Game
driver2.get('https://www.chess.com/live')
time.sleep(5)
chat = driver2.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[2]/div/div[2]/input')
chat.text = "/play"
chat.submit()
# driver2.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[2]/div/div[2]/input').submit()

'''
# Login with fake
driver.get('https://www.chess.com/')
driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/a').click()
driver.find_element_by_xpath('//*[@id="sb"]/div[2]/a[7]').click()
driver.find_element_by_xpath('//*[@id="username"]').send_keys('clouph')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('muhkap')
driver.find_element_by_xpath('//*[@id="_remember_me"]').click()
driver.find_element_by_xpath('//*[@id="login"]').click()

# Play with fake
driver.get('https://www.chess.com/live')
# current_url = driver.current_url
driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[2]/div/div[2]/input').text = '/play stockfish 30 w u'
driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[2]/div/div[2]/input').submit()
'''


# bot
# driver.get('https://www.chess.com/play/computer')
# driver.save_screenshot("screenshot.png")
# driver.find_element_by_xpath('//*[@id="newbie-modal"]/div/div/button').click()
# driver.find_element_by_xpath('//*[@id="topPlayer"]/div[2]/a/span').click()
# driver.find_element_by_xpath('//*[@id="game-settings"]/div[2]/div[1]/div[1]/div[1]/ul/li[10]/a').click()
# driver.find_element_by_xpath('//*[@id="game-settings"]/div[1]/button/i').click()
# driver.find_element_by_xpath('//*[@id="game-settings"]/div[1]/button').click()
# driver.find_element_by_id('movelist_1')

#
# driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[1]/div[1]/div/a[22]/div').click()
# driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[1]/div[1]/div/a[22]/div').click()
# driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[1]/div[1]/div[2]/a[4]').click()
# driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[1]/div[1]/div/a[22]/div').click()
# driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[1]/div[1]/div[2]/button').click()
# //*[@id="live-app"]/div[2]/div[1]/ul/li[2]/span
# //*[@id="live-app"]/div[2]/div[1]/ul/li[2]/i
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# class WebDriverPythonBasics(unittest.TestCase):
#     def setUp(self):
#         self.browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
#
#     def test_saucelabs_homepage_header_displayed(self):
#         self.browser.get('https://www.chess.com/play/computer')
#         header = self.browser.find_element(By.ID, 'site-header')
#         self.assertTrue(header.is_displayed())
#
#
#     def tearDown(self):
#         self.browser.close()
#
# if __name__ == '__main__':
#     unittest.main()