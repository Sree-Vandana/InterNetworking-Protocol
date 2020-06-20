import pygame, math
from Client_Network import Game_Network
from tkinter import *
from tkinter import messagebox

# GUI
# initialize pygame module
pygame.init()

# score board global values
score = [0,0]
ties = 0

timer = 11
crash = 0
crash_count = 6
P = 1

class RPS_GUI:

    def __init__(self):

        # window of the game (tuple)
        self.height = 500  # pixels
        self.width = 600  # pixels
        self.game_window = pygame.display.set_mode((self.width, self.height))

        #background
        self.background = pygame.image.load('1.jpg')

        # Title and Logo
        pygame.display.set_caption("Rock Paper Scissors")
        icon = pygame.image.load('rock.png')
        pygame.display.set_icon(icon)

    def menu_screen(self):

        global score, crash, timer, ties, crash_count, P, m

        run = True
        clock = pygame.time.Clock()
        print("in menu screen")
        while run:
            clock.tick(100)
            # background image
            self.game_window.fill((128, 128, 128))
            self.background = pygame.transform.scale(self.background, (600, 500))
            rect = self.background.get_rect()
            rect = rect.move((0, 0))
            self.game_window.blit(self.background, rect)

            font = pygame.font.SysFont("comicsans", 40)
            if crash == 1:
                text_1 = font.render("could not retrive game object", 1, (255, 0, 0))
                text_2 = font.render("try after sometime :(",1, (255, 0, 0))
                self.game_window.blit(text_1, (50, 250))
                self.game_window.blit(text_2, (80, 300))

                seconds = self.clock_t.tick() / 1000.0
                crash_count -= seconds
                crash_count_display = math.trunc(crash_count)

                font = pygame.font.SysFont("comicsans", 40)
                text_3 = font.render("wait and try later in" + " " + (str(int(crash_count_display))), 1, (0, 255, 255), True)
                self.game_window.blit(text_3, (110, 350))

                if crash_count_display <= 0:
                    window = Tk()
                    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                    window.withdraw()

                    if messagebox.askyesno('question','want to stay connected and try(click YES) or QUIT (click NO)?') == True:
                        crash_count = 6
                        crash = 0
                    else:
                        pygame.quit()

                    window.deiconify()
                    window.destroy()
                    window.quit()


            else:
                if P == 0:
                    font = pygame.font.SysFont("comicsans", 30)
                    text_10 = font.render("other player got disconnected", 1, (0, 255, 0))
                    self.game_window.blit(text_10, (140, 200))

                font = pygame.font.SysFont("comicsans", 30)
                text_10 = font.render("Start Playing?", 1, (255, 255, 255))
                self.game_window.blit(text_10, (230, 230))
                text = font.render("<< Click to form pairs and play :) >>", 1, (0, 255, 255))
                self.game_window.blit(text, (140, 250))

            img1 = pygame.image.load('rock.png')
            img2 = pygame.image.load('paper.png')
            img3 = pygame.image.load('scissors.png')
            self.game_window.blit(img1, (250, 50))
            self.game_window.blit(img2, (200, 100))
            self.game_window.blit(img3, (280, 100))

            pygame.display.update()

            # event manager
            #if an event occured.. quit this main screen and star gamming interface
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                # if clicked on screen; end this loop and start main
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        score = [0, 0]
        ties = 0
        timer = 11
        self.main()

    def main(self):

        global score, crash, ties, buttons_obj_list, P, m

        run = True
        #clock = pygame.time.Clock()
        # Client network object and get the respective player no.
        try:
            n = Game_Network()
            player = int(n.get_player_num())
            P = 1
            # print("You are player", player)
            pygame.display.set_caption("Rock Paper Scissors (player " + str(player) + ")")
        except:
            crash = 1
            self.clock_t = pygame.time.Clock()
            self.menu_screen()

        while run:
            # retrive game object
            try:
                game_obj = n.send("get")
            except:
                run = False
                print("Couldn't get game\nsomthing wrong with the server\nsending you back to the game menu")
                P = 0
                break
            # after getting the game object..
            if game_obj.both_players_Went():  # if both players went
                self.redraw_game_window(self.game_window, game_obj, player)  # update frames
                pygame.time.delay(300)
                try:
                    game_obj = n.send("reset")
                except:
                    run = False
                    print("Something went wrong while sending request.")
                    crash = 1
                    self.menu_screen()
                    break

                """
                winner = -1  --> tie
                winner = 0   --> player 0 wins
                winner = 1   --> player 1 wins 
                winner = 2   --> player 0 and 1 wants a new game
                winner = 3   --> any player request for new game; but other wants to continue 
                """
                font = pygame.font.SysFont("comicsans", 50)
                winner = game_obj.winner()

                if winner == -1:
                    ties += 1
                elif winner == 0 or winner == 1:
                    score[winner] += 1
                if (winner == 1 and player == 1) or (winner == 0 and player == 0):
                    text = font.render("You Won!", 1, (255, 0, 0))
                elif winner == -1:
                    text = font.render("Tie Game!", 1, (255, 0, 0))
                elif winner == 2:
                    text = font.render("Starting new game...", 1, (255, 0, 0))
                    score = [0, 0]
                    ties = 0
                elif winner == 3:
                    text = font.render("continue this game...", 1, (255, 0, 0))
                else:
                    text = font.render("You Lost...", 1, (255, 0, 0))

                self.game_window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))
                pygame.display.update()
                pygame.time.delay(1500)

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in buttons_obj_list:
                        if button.click(pos) and game_obj.connected():
                            # if any player cliecked new game; set score and ties =0 on both players screen
                            if (button.text.upper()[0] == "N"):
                                n.send(button.text)
                                self.redraw_game_window(self.game_window, game_obj, 0)
                                self.redraw_game_window(self.game_window, game_obj, 1)
                            else:
                                if player == 0:
                                    if not game_obj.player_1_Went:
                                        n.send(button.text)
                                else:
                                    if not game_obj.player_2_Went:
                                        n.send(button.text)
                        pygame.display.update()
            self.clock_t = pygame.time.Clock()
            self.redraw_game_window(self.game_window, game_obj, player)

    def redraw_game_window(self, game_window, game_obj, player):

        game_window.fill((128, 128, 128))
        game_window.blit(self.background, (0, 0))
        global score
        global ties
        global buttons_obj_list
        global timer

        # if not connected to other playing pair
        if not (game_obj.connected()):
            seconds = self.clock_t.tick()/1000.0
            timer -= seconds
            displaytimer = math.trunc(timer)
            font = pygame.font.SysFont("comicsans", 40)
            #text = font.render("Waiting for Player to connect...", 1, (255, 0, 0), True)
            text = font.render("Waiting for Player to connect..."+" "+(str(int(displaytimer))), 1, (255, 255, 255), True)
            game_window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))

            if displaytimer <= 0:
                window = Tk()
                window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                window.withdraw()

                if messagebox.askyesno('question', 'taking longer to connect with playing pair\n want to continue wait(click YES) or QUIT (click NO)?') == True:
                    timer = 11
                else:
                    pygame.quit()

                window.deiconify()
                window.destroy()
                window.quit()

        # if connected
        else:
            font = pygame.font.SysFont("comicsans", 40)

            text = font.render("Your Move", 1, (0, 255, 255))
            game_window.blit(text, (70, 120))

            text = font.render("Opponents", 1, (0, 255, 255))
            game_window.blit(text, (360, 120))

            move1 = game_obj.get_player_move(0)
            move2 = game_obj.get_player_move(1)

            if game_obj.both_players_Went():  # if both went..
                text1 = font.render(move1, 1, (255, 255, 255))
                text2 = font.render(move2, 1, (255, 255, 255))
            else:
            # For player 1
                if game_obj.player_1_Went and player == 0:
                    text1 = font.render(move1, 1, (255, 255, 255))
                elif game_obj.player_1_Went:
                    if move1 == "NewGame":
                        text1 = font.render("New Game", 1, (255, 255, 255))
                    elif move1 == "Menu":
                        text1 = font.render("Menu", 1, (255, 255, 255))
                    else:
                        text1 = font.render("Locked In", 1, (255, 255, 255))
                # if both did not go..
                else:
                    text1 = font.render("Waiting...", 1, (255, 255, 255))
            # For player 2
                if game_obj.player_2_Went and player == 1:
                    text2 = font.render(move2, 1, (255, 255, 255))
                elif game_obj.player_2_Went:
                    if move2 == "NewGame":
                        text2 = font.render("New Game", 1, (255, 255, 255))
                    elif move2 == "Menu":
                        text2 = font.render("Menu", 1, (255, 255, 255))
                    else:
                        text2 = font.render("Locked In", 1, (255, 255, 255))
                # if both did not go..
                else:
                    text2 = font.render("Waiting...", 1, (255, 255, 255))

            # if game.player_1_Went and game.p1moove
            if player == 1:
                game_window.blit(text2, (90, 200))
                game_window.blit(text1, (390, 200))

            else:
                game_window.blit(text1, (90, 200))
                game_window.blit(text2, (390, 200))

            for button in buttons_obj_list:
                button.draw(game_window)

            # score, tie = game.get_score()
            if game_obj.ng == 1:
                score = [0, 0]
                ties = 0

            score_font = pygame.font.SysFont("comicsans", 30)
            score_text = score_font.render("score ", 1, (0, 255, 255))
            game_window.blit(score_text, (40, 10))

            score_text = score_font.render("player 0 --> " + str(score[0]), 1, (255, 255, 255))
            game_window.blit(score_text, (40, 30))

            score_text = score_font.render("player 1 --> " + str(score[1]), 1, (255, 255, 255))
            game_window.blit(score_text, (40, 50))

            score_font = pygame.font.SysFont("comicsans", 30)
            score_text = score_font.render("ties: " + str(ties), 1, (0, 255, 255))
            game_window.blit(score_text, (200, 10))

        pygame.display.update()

class Button:

    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 60
        GUI = RPS_GUI()
        self.game_window = GUI.game_window

    def draw(self, game_window):
        pygame.draw.rect(game_window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(self.text, 1, (255,255,255))
        game_window.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

RPS = RPS_GUI()
buttons_obj_list = [Button("Rock", 40, 350, (0, 0, 0)), Button("Scissors", 225, 350, (0, 0, 255)),Button("Paper", 400, 350, (192, 192, 192)), Button("NewGame", 450, 2, (255, 0, 0))]
while True:
    RPS.menu_screen()
