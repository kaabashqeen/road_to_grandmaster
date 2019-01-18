from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import chess
from stockfish import Stockfish


class Chess(object):

    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        x_space = height / 16
        y_space = width / 16
        self.board = {}
        self.make_board(x_space,y_space, color)

    def make_board(self, x_topleft, y_topleft, color):
        x_distance = x_topleft*2
        y_distance = y_topleft*2
        self.board['a8'] = (x_topleft, y_topleft)
        alpha_list = ['a','b','c','d','e','f','g','h']
        if color == "White":
            alpha_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            for i in range(8,0,-1):
                y_start = y_topleft + y_distance*(8-i)
                x_start = x_topleft
                for j in range(len(alpha_list)):
                    loc = alpha_list[j] + str(i)
                    self.board[loc] = (x_start+x_distance*(j),y_start)
        elif color == "Black":
            alpha_list.reverse()
            print(alpha_list)
            for i in range(1,9):
                y_start = y_topleft + y_distance*(i-1)
                x_start = x_topleft
                for j in range(len(alpha_list)):
                    loc = alpha_list[j] + str(i)
                    self.board[loc] = (x_start+x_distance*(j),y_start)


# def endgame_check(moveset):
#     for move in moveset:
#         if move.text == "1-0":
#             return('W')
#         elif move.text == "0-1":
#             return("B")
#         elif move.text == "1/2-1/2":
#             return('D')
#     return False

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
# driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[1]/div[1]/ul/li[10]/a').click()
# start play
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()
# switch to black
driver.find_element_by_xpath('//*[@id="chess-board-sidebar"]/div[5]/div[2]/a[1]/i').click()
# get element.style height and width of board
chessboard = driver.find_element_by_xpath('//*[@id="chessboard_boardarea"]')
height, width = chessboard.size['height'], chessboard.size['width']

start = driver.find_elements_by_xpath('//*[@id="chessboard_boardarea"]')[0]

# assume game is white for me
# color = driver.find_element_by_xpath('//*[@id="live-app"]/div[1]/div[2]/div[3]')
# color = color.get_attribute("class")
# if color.find("white") == -1:
color = "Black"
# else:
#     color = "White"
chess_game = Chess(height, width, color)
if color == "Black":
    while len(driver.find_elements_by_class_name("gotomove"))==0:
        pass
    # action = webdriver.ActionChains(driver)
    # action.move_to_element_with_offset(start, chess_game.board['e2'][0], chess_game.board['e2'][1])
    # action.click()
    # action.move_to_element_with_offset(start, chess_game.board['e4'][0], chess_game.board['e4'][1])
    # action.click()
    # action.perform()

elif color == "White":
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
    if move.text!="":
        board.push_san(move.text)
        moves[move_count] = move.text
        movelist.append(move.text)

        move_count += 1

game = True

offset = 0
if color == "Black":
    offset = -1
while game:
    time.sleep(1)
    moveset1 = driver.find_elements_by_class_name("gotomove")
    moveset = [move.text for move in moveset1]
    move = moveset[-1]
    if move == "1-0":
        print ('W')
        break
    elif move == "0-1":
        print ("B")
        break
    elif move == "1/2-1/2":
        print ('D')
        break

    if len(prev_moveset) != len(moveset):
        diff = len(moveset)-len(prev_moveset)
        print(diff)
        print(len(moveset))
        for move in moveset[(-1*diff+offset):]:
            if move!='':
                print(move)
                moves[move_count] = move
                movelist.append(move)
                # update state of board
                board.push_san(move)
                move_count += 1
                print('done')

    print(moves)
    print(board)

    stockfish.set_fen_position(board.fen())
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

    if color=="White":
        curr_moves = driver.find_elements_by_class_name("gotomove")
        # sleep_count = 0
        last_move = curr_moves[-1].text
        while last_move=='':
            print(len(driver.find_elements_by_class_name("gotomove")))
            print("waiting")
            time.sleep(1)
            curr_moves = driver.find_elements_by_class_name("gotomove")
            last_move = curr_moves[-1].text
            # sleep_count+=1
            # if sleep_count == 100:
    elif color=="Black":
        curr_moves = driver.find_elements_by_class_name("gotomove")
        # sleep_count = 0
        last_move = curr_moves[-1].text
        while last_move=='':
            print(len(driver.find_elements_by_class_name("gotomove")))
            print("waiting")
            time.sleep(1)
            curr_moves = driver.find_elements_by_class_name("gotomove")
            last_move = curr_moves[-1].text
            # sleep_count+=1
            # if sleep_count == 100:
            move = moveset[-2].text
            if move == "1-0":
                print('W')
                break
            elif move == "0-1":
                print("B")
                break
            elif move == "1/2-1/2":
                print('D')
                break

    time.sleep(2)
    prev_moveset = moveset
    print()
    print('next move')
    print()

print('')
driver.find_element_by_xpath('//*[@id="game-over"]/div[1]/div[2]/div[2]/button').click()
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()


# driver.close()
# driver2.close()

'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import chess
from stockfish import Stockfish


class Chess(object):

    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        x_space = height / 16
        y_space = width / 16
        self.board = {}
        self.make_board(x_space,y_space, color)

    def make_board(self, x_topleft, y_topleft, color):
        x_distance = x_topleft*2
        y_distance = y_topleft*2
        self.board['a8'] = (x_topleft, y_topleft)
        alpha_list = ['a','b','c','d','e','f','g','h']
        if color == "White":
            alpha_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            for i in range(8,0,-1):
                y_start = y_topleft + y_distance*(8-i)
                x_start = x_topleft
                for j in range(len(alpha_list)):
                    loc = alpha_list[j] + str(i)
                    self.board[loc] = (x_start+x_distance*(j),y_start)
        elif color == "Black":
            alpha_list.reverse()
            print(alpha_list)
            for i in range(1,9):
                y_start = y_topleft + y_distance*(i-1)
                x_start = x_topleft
                for j in range(len(alpha_list)):
                    loc = alpha_list[j] + str(i)
                    self.board[loc] = (x_start+x_distance*(j),y_start)


# def endgame_check(moveset):
#     for move in moveset:
#         if move.text == "1-0":
#             return('W')
#         elif move.text == "0-1":
#             return("B")
#         elif move.text == "1/2-1/2":
#             return('D')
#     return False

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

options.executable_path='/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=options)
# driver2 = webdriver.Chrome(options=options)
stockfish = Stockfish('/Users/kaabashqeen/Downloads/stockfish-10-mac/Mac/stockfish-10-64')

Play actual


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
time.sleep(3)
chessboard = driver.find_element_by_id("game-board")

MIRROR PLAY 
# bot
driver.get('https://www.chess.com/play/computer')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="newbie-modal"]/div/div/button').click()
# change settings
driver.find_element_by_xpath('//*[@id="chess-board-sidebar"]/div[5]/div[1]/button[1]').click()
# choose level 10 bot
# driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[1]/div[1]/ul/li[10]/a').click()
# start play
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()
# switch to black
# driver.find_element_by_xpath('//*[@id="chess-board-sidebar"]/div[5]/div[2]/a[1]/i').click()
# get element.style height and width of board

chessboard = driver.find_element_by_xpath('//*[@id="chessboard_boardarea"]')

height, width = chessboard.size['height'], chessboard.size['width']

start = chessboard[0]

# assume game is white for me
color = driver.find_element_by_xpath('//*[@id="live-app"]/div[1]/div[2]/div[3]')
color = color.get_attribute("class")
if color.find("white") == -1:
    color = "Black"
else:
    color = "White"
chess_game = Chess(height, width, color)
if color == "Black":
    while len(driver.find_elements_by_class_name("gotomove"))==0:
        pass
    # action = webdriver.ActionChains(driver)
    # action.move_to_element_with_offset(start, chess_game.board['e2'][0], chess_game.board['e2'][1])
    # action.click()
    # action.move_to_element_with_offset(start, chess_game.board['e4'][0], chess_game.board['e4'][1])
    # action.click()
    # action.perform()

elif color == "White":
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
    if move.text!="":
        board.push_san(move.text)
        moves[move_count] = move.text
        movelist.append(move.text)

        move_count += 1

game = True

offset = 0
if color == "Black":
    offset = -1
while game:
    time.sleep(1)
    moveset1 = driver.find_elements_by_class_name("gotomove")
    moveset = [move.text for move in moveset1]
    move = moveset[-1]
    if move == "1-0":
        print ('W')
        break
    elif move == "0-1":
        print ("B")
        break
    elif move == "1/2-1/2":
        print ('D')
        break

    if len(prev_moveset) != len(moveset):
        diff = len(moveset)-len(prev_moveset)
        print(diff)
        print(len(moveset))
        for move in moveset[(-1*diff+offset):]:
            if move!='':
                print(move)
                moves[move_count] = move
                movelist.append(move)
                # update state of board
                board.push_san(move)
                move_count += 1
                print('done')

    print(moves)
    print(board)

    stockfish.set_fen_position(board.fen())
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

    if color=="White":
        curr_moves = driver.find_elements_by_class_name("gotomove")
        # sleep_count = 0
        last_move = curr_moves[-1].text
        while last_move=='':
            print(len(driver.find_elements_by_class_name("gotomove")))
            print("waiting")
            time.sleep(1)
            curr_moves = driver.find_elements_by_class_name("gotomove")
            last_move = curr_moves[-1].text
            # sleep_count+=1
            # if sleep_count == 100:
    elif color=="Black":
        curr_moves = driver.find_elements_by_class_name("gotomove")
        # sleep_count = 0
        last_move = curr_moves[-1].text
        while last_move=='':
            print(len(driver.find_elements_by_class_name("gotomove")))
            print("waiting")
            time.sleep(1)
            curr_moves = driver.find_elements_by_class_name("gotomove")
            last_move = curr_moves[-1].text
            # sleep_count+=1
            # if sleep_count == 100:
            move = moveset[-2].text
            if move == "1-0":
                print('W')
                break
            elif move == "0-1":
                print("B")
                break
            elif move == "1/2-1/2":
                print('D')
                break

    time.sleep(2)
    prev_moveset = moveset
    print()
    print('next move')
    print()

print('')
driver.find_element_by_xpath('//*[@id="game-over"]/div[1]/div[2]/div[2]/button').click()
driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()


# driver.close()
# driver2.close()

'''