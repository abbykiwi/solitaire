"""
Implements a simplified Solitaire game with a GUI

"""
from tkinter import *
import random

class Solitaire:
    # implements the class of the game of Solitaire
    def __init__(self, num_cards):
        # initialises the values of the deques the number of cards, the number of columns and the number of chances
        self.t = []
        ncards = []
        while len(ncards) < num_cards:
            num = random.randrange(0, num_cards)
            if num not in ncards:
                ncards.append(num)
        self.__CardNo = len(ncards)
        self.__ColNo = (self.__CardNo // 8) + 3
        self.__ChanceNo = self.__CardNo * 2 + 3
        for i in range(self.__ColNo):
            self.t.append(Deque())
        for i in range(self.__CardNo):
            self.t[0].add_front(Card(ncards[i], 0))
        self.starting = True

    def play(self):
        # implements the playing of the game andcreates the original canvas/ Tk object
        self.window = Tk()
        self.window.title("Solitaire - CompSci 130 Assignment 2")
        self.canvas = True
        canvas_width = 1000
        canvas_height = 700
        self.a_canvas = Canvas(self.window, width=canvas_width, height=canvas_height)
        self.a_canvas.pack(expand=False)
        
        #displays the gui with all the cards in place to start the game
        self.display_gui(self.a_canvas, first=True)
        self.window.wm_protocol("WM_DELETE_WINDOW", self.quit)  
        self.window.mainloop()
            
    def display_gui(self, a_canvas, first=False):
        global blanks_list
        global rounds
        columns = self.__ColNo
        cards = self.__CardNo
        
        # creates the starting layout of the cards, with all the cards in pile 0
        left = 175
        down = 25
        if first == True:
            # creates the blank starting columns
            for l in range(1, columns):
                c = Card("", l)
                c.create_blank(left, down, a_canvas, self.window)
                blanks_list.append(c)
                left += 150
            left = 25 
                
        if self.t[0].size() == cards:
            # places all the cards on the first column in a random order
            items = self.t[0].get_list_of_all()
            for j in range(cards):
                if j == cards - 1:
                    items[j].create(left, down, j, True, a_canvas, self.window)
                else:
                    items[j].create(left, down, j, False, a_canvas, self.window)
                down += 25 
                left += 5
            down = 25 
            left += 150
            
            # creates the rotate button and the rounds counter
            b = Rotate_Button()
            b.create(70, down*cards+200, self.window)
            
            rounds.create(100, 650, self.window)

    def get_deques(self):
        # returns the list of deques in the game
        return self.t

    def get_chances(self):
        # returns the number of chances the player has
        return self.__ChanceNo
    
    def win(self):
        # creates the window that pops up when the player wins the game
        self.win_window = Tk()
        self.win_window.title("You Win!")
        canvas_width = 450
        canvas_height = 200
        a_canvas = Canvas(self.win_window, width=canvas_width, height=canvas_height)
        a_canvas.pack(expand=True)
        a_canvas.create_text(225, 50, text="YOU WIN!", font=("Courier New", 50), fill="green")
        # creates a button for the play again and quit options
        again = Button(self.win_window, text="Play Again", font=('Courier New', 20), command=self.play_again)
        again.place(x=50, y=100)
        quit = Button(self.win_window, text="Quit", font=('Courier New', 20), command=self.quit)
        quit.place(x=250, y=100)
        self.canvas = False
        #destroys the game window
        self.window.destroy()

    def lose(self):
        # creates the window that appears when the player loses the game
        self.win_window = Tk()
        self.win_window.title("You Lose!")
        canvas_width = 450
        canvas_height = 200
        a_canvas = Canvas(self.win_window, width=canvas_width, height=canvas_height)
        a_canvas.pack(expand=True)
        a_canvas.create_text(225, 50, text="YOU LOSE!", font=("Courier New", 50), fill="red")
        # creates a button for the play again and quit options
        again = Button(self.win_window, text="Play Again", font=('Courier New', 20), command=self.play_again)
        again.place(x=50, y=100)
        quit = Button(self.win_window, text="Quit", font=('Courier New', 20), command=self.quit)
        quit.place(x=250, y=100)
        self.canvas = False
        #destroys the game window
        self.window.destroy()

    def play_again(self):
        # allows the player to play again
        global playing
        playing = True
        self.win_window.destroy()

    def quit(self):
        # quits the game
        global playing
        if self.canvas == True:
            #quits the game when the player is in game
            self.window.destroy()
        else:
            # quits the game when the player has finished a game
            self.win_window.destroy()
        playing = False
          
class Card:
    # implements the card class the creates and manages each card in the game
    def __init__(self, value, column):
        global deques
        global columns_selected
        columns_selected = columns_selected
        self.value = value
        self.a_canvas = None
        self.colours = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']
        self.colour = None
        self.x = 0
        self.y = 0
        self.column_num = column
        self.clicked = False
    
    def create(self, x, y, num, last, a_canvas, window):
        #creates a card and places it in the window at the given x and y coordinates
        self.colour = self.colours[num]
        self.a_canvas = a_canvas
        if last:
            if self.value >= 10:
                # if the value of the card is less than 10 - need to implement different padding for the text on the label
                self.l = Label(window, text=self.value, bg="white", relief="solid", padx=27, pady=62, font=("Courier", 29))
                # the cards are implemented as label widgets to make it easier to manange and use them in the game
            else:
                self.l = Label(window, text=self.value, bg="white", relief="solid", padx=38, pady=62, font=('Courier', 29))
            self.l.place(x=x, y=y)
            # binds the label to different events e.g. if the mouse hovers, leaves or clicks on the label
            self.l.bind("<Button-1>", self.select_card)
            self.l.bind("<Enter>", self.hover)
            self.l.bind("<Leave>", self.leave)
        else:
            if self.value >= 10:
                self.l = Label(window, text=self.value, bg=self.colour, relief="solid", padx=27, pady=62, activebackground='red', font=('Courier', 29))
            else:
                self.l = Label(window, text=self.value, bg=self.colour, relief="solid", padx=38, pady=62, activebackground='red', font=('Courier', 29))
            self.l.place(x=x, y=y)
            
        self.x = x
        self.y = y
        self.num = num
    
    def create_blank(self, x, y, a_canvas, window, ):
        #creates a blank (black) base card
        self.a_canvas = a_canvas
        self.l = Label(window, text="", bg="black", padx=45, pady=70)
        self.l.place(x=x, y=y)
        self.l.bind("<Button-1>", self.select_card)
        self.l.bind("<Enter>", self.hover)
        self.l.bind("<Leave>", self.leave_blank)
        
    def select_card(self, event):
        # determines what happens when the card is clicked
        if self.clicked == True:
            # if the card was already selected, clicking it again would deselect it
            self.deselect()
        else:
            # if the card was not already selected
            self.clicked = True
            self.l.config(bg="red")
            columns_selected.append(self.get_column())
            if len(columns_selected) == 2:
                # if there are two columns selected the moves the cards from pile 1 to pile 2
                # calls the move function to move the two selected cards
                move(deques, columns_selected[0], columns_selected[1])
                for i in range(len(columns_selected)):
                    # removed the pile numbers from the columns_selected list
                    columns_selected.pop()
            if len(columns_selected) > 2:
                # deselect the two cards if there are more than two piles in the list 
                self.deselect()
                
    def hover(self, event):
        #if the mouse is placed over a card, it will turn red
        self.l.config(bg="red")
    
    def leave(self, event):
        # when the mouse leaves a card (playing card), without clicking it, it turns back to white
        if self.clicked == False:
            self.l.config(bg="white")
            
    def leave_blank(self, event):
        # when the mouse leaves a blank base card without clicking it, it turns back to black
        if self.clicked == False:
            self.l.config(bg="black")
        if columns_selected == []:
            self.l.config(bg="black")
            
    def get_column(self):
        #returns the column number of the card
        return self.column_num
    def get_value(self):
        #returns the numerical value of the card
        return self.value
    
    def move_card(self, x, y):
        #moves the card on the canvas
        self.l.place(x=x, y=y)
        self.l.config(bg="white")
        self.x = x
        self.y = y
    
    def set_deque(self, column):
        #changes the deque/column number of the card
        self.column_num = column
        
    def set_last(self):
        # sets the card as being the last card in the pile, therefore allowing for it to be selected/moved
        self.l.config(bg="white")
        self.l.bind("<Button-1>", self.select_card)
        self.l.bind("<Enter>", self.hover)
        self.l.bind("<Leave>", self.leave)
        
    def set_not_last(self):
        # sets the card as being not the last card in the pile, therefore not allowing for it to be selected/moved
        self.l.config(bg=self.colour)
        self.l.unbind("<Button-1>")
        self.l.unbind("<Enter>")
        self.l.unbind("<Leave>")
        
    def __lt__(self, other):
        # determines whether the card is less than another card
        if self.value < other.value:
            return True
        else:
            return False

    def deselect(self):
        # implements the deselection of the cards
        self.clicked = False
        self.l.config(bg='white')
        columns_selected.pop(columns_selected.index(self.get_column()))

    def invalid_move(self):
        # deselects the card if there is an invalid move
        self.deselect()


class RoundCounter:
    def __init__(self, total):
        # implements the round counter that counts the round and determines if the player has lost the game
        self.a_canvas = None
        self.x = None
        self.y = None
        self.total = total
        self.current = 1
        self.string = 'Round 1 out of {}'.format(self.total)
    def create(self, x, y, window):
        # creates the Round Counter label on the canvas
        self.l = Label(window, text=self.string, font=('Courier', 40))
        self.l.place(x=x, y=y)
    def increment(self):
        # increments the round counter 
        self.current += 1
        self.string = 'Round {} out of {}'.format(self.current, self.total)
        self.l.config(text=self.string)
    def check_lose(self):
        # determines if the player has exceeded the number of moves given and therefore determines if the player loses the game
        global game
        if self.current >= self.total:
            game.lose()
        elif self.current >= self.total-3:
            # when there are only three moves remaining the text turns red
            self.l.config(fg='red')


class Rotate_Button:
    # implements the rotate button that rotates the cards from the front of pile zero to the back of pile zero
    def __init__(self):
        self.a_canvas = None
    def create(self, x, y, window):
        # creates the rotate button on the tkinter canvas
        global deques
        self.b = Button(window, text="Rotate", command=self.clicked, font=("Courier", 30))
        self.b.place(x=x, y=y)
    def clicked(self):
        # calls the move function to move the card from the back of pile zero to the front of pile zero
        self.b.config(relief=SUNKEN)
        move(deques, 0, 0)


class Deque:
    # implements the deque class that keeps track of the queue of cards for each pile
    def __init__(self):
        # intiates a list to store the items in the queue
        self.items = []
    def add_front(self, item):
        # adds an item to the front of the queue
        self.items.append(item)
    def add_rear(self, item):
        # adds an item to the rear of the queue
        self.items.insert(0, item)
    def remove_front(self):
        # removes an item from the front of the queue and returns it
        removed = self.items.pop()
        return removed
    def remove_rear(self):
        # removes an item from the rear of the queue and returns it
        removed = self.items.pop(0)
        return removed
    def size(self):
        # returns the size of the deque
        return len(self.items)
    def peek(self):
        # returns the item at the front of the queue
        return self.items[-1]
    def peeklast(self):
        # returns the item at the back of the queue
        return self.items[0]
    def get_list_of_all(self):
        # returns a list of all the items in the deque
        return [self.items[i] for i in range(len(self.items))] 
    def printall(self):
        # prints all the elements in the deque
        if self.size() >= 1:
            for i in range(len(self.items)):
                print(self.items[i].get_value(), end=" ")   
        print()
    def index(self, index):
        # returns the index of an item in the queue
        return self.items[index]
    def __iter__(self):
        # calls the iteration class to iterate through the items in the deque
        return DequeIteration(self.items)

class DequeIteration:
    # implements the iteration through an instance of the deque class
    def __init__(self, lst):
        self.max = len(lst)
        self.current = 0
        self.lst = lst

    def __next__(self):
        # returns the next element in the deque class, otherwise it raises the StopIteration exception
        if self.current == self.max:
            raise StopIteration
        else:
            current = self.lst[self.current]
            self.current += 1
            return current

                 
def move(deque, c1, c2):
    # implements the movement of the cards from one pile to another
    global blanks_list
    global game
    global rounds
    if deque[c1].size() > 0 and deque[c2].size() >= 0:
        if c1 == 0 and c2 == 0:
            # if moving from the front of pile 0 to the back of pile 0
            removed = deque[c1].remove_front()
            deque[c2].add_rear(removed)
            removed.set_deque(c2)
            removed.clicked = False
            removed.set_not_last()
            for counter, value in enumerate(deque[c2]):
                value.move_card(column_coordinates[c2]+(counter*5), (25*(counter+1)))
                value.l.lift()
                value.set_not_last()
            deque[c2].peek().set_last()
            #checks if the game is lost, then increments the round counter
            rounds.check_lose()
            rounds.increment()
        
        elif c1 == 0 and c2 > 0:
            # if c1 is pile 0 and c2 is not pile 0
            if deque[c2].size() == 0:
                # if the deque of c2 is empty
                removed = deque[c1].remove_front()
                deque[c2].add_rear(removed)
                removed.move_card(column_coordinates[c2], 25)
                removed.clicked = False
                removed.set_deque(c2)
                blanks_list[c2].clicked = False
                if deque[c1].size() > 0:
                    deque[c1].peek().set_last()
                # checks if the game is won, otherwise checks if the game is lost then increments the round counter
                if IsComplete(deque[c2]):
                    game.win()
                else:
                    rounds.check_lose()
                    rounds.increment()
            
            elif deque[c1].peek().get_value() == deque[c2].peeklast().get_value() - 1: 
                #moving from pile 0 to a non-empty c2 pile
                removed = deque[c1].remove_front()
                last_other = deque[c2].peeklast()
                deque[c2].add_rear(removed)
                removed.move_card(column_coordinates[c2]+((deque[c2].size()*5)-5), 25*deque[c2].size())
                removed.l.lift()
                removed.clicked = False
                blanks_list[c2].clicked = False
                removed.set_deque(c2)
                if deque[c1].size() > 0:
                    deque[c1].peek().set_last()
                last_other.clicked = False
                last_other.set_not_last()
                if IsComplete(deque[c2]):
                    game.win()
                else:
                    rounds.check_lose()
                    rounds.increment()
            # if the move is invalid, deselect the two cards
            else:
                deque[c1].peek().invalid_move()
                deque[c2].peeklast().invalid_move()

        elif c1 > 0 and c2 > 0:
            # if c1 is not pile 0 and c2 is not pile 0
            if deque[c2].size() == 0:
                for i in range(deque[c1].size()):
                    last = deque[c1].peek()
                    if deque[c2].size() > 0:
                        last_other = deque[c2].peeklast()
                        last_other.set_not_last()
                    deque[c2].add_rear(deque[c1].peek())
                    deque[c1].remove_front()
                    last.move_card(column_coordinates[c2]+((deque[c2].size()*5)-5), 25*deque[c2].size())
                    last.clicked = False
                    blanks_list[c2].clicked = False
                    last.set_deque(c2)
                    if deque[c1].size() != 0:
                        last.set_not_last()
                    else:
                        last.set_last()
                    if IsComplete(deque[c2]):
                        game.win()
                rounds.check_lose()
                rounds.increment()
                        
            elif deque[c1].peek().get_value() == deque[c2].peeklast().get_value() - 1:
                # if the card on c1 is smaller than the card on c2 by 1
                for i in range(deque[c1].size()):
                    removed = deque[c1].remove_front()
                    last_other = deque[c2].peeklast()
                    last_other.set_not_last()
                    last_other.clicked = False
                    deque[c2].add_rear(removed)
                    # removes the card for the deque and adds it to the other deque then move the carad physically to that deque
                    removed.move_card(column_coordinates[c2]+((deque[c2].size()*5)-5), 25*deque[c2].size())
                    removed.l.lift()
                    removed.clicked = False
                    blanks_list[c2].clicked = False
                    removed.set_deque(c2)
                    if IsComplete(deque[c2]):
                        game.win()
                rounds.check_lose()
                rounds.increment()
            
            else:
                deque[c1].peek().invalid_move()
                deque[c2].peeklast().invalid_move()

def IsComplete(deque):
    # determines if the game is complete and if the player has won the game
    global deques
    global num_cards
    if deque.size() == num_cards:
        return True
    return False

playing = True
while playing:
    # creates the playing of the game which continues until the player closes the game
    columns_selected = []
    column_coordinates = [25, 175, 325, 475, 625, 775] # stores the x coordinates of each of the pile
    blanks_list = [0]
    num_cards = 11 #starts the game with 11 cards
    game = Solitaire(num_cards)
    rounds = RoundCounter(game.get_chances())
    deques = game.get_deques()
    game.play() # begins the game
