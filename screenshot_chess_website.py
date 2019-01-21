from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import chess
from stockfish import Stockfish


class Chess(object):

    def __init__(self):
        self.board = {}
        self.game_count=0
        self.games = open('games.txt', 'a')


    def makeBoard(self, x_topleft, y_topleft, color):
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


    def play(self):
        self.startUpGame()
        stockfish = Stockfish('/Users/kaabashqeen/Downloads/stockfish-10-mac/Mac/stockfish-10-64')
        chat = driver.find_element_by_class_name('chat-input-component').find_element_by_css_selector('input')
        play_game_button = driver.find_element_by_class_name('quick-challenge-play').click()
        messages_to_check = driver.find_elements_by_class_name("chat-message-component")
        game_found = False
        while game_found is False:
            print("Waiting to find opponent to play")
            if len(messages_to_check) == 0:
                continue
            else:
                for msg in messages_to_check:
                    if msg.get_attribute("data-notification") == "gameNewGamePlaying":
                        game_found = True
                        print("Game found!")
            time.sleep(5)
            messages_to_check = driver.find_elements_by_class_name("chat-message-component")
        time.sleep(3)
        chessboard = driver.find_element_by_id("game-board")
        height, width = chessboard.size['height'], chessboard.size['width']
        start = chessboard
        my_color = driver.find_element_by_xpath('//*[@id="live-app"]/div[1]/div[2]/div[3]')
        my_color = my_color.get_attribute("class")
        if my_color.find("white") == -1:
            my_color = "Black"
        else:
            my_color = "White"
        x_topleft = height/16
        y_topleft = width/16

        self.makeBoard(x_topleft,y_topleft, my_color)

        if my_color == "Black":
            while len(driver.find_elements_by_class_name("move-text-component")) == 0:
                print("Waiting for opponent to make initial move")
                time.sleep(1)
                pass

        elif my_color == "White":
            # make initial move of pawn
            action = webdriver.ActionChains(driver)
            action.move_to_element_with_offset(start, chess_game.board['e2'][0], chess_game.board['e2'][1])
            action.click()
            action.move_to_element_with_offset(start, chess_game.board['e4'][0], chess_game.board['e4'][1])
            action.click()
            action.perform()

        time.sleep(2)

        prev_moveset = driver.find_elements_by_class_name("move-text-component")

        # moves contains numbered list of moves 1-n
        moves = {}
        # movelist contains actions for python-chess to take to ascertain current board state
        movelist = []
        print(my_color)
        board = chess.Board()
        move_count = 1
        stockfish.depth = 20
        for move in prev_moveset:
            if move.text != "":
                board.push_san(move.text)
                moves[move_count] = move.text
                movelist.append(move.text)
                move_count += 1

        game_is_playing = True

        while game_is_playing:
            time.sleep(1)
            try:
                moveset1 = driver.find_elements_by_class_name("move-text-component")
            except:
                messages = driver.find_elements_by_class_name('chat-message-component')
                for msg in messages:
                    if msg.get_attribute("data-notification") == "gameOver":
                        game_is_playing = False
                        break
            moveset = [move.text for move in moveset1]
            print(moveset)
            move = moveset[-1]
            if move == "1-0":
                print('W')
                break
            elif move == "0-1":
                print("B")
                break
            elif move == "1/2-1/2":
                print('D')
                break

            if len(prev_moveset) != len(moveset):
                diff = len(moveset) - len(prev_moveset)
                print(diff)
                print(len(moveset))
                for move in moveset[(-1 * diff):]:
                    if move != '':
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
                    action.move_to_element_with_offset(start, chess_game.board[move2][0],
                                                       chess_game.board[move2][1] + height / 16)
                action.click()
            action.perform()

            if my_color == "White":
                curr_moves = driver.find_elements_by_class_name("move-text-component")
                sleep_count = 0
                last_move = curr_moves[-1].text
                while len(curr_moves) % 2 == 1:
                    print(len(driver.find_elements_by_class_name("move-text-component")))
                    print("waiting")
                    time.sleep(1)
                    try:
                        curr_moves = driver.find_elements_by_class_name("move-text-component")
                        last_move = curr_moves[-1].text
                    except:
                        draw_check = driver.find_element_by_class_name('draw-offer-decline')
                        draw_check.click()
                        time.sleep(3)
                        curr_moves = driver.find_elements_by_class_name("move-text-component")
                        last_move = curr_moves[-1].text
                    sleep_count += 1
                    if sleep_count >= 30:
                        if self.endGameCheck():
                            game_is_playing = False
                            try:
                                ratings = driver.find_elements_by_class_name('user-tagline-rating')
                                for i in range(len(ratings)):
                                    if i ==0:
                                        self.games.write('\n opponent:', ratings[i].text)
                                    else:
                                        self.games.write(' (now at', ratings[i].text, 'rating')
                            except:
                                break
                            break

            elif my_color == "Black":
                curr_moves = driver.find_elements_by_class_name("move-text-component")
                sleep_count = 0
                last_move = curr_moves[-1].text
                while len(curr_moves) % 2 == 0:
                    print(len(driver.find_elements_by_class_name("move-text-component")))
                    print("waiting")
                    time.sleep(1)
                    try:
                        curr_moves = driver.find_elements_by_class_name("move-text-component")
                        last_move = curr_moves[-1].text
                    except:
                        draw_check = driver.find_element_by_class_name('draw-offer-decline')
                        draw_check.click()
                        time.sleep(3)
                        curr_moves = driver.find_elements_by_class_name("move-text-component")
                        last_move = curr_moves[-1].text
                    sleep_count += 1
                    if sleep_count >= 30:
                        if self.endGameCheck():
                            game_is_playing= False
                            try:
                                ratings = driver.find_elements_by_class_name('user-tagline-rating')
                                for i in range(len(ratings)):
                                    if i ==0:
                                        self.games.write('\n opponent:', ratings[i].text)
                                    else:
                                        self.games.write(' (now at', ratings[i].text, 'rating')
                            except:
                                break
                            break
            time.sleep(2)
            prev_moveset = moveset
            print()
            print('next move')
            print()
            if self.endGameCheck():
                game_is_playing = False
                try:
                    ratings = driver.find_elements_by_class_name('user-tagline-rating')
                    for i in range(len(ratings)):
                        if i == 0:
                            self.games.write('\n opponent:', ratings[i].text)
                        else:
                            self.games.write(' (now at', ratings[i].text, 'rating')
                except:
                    break
                break
        print('end')
        self.game_count+=1
        if self.game_count==1:
            self.games.close()
            pass

        else:
            self.games.write('\n')
            self.play()


    def startUpGame(self):

        driver.get('https://www.chess.com/live')
        time.sleep(5)
        available_options = driver.find_elements_by_class_name('tabset-nav-title')
        if len(available_options) == 3:
            start = available_options[1]
            action = webdriver.ActionChains(driver)
            action.move_to_element_with_offset(start, 1, 1)
            action.click()
            action.perform()
        time.sleep(3)


    def endGameCheck(self):
        try:
            if driver.find_element_by_class_name('game-over-dialog-component'):
                return True
        except:
            return False

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.executable_path='/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=options)

# Login
driver.get('https://www.chess.com/')
driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/a').click()
driver.find_element_by_xpath('//*[@id="sb"]/div[2]/a[7]').click()
driver.find_element_by_xpath('//*[@id="username"]').send_keys('')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('')
driver.find_element_by_xpath('//*[@id="_remember_me"]').click()
driver.find_element_by_xpath('//*[@id="login"]').click()

# Play

chess_game = Chess()
chess_game.play()


# driver.find_element_by_xpath('//*[@id="game-over"]/div[1]/div[2]/div[2]/button').click()
# driver.find_element_by_xpath('//*[@id="new-game"]/div[2]/div[1]/article/div[2]/button').click()


# driver.close()
# driver2.close()
