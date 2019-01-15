from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import chess
from stockfish import Stockfish


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
# driver2 = webdriver.Chrome(options=options)
stockfish = Stockfish('/Users/kaabashqeen/Downloads/stockfish-10-mac/Mac/stockfish-10-64')

''' Play actual


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
driver.find_element_by_xpath('//*[@id="newbie-modal"]/div/div/button').click()
# change settings
driver.find_element_by_xpath('//*[@id="chess-board-sidebar"]/div[5]/div[1]/button[1]').click()
# choose level 10 bot
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[1]/div[1]/ul/li[10]/a').click()
# start play
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()

# get element.style height and width of board
chessboard = driver.find_element_by_xpath('//*[@id="chessboard_boardarea"]')
height, width = chessboard.size['height'], chessboard.size['width']
chess_game = Chess(height, width)
start = driver.find_elements_by_xpath('//*[@id="chessboard_boardarea"]')[0]

# assume game is white for me

# make initial move of pawn
action = webdriver.ActionChains(driver)
action.move_to_element_with_offset(start, chess_game.board['e2'][0], chess_game.board['e2'][1])
action.click()
action.move_to_element_with_offset(start, chess_game.board['e4'][0], chess_game.board['e4'][1])
action.click()
action.perform()

time.sleep(5)

prev_moveset = driver.find_elements_by_class_name("gotomove")

# moves contains numbered list of moves 1-n
moves = {}
# movelist contains actions for python-chess to take to ascertain current board state
movelist = []

board = chess.Board()
move_count = 1
stockfish.depth = 20
for move in prev_moveset:

    board.push_san(move.text)
    moves[move_count] = move.text
    movelist.append(move.text)

    move_count += 1

game = True
while game:
    moveset = driver.find_elements_by_class_name("gotomove")
    # print(len(moveset),len(prev_moveset))
    if len(prev_moveset) != len(moveset):
        diff = len(moveset)-len(prev_moveset)
        print(diff)
        print(len(moveset))
        print(len(moveset[(-1*diff):]))
        for move in moveset[(-1*diff):]:
            if move.text!='':
                print(move.text)
                moves[move_count] = move.text
                movelist.append(move.text)
                # update state of board
                board.push_san(move.text)
                move_count += 1
                print('done')


    print(moves)
    print(board)

    stockfish.set_fen_position(board.fen())
    # print(stockfish.depth)
    print(stockfish.get_best_move())
    best_move = stockfish.get_best_move()

    move1 = best_move[:2]
    move2 = best_move[2:]

    action = webdriver.ActionChains(driver)
    action.move_to_element_with_offset(start, chess_game.board[move1][0], chess_game.board[move1][1])
    action.click()
    promote = False
    if len(move2) == 3:
        move3 = move2[-1]
        move2 = move2[:-1]
        promote = True
    action.move_to_element_with_offset(start, chess_game.board[move2][0], chess_game.board[move2][1])
    action.click()
    if promote:
        if move3 == 'q':
            action.move_to_element_with_offset(start, chess_game.board[move2][0], chess_game.board[move2][1])
        elif move3 == 'n':
            action.move_to_element_with_offset(start, chess_game.board[move2][0], chess_game.board[move2][1]+height/16)
        action.click()
    action.perform()

    curr_moves = driver.find_elements_by_class_name("gotomove")
    
    while curr_moves[-1].text=='':
        print(len(driver.find_elements_by_class_name("gotomove")))
        print("waiting")
        time.sleep(1)
        curr_moves = driver.find_elements_by_class_name("gotomove")
    time.sleep(2)
    prev_moveset = moveset
    print()
    print('next move')
    # for move in curr_moves:
    #     print(move.text)
    # print()
    #
    # for move in prev_moveset:
    #     print(move)
    print()
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
