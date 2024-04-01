#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Rafał Biedrzycki
Kodu tego mogą używać moi studenci na ćwiczeniach z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów, aby mogli skupić się na algorytmach sztucznej inteligencji. 
Kod nie jest wzorem dobrej jakości programowania w Pythonie, nie jest również wzorem programowania obiektowego, może zawierać błędy.
Mam świadomość wielu jego braków ale nie mam czasu na jego poprawianie.

Zasady gry: https://en.wikipedia.org/wiki/English_draughts (w skrócie: wszyscy ruszają się po 1 polu. Pionki tylko w kierunku wroga, damki w dowolnym)
  z następującymi modyfikacjami: a) bicie nie jest wymagane,  b) dozwolone jest tylko pojedyncze bicie (bez serii).

Nalezy napisac funkcje minimax_a_b_recurr, minimax_a_b (woła funkcję rekurencyjną) i  evaluate, która ocenia stan gry

Chętni mogą ulepszać mój kod (trzeba oznaczyć komentarzem co zostało zmienione), mogą również dodać obsługę bicia wielokrotnego i wymagania bicia. Mogą również wdrożyć reguły: https://en.wikipedia.org/wiki/Russian_draughts
"""

import numpy as np
import pygame
from copy import deepcopy

FPS = 20

#MINIMAX_DEPTH = 5
Blue_depth=3
White_depth=3

WIN_WIDTH = 800
WIN_HEIGHT = 800


BOARD_WIDTH = 8

FIELD_SIZE = WIN_WIDTH/BOARD_WIDTH
PIECE_SIZE = FIELD_SIZE/2 - 8
MARK_THICK = 2
POS_MOVE_MARK_SIZE = PIECE_SIZE/2


WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

class Move:
    def __init__(self, piece, dest_row, dest_col, captures=None):
        self.piece=piece
        self.dest_row=dest_row
        self.dest_col=dest_col
        self.captures=captures

class Field:
    def draw(self):
        pass
    
    def is_empty(self):
        return True
    
    def is_white(self):
        return False

    def is_blue(self):
        return False
    
    def toogle_mark(self):    
        pass
    
    def is_move_mark(self):
        return False    
    
    def is_marked(self):
        return False       

    def __str__(self):
        return "."
    
class PosMoveField(Field):
    def __init__(self, is_white, window, row, col, board, row_from, col_from, pos_move):
        self.__is_white=is_white
        self.__is_marked =False 
        self.window = window
        self.row = row
        self.col = col
        self.board = board
        self.row_from = row_from
        self.col_from = col_from
        self.pos_move=pos_move
        
            
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result                
        
    def draw(self):
        x = self.col*FIELD_SIZE
        y = self.row*FIELD_SIZE
        pygame.draw.circle(self.window, RED, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), POS_MOVE_MARK_SIZE)
    
    def is_empty(self):
        return True
        
    def is_move_mark(self):
        return True

class Pawn(Field):    
    def __init__(self, is_white, window, row, col, board):
        self.__is_white=is_white
        self.__is_marked =False 
        self.window = window
        self.row = row
        self.col = col
        self.board = board
        
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result  

    def __str__(self):
        if self.is_white():
            return "w"
        return "b"
            
    def is_king(self):
        return False
    
    def is_empty(self):
        return False
    
    def is_white(self):
        return self.__is_white

    def is_blue(self):
        return not self.__is_white
    
    def is_marked(self):
        return self.__is_marked
    
    def toogle_mark(self):
        if self.__is_marked:
            for pos_move in self.pos_moves: #remove possible moves
                row = pos_move.dest_row
                col = pos_move.dest_col
                self.board.board[row][col] = Field()
            self.pos_moves=[]
        else:#self.is_marked
            self.pos_moves = self.board.get_piece_moves(self)
            for pos_move in self.pos_moves:
                row = pos_move.dest_row
                col = pos_move.dest_col
                self.board.board[row][col] = PosMoveField(False, self.window, row, col, self.board, self.row, self.col, pos_move)
            
        self.__is_marked = not self.__is_marked
    
    def draw(self):
        if self.__is_white:
            cur_col = WHITE
        else:
            cur_col = BLUE
        x = self.col*FIELD_SIZE
        y = self.row*FIELD_SIZE
        pygame.draw.circle(self.window, cur_col, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE)

        if self.__is_marked:
            pygame.draw.circle(self.window, RED, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE+MARK_THICK, MARK_THICK)

class King(Pawn):    
    def __init__(self, pawn):
        super().__init__(pawn.is_white(), pawn.window, pawn.row, pawn.col, pawn.board)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        return result  
    
    def is_king(self):
        return True

    def __str__(self):
        if self.is_white():
            return "W"
        return "B"
    
    def draw(self):
        if self.is_white():
            cur_col = WHITE
        else:
            cur_col = BLUE
        x = self.col*FIELD_SIZE
        y = self.row*FIELD_SIZE
        pygame.draw.circle(self.window, cur_col, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE)
        pygame.draw.circle(self.window, GREEN, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE/2)

        if self.is_marked():
            pygame.draw.circle(self.window, RED, (x+FIELD_SIZE/2, y+FIELD_SIZE/2), PIECE_SIZE+MARK_THICK, MARK_THICK)

class Board:
    def __init__(self, window): #row, col
        self.board = []#np.full((BOARD_WIDTH, BOARD_WIDTH), None)
        self.window = window
        self.marked_piece = None 
        self.something_is_marked=False
        self.white_turn = True
        self.white_fig_left = 12
        self.blue_fig_left = 12

        self.__set_pieces()
        
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.__dict__.update(self.__dict__)
        result.board= deepcopy(self.board )
        return result  

    def __str__(self):
        to_ret=""
        for row in range(8):
            for col in range(8):
                to_ret+=str(self.board[row][col])
            to_ret+="\n"
        return to_ret
        
    def __set_pieces(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                self.board[row].append( Field() )

        for row in range(3):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(False, self.window, row, col, self)

        for row in range(5, 8):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                self.board[row][col] = Pawn(True, self.window, row, col, self)


    def get_piece_moves(self, piece):
        pos_moves=[]
        row = piece.row
        col = piece.col
        if piece.is_blue():
            enemy_is_white = True
        else:
            enemy_is_white = False

        if piece.is_white() or (piece.is_blue() and piece.is_king()):            
            dir_y = -1
            if row > 0:
                new_row=row+dir_y
                if col > 0:
                    new_col=col-1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece, new_row, new_col))  
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y>=0 and new_col-1>=0 and self.board[new_row+dir_y][new_col-1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col-1, self.board[new_row][new_col]))  
                        
                if col < BOARD_WIDTH-1:
                    new_col=col+1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))    
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y>=0 and new_col+1<BOARD_WIDTH and self.board[new_row+dir_y][new_col+1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col+1, self.board[new_row][new_col]))  

        if piece.is_blue() or (piece.is_white() and self.board[row][col].is_king()):
            dir_y = 1
            if row<BOARD_WIDTH-1:
                new_row=row+dir_y
                if col > 0:
                    new_col=col-1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))    
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y<BOARD_WIDTH and new_col-1>=0 and self.board[new_row+dir_y][new_col-1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col-1, self.board[new_row][new_col]))  
                        
                if col < BOARD_WIDTH-1:
                    new_col=col+1
                    if self.board[new_row][new_col].is_empty():
                        pos_moves.append(Move(piece,new_row, new_col))    
                        #ruch zwiazany z biciem
                    elif self.board[new_row][new_col].is_white()==enemy_is_white and new_row+dir_y<BOARD_WIDTH and new_col+1<BOARD_WIDTH and self.board[new_row+dir_y][new_col+1].is_empty():
                        pos_moves.append(Move(piece,new_row+dir_y, new_col+1, self.board[new_row][new_col]))  
        return pos_moves
    
    #ToDo
    def evaluate(self, is_blue_turn):
        h=0
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                pawn = self.board[row][col]
                if type(pawn) is not Field:
                    if pawn.is_blue():
                        if pawn.is_king():
                            h += 10
                        else:
                            h += 1
                    if pawn.is_white():
                        if pawn.is_king():
                            h -= 10
                        else:
                            h -= 1
        return h

    def evaluate1(self, is_blue_turn):
        h=0
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                pawn = self.board[row][col]
                if type(pawn) is not Field:
                    if pawn.is_blue():
                        if pawn.is_king():
                            h += 1
                        else:
                            h += 1
                    if pawn.is_white():
                        if pawn.is_king():
                            h -= 1
                        else:
                            h -= 1
        return h

    def evaluate2(self, is_blue_turn):
        h = 0
        for row in range(BOARD_WIDTH):
            for col in range((row + 1) % 2, BOARD_WIDTH, 2):
                pawn = self.board[row][col]
                if type(pawn) is not Field:
                    if pawn.is_blue():
                        if row < 4:
                            if pawn.is_king():
                                h += 10
                            else:
                                h += 5
                        else:
                            if pawn.is_king():
                                h += 10
                            else:
                                h += 7
                    if pawn.is_white():
                        if row >= 4:
                            if pawn.is_king():
                                h -= 10
                            else:
                                h -= 5
                        else:
                            if pawn.is_king():
                                h -= 10
                            else:
                                h -= 7
        return h

    def evaluate3(self, is_blue_turn):
        h = 0
        for row in range(BOARD_WIDTH):
            for col in range((row + 1) % 2, BOARD_WIDTH, 2):
                pawn = self.board[row][col]
                if type(pawn) is not Field:
                    if pawn.is_blue():
                        if pawn.is_king():
                            h += 10
                        else:
                            h += 5 + (7 - row)
                    if pawn.is_white():
                        if pawn.is_king():
                            h -= 10
                        else:
                            h -= 5 + row
        return h

    def get_possible_moves(self, is_blue_turn):
        pos_moves = []
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                if not self.board[row][col].is_empty():
                    if (is_blue_turn and self.board[row][col].is_blue()) or (not is_blue_turn and self.board[row][col].is_white()):                        
                        pos_moves.extend( self.get_piece_moves(self.board[row][col]) )
        return pos_moves
        
                
    def draw(self):
        self.window.fill(WHITE)
        for row in range(BOARD_WIDTH):
            for col in range((row+1) % 2, BOARD_WIDTH, 2):
                y = row*FIELD_SIZE
                x = col*FIELD_SIZE
                pygame.draw.rect(self.window, BLACK, (x, y , FIELD_SIZE, FIELD_SIZE))
                self.board[row][col].draw()
                            

  
    def move(self, field):
        d_row = field.row
        d_col = field.col
        row_from = field.row_from
        col_from = field.col_from
        self.board[row_from][col_from].toogle_mark()
        self.something_is_marked = False
        self.board[d_row][d_col]=self.board[row_from][col_from]
        self.board[d_row][d_col].row=d_row
        self.board[d_row][d_col].col=d_col
        self.board[row_from][col_from]=Field()     

        if field.pos_move.captures:
            fig_to_del = field.pos_move.captures
            
            self.board[fig_to_del.row][fig_to_del.col]=Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1
            
        if self.white_turn and d_row==0:#damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        if not self.white_turn and d_row==BOARD_WIDTH-1:#damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])
            
        self.white_turn = not self.white_turn
    
    def end(self):
        return self.white_fig_left==0 or self.blue_fig_left==0 or len(self.get_possible_moves(not self.white_turn))==0
        
    def clicked_at(self, row, col):
        field = self.board[row][col]
        if field.is_move_mark():
            self.move(field)
        if (field.is_white() and self.white_turn and not self.something_is_marked) or (field.is_blue() and not self.white_turn and not self.something_is_marked):
            field.toogle_mark()
            self.something_is_marked = True
        elif self.something_is_marked and field.is_marked():
            field.toogle_mark()
            self.something_is_marked = False

    #tu spore powtorzenie kodu z move            
    def make_ai_move(self, move):                
        d_row = move.dest_row
        d_col = move.dest_col
        row_from = move.piece.row
        col_from = move.piece.col

        self.board[d_row][d_col]=self.board[row_from][col_from]
        self.board[d_row][d_col].row=d_row
        self.board[d_row][d_col].col=d_col
        self.board[row_from][col_from]=Field()     

        if move.captures:
            fig_to_del = move.captures
            
            self.board[fig_to_del.row][fig_to_del.col]=Field()
            if self.white_turn:
                self.blue_fig_left -= 1
            else:
                self.white_fig_left -= 1
            
        if self.white_turn and d_row==0:#damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])

        if not self.white_turn and d_row==BOARD_WIDTH-1:#damka
            self.board[d_row][d_col] = King(self.board[d_row][d_col])
            
        self.white_turn = not self.white_turn
        

class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board(window)

    def update(self):
        self.board.draw()
        pygame.display.update()
    
    def mouse_to_indexes(self, pos):
        return (int(pos[0]//FIELD_SIZE), int(pos[1]//FIELD_SIZE))

    def clicked_at(self, pos):
        (col, row) = self.mouse_to_indexes(pos)
        self.board.clicked_at(row, col)
        


#ToDo
#max to niebieski
def minimax_a_b(board, depth):
    a = float('-inf') #najleoszy wybrór dla max
    b = float('inf') #najleoszy wybrór dla min
    move_value_max = float('-inf')
    move_value_min = float('inf')
    move_max = not board.white_turn #max domyślnie niebieski
    moves = list(set(board.get_possible_moves(move_max)))
    best_move = np.random.choice(moves)
    for move in moves:
        board_copy = deepcopy(board)
        board_copy.make_ai_move(move)
        move_value = minimax_a_b_recurr(board_copy, depth-1, not move_max, a, b)
        if move_max:
            if move_value > move_value_max:
                best_move = move
                move_value_max = move_value
        else:
            if move_value < move_value_min:
                best_move = move
                move_value_min = move_value
    return best_move

#ToDo
def minimax_a_b_recurr(board, depth, move_max, a, b):
    if depth == 0 or board.end():
        return board.evaluate(move_max)
    moves = board.get_possible_moves(move_max)
    if move_max:
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.make_ai_move(move)
            a = max(a,minimax_a_b_recurr(board_copy, depth-1, False, a, b))
            if a >= b:
                return b
        return a
    else:
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.make_ai_move(move)
            b = min(b, minimax_a_b_recurr(board_copy, depth - 1, True, a, b))
            if a >= b:
                return a
        return b

def alt_minimax_a_b(board, depth):
    a = float('-inf') #najleoszy wybrór dla max
    b = float('inf') #najleoszy wybrór dla min
    move_value_max = float('-inf')
    move_value_min = float('inf')
    move_max = not board.white_turn #max domyślnie niebieski
    moves = list(set(board.get_possible_moves(move_max)))
    best_move = np.random.choice(moves)
    #best_move_value = 0
    for move in moves:
        board_copy = deepcopy(board)
        board_copy.make_ai_move(move)
        move_value = alt_minimax_a_b_recurr(board_copy, depth-1, not move_max, a, b)
        #if best_move is None:
        #    best_move = move
        #    best_move_value = move_value
        if move_max:
            if move_value > move_value_max:
                best_move = move
                move_value_max = move_value
        else:
            if move_value < move_value_min:
                best_move = move
                move_value_min = move_value
    return best_move

def alt_minimax_a_b_recurr(board, depth, move_max, a, b):
    if depth == 0 or board.end():
        return board.evaluate1(move_max)
    moves = board.get_possible_moves(move_max)
    if move_max:
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.make_ai_move(move)
            a = max(a,alt_minimax_a_b_recurr(board_copy, depth-1, False, a, b))
            if a >= b:
                return b
        return a
    else:
        for move in moves:
            board_copy = deepcopy(board)
            board_copy.make_ai_move(move)
            b = min(b, alt_minimax_a_b_recurr(board_copy, depth - 1, True, a, b))
            if a >= b:
                return a
        return b

def main():
    w=0
    b=0
    x=1
    while x < 16:
        window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        is_running = True
        clock = pygame.time.Clock()
        game = Game(window)
        while is_running:
            clock.tick(FPS)
            if game.board.end():
                is_running = False
                if game.board.white_turn:
                    print("blue won")
                    pygame.quit()
                    b += 1
                    continue
                else:
                    print("white won")
                    pygame.quit()
                    w+=1
                    continue
            if not game.board.white_turn:
                move = alt_minimax_a_b( deepcopy(game.board), Blue_depth)
                game.board.make_ai_move(move)
            game.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                # dla gracza białych
                #if event.type == pygame.MOUSEBUTTONDOWN:
                #    pos = pygame.mouse.get_pos()
                #    game.clicked_at(pos)
                #dla ai białych
            if game.board.white_turn and not game.board.end():
                move = minimax_a_b(deepcopy(game.board), White_depth)
                game.board.make_ai_move(move)
            game.update()
        pygame.quit()
        x+=1
    print("white depth: ",White_depth," | ","blue depth: ",Blue_depth)
    print("white score: ",w," | ","blue score: ",b)

def main_notshowing():
    w=0
    b=0
    x=1
    while x < 16:
        window = None
        is_running = True
        clock = None
        board = Board(None)
        while is_running:
            if board.end():
                is_running = False
                if board.white_turn:
                    print("blue won")
                    b += 1
                    continue
                else:
                    print("white won")
                    w+=1
                    continue
            if not board.white_turn:
                move = alt_minimax_a_b( deepcopy(board), Blue_depth)
                board.make_ai_move(move)
                #dla ai białych
            if board.white_turn and not board.end():
                move = minimax_a_b(deepcopy(board), White_depth)
                board.make_ai_move(move)
        x+=1
    print("white depth: ",White_depth," | ","alt blue depth: ",Blue_depth)
    print("white score: ",w," | ","alt blue score: ",b)
main()
    
