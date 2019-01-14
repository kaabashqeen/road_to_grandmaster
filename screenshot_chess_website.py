from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import chess


class Chess(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        x_space = height / 16
        y_space = width / 16
        self.board = {}
        self.make_board(x_space,y_space)

    def make_board(self, x_topleft, y_topleft):
        x_distance = x_topleft*2
        y_distance = y_topleft*2
        self.board['a8'] = (x_topleft, y_topleft)
        alpha_list = ['a','b','c','d','e','f','g','h']

        for i in range(8,0,-1):
            y_start = y_topleft + y_distance*(8-i)
            x_start = x_topleft
            for j in range(len(alpha_list)):
                loc = alpha_list[j] + str(i)
                self.board[loc] = (x_start+x_distance*(j),y_start)




options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

options.executable_path='/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=options)

''' Play actual
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
chat2 = driver2.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[2]/div/div[2]/input')
chat2.send_keys("/play")
chat2.send_keys(Keys.ENTER)
 '''

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
chat = driver.find_element_by_xpath('//*[@id="live-app"]/div[2]/div[2]/div/div[2]/input')
chat.send_keys("/play stockfish 30 w u")
chat.send_keys(Keys.ENTER)
'''

'''   MIRROR PLAY   '''
# bot
driver.get('https://www.chess.com/play/computer')
time.sleep(2)
# change settings
driver.find_element_by_xpath('//*[@id="chess-board-sidebar"]/div[5]/div[1]/button[1]').click()
# choose level 10 bot
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[1]/div[1]/ul/li[10]/a').click()
# start play
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()


# assume game is white for me

game = True

count = 0
while game:
    # moveset = driver.find_elements_by_id("movelist_")
    moveset = driver.find_elements_by_class_name("gotomove")
    moves = {}
    movelist = []
    move_count = 1
    for move in moveset:
        if move.text!='':
            moves[move_count] = move.text
            move_count+=1
            movelist.append(move.text)
        # print(movelist)
    # print(moveset1, count)
    # moves = driver.find_element_by_xpath('//*[@id="moveListControl"]')
    # moves_to_store = moves.text.split("\n")
    # print(moves_to_store, count)
    print(moves)
    print()

    count+=1

    board = chess.Board()

    for move in movelist:
        board.push_san(move)

    print(board)
    # get element.style height and width of board
    #

    chessboard = driver.find_element_by_xpath('//*[@id="chessboard_boardarea"]')
    height, width = chessboard.size['height'], chessboard.size['width']
    chess_game = Chess(height, width)

    start = driver.find_elements_by_xpath('//*[@id="chessboard_boardarea"]')[0]

    action = webdriver.ActionChains(driver)
    action.move_to_element_with_offset(start, chess_game.board['e2'][0], chess_game.board['e2'][1])
    action.click()
    action.move_to_element_with_offset(start, chess_game.board['e4'][0], chess_game.board['e4'][1])
    action.click()
    action.perform()

    time.sleep(5)




# driver.close()
# driver2.close()

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
# driver.save_screenshot("screenshot.png")
