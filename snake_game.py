import curses
import time
import random
from curses import textpad

stdscr = curses.initscr()

menu = ['Start', 'Exit']


def print_menu(stdscr, selected_row_idx):

    h,  w = stdscr.getmaxyx()

    for idx,row in enumerate(menu):

        x = w//2 - len(menu)//2
        y = h//2 - len(menu)//2 + idx

        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        
        else:
            stdscr.addstr(y,x,row)

    stdscr.refresh()


def exit_func(stdscr):

    sh,  sw = stdscr.getmaxyx()

    exit_txt = "Exiting ...."

    stdscr.attron(curses.color_pair(1))

    stdscr.addstr(sh//2, sw//2, exit_txt)
    stdscr.attroff(curses.color_pair(1))

    stdscr.refresh()


def create_food(snake, box):
    food = None

    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]

        if food in snake:
            food = None

    return food

def print_score(stdscr, score):

    sh, sw = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(4)) # adding green color to food

    score_text = "Score: {}".format(score)
    stdscr.attron(curses.color_pair(4)) # adding green color to food

    stdscr.addstr(0, sw//2 - len(score_text)//2, score_text)
    stdscr.refresh()

def print_speed(snake_speed):
    
    if snake_speed >= 40 :
        speed = "Speed Mode: Slow".format(snake_speed)
        stdscr.addstr(2,2,speed)

        stdscr.refresh()


    elif snake_speed <= 40 :
        speed = "Speed Mode: Normal".format(snake_speed)
        stdscr.addstr(2,2,speed)

        stdscr.refresh()

    elif snake_speed <=20:
        speed = "Speed Mode: Fastest".format(snake_speed)
        stdscr.addstr(2,2,speed)

        stdscr.refresh()

    stdscr.refresh()

def game(stdscr):

    curses.curs_set(0)

    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.nodelay(1)

    snake_speed = 60 # Snake Speed starting value

    stdscr.timeout(snake_speed) # snake speed
    
    score = 0 # Score variable
        
    sh, sw = stdscr.getmaxyx() # getting screen size

    box = [[3,3], [sh-3, sw-3]] # setting "box" values

    textpad.rectangle(stdscr, box[0][0], box[0][1], box [1][0], box[1][1]) # Creating Reactangle

    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]] # Creating snake
    direction = curses.KEY_RIGHT

    for y,x in snake: # Snake Constantly move
        stdscr.attron(curses.color_pair(2)) # adding green color to snake

        stdscr.addstr(y, x, "$") # setting how snake will be on the screen and moving
        
        stdscr.attroff(curses.color_pair(2)) # adding green color to snake

    food = create_food(snake, box)


    stdscr.attron(curses.color_pair(3)) # adding blue color to food

    stdscr.addstr(food[0], food[1], '*') # printing food on the game

    stdscr.attroff(curses.color_pair(3)) # adding blue color to food

    print_score(stdscr, score)
    print_speed(snake_speed)

    while 1 : # Game Loop
        key = stdscr.getch()

        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key

        head = snake[0] # Creating head variable to control snake

        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1] # where to move snake if the user press RIGHT key

        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1] # where to snake move if the user press LEFT key
        
        elif direction== curses.KEY_UP:
            new_head = [head[0]-1, head[1]] # where to move snake if the user press UP key

        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]] # where to move snake if the user press DOWN key

        stdscr.attron(curses.color_pair(2)) # adding green color to snake

        snake.insert(0, new_head) # add new position with a new special key like "$"
        stdscr.addstr(new_head[0], new_head[1], "$") 

        stdscr.attroff(curses.color_pair(2)) # adding green color to snake

        if snake[0] == food : # if snake head touches a "*" of food
            
            food = create_food(snake, box) # create another food

            stdscr.attron(curses.color_pair(3)) # adding blue color to food

            stdscr.addstr(food[0], food[1], '*') # print to the screen another food

            stdscr.attroff(curses.color_pair(3)) # adding blue color to food

            score += 1 # add one to score variable
            snake_speed -= 5 # rest 5 to snake timeout so, it can go more faster
                
            print_score(stdscr, score)
            print_speed(snake_speed)

        else: # if case snake touches itself, print game over and exit the game
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()


            if (snake[0][0] in [box[0][0], box[1][0]] or
                snake[0][1] in [box[0][1], box[1][1]] or snake[0] in snake[1:]):

                msg = """Game Over! Score {}""".format(score)

                stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
                stdscr.refresh()
                time.sleep(2)
                
                break

            stdscr.refresh()


def starting_menu(stdscr):

    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    current_row_idx = 0
    
    print_menu(stdscr,current_row_idx)

    while 1 :

        stdscr.attron(curses.color_pair(2))

        stdscr.addstr(3,1,'''
     ███████╗███╗   ██╗ █████╗ ██╗  ██╗███████╗██╗
     ██╔════╝████╗  ██║██╔══██╗██║ ██╔╝██╔════╝██║
     ███████╗██╔██╗ ██║███████║█████╔╝ █████╗  ██║
     ╚════██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ╚═╝
     ███████║██║ ╚████║██║  ██║██║  ██╗███████╗██╗
     ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝''')
        
        stdscr.attroff(curses.color_pair(2))
        sh, sw = stdscr.getmaxyx()

        box = [[2,2], [sh-2, sw-2]]

        textpad.rectangle(stdscr, box[0][0], box[0][1], box [1][0], box[1][1])


        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
                    
        elif key == curses.KEY_DOWN and current_row_idx < len(menu)-1:
            current_row_idx += 1

        elif key == curses.KEY_ENTER or key in [10, 13]:

            if current_row_idx == len(menu)-1: # Exit Option
                exit_func(stdscr)
                time.sleep(2)
                break
                

            elif current_row_idx == len(menu)-2: # Start option
                start_txt = "Starting the game ..."
                stdscr.addstr(sh//2, sw//2, start_txt)
                stdscr.refresh()

                time.sleep(2)

                stdscr.clear()
                game(stdscr)
            


        print_menu(stdscr, current_row_idx)
        
        stdscr.refresh()

curses.wrapper(starting_menu)
