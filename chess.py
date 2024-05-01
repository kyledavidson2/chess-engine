#CIS3700 Assignment 2
#Date: 2023-03-03
#Author: Kyle Davidson

import re
import copy

class Piece:
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.isAlive = True
        self.start_pos = position
    
class Pawn(Piece):
    value = 1

    def __init__(self, colour, position):
        super().__init__(colour, position)

    def __str__(self):
        return f'{self.colour}P'

    def generate_moves(self, pieces):
        moves = []

        #2 forward from start position
        if self.start_pos == self.position:
            result, occupied = check_space(self.position, 'up', pieces, self.colour, offset=2)
            if result and not occupied: moves.append(result)
        
        #1 forward
        result, occupied = check_space(self.position, 'up', pieces, self.colour)
        if result and not occupied: moves.append(result)

        #check diagonals for pieces
        upr, occupied_r = check_space(self.position, 'up_r', pieces, self.colour)
        upl, occupied_l = check_space(self.position, 'up_l', pieces, self.colour)

        if upr and occupied_r:
            moves.append(upr)

        if upl and occupied_l:
            moves.append(upl)

        return moves

class Rook(Piece):
    value = 4

    def __str__(self):
        return f'{self.colour}R'

    def generate_moves(self, pieces):
        moves = []

        directions = ['up','down','left','right']
        for d in directions:
            moves.extend(check_direction(self.position, d, pieces, self.colour))

        #print(moves)
        return moves
            
class Bishop(Piece):
    value = 3

    def __str__(self):
        return f'{self.colour}B'

    def generate_moves(self, pieces):
        moves = []

        directions = ['up_r','down_r','up_l','down_l']
        for d in directions:
            moves.extend(check_direction(self.position, d, pieces, self.colour))

        #print(moves)
        return moves

class Knight(Piece):
    value = 3

    def __str__(self):
        return f'{self.colour}N'
    
    def generate_moves(self, pieces):
        moves = []
        
        #can move in any direction, colour doesnt matter
        possible_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

        k = self.position[0]
        l = self.position[1]

        for p in possible_moves:
            if (0 <= p[0]+k < 8) and (0 <= p[1]+l < 8): 
                if pieces[p[0]+k][p[1]+l] == 0:
                    moves.append((p[0]+k,p[1]+l))
                elif pieces[p[0]+k][p[1]+l].colour != self.colour:
                    moves.append((p[0]+k,p[1]+l))
        #print(moves)
        return moves

class King(Piece):
    value = 1000

    def __str__(self):
        return f'{self.colour}K'

    def generate_moves(self, pieces):
        moves = []

        directions = ['up','down','left','right','up_r','down_r','up_l','down_l']
        for d in directions:
            result, occupied = check_space(self.position, d, pieces, self.colour)
            if result: moves.append(result)

        if self.start_pos == self.position:
            left_rook = pieces[self.position[0]][0]
            right_rook = pieces[self.position[0]][7]

            if left_rook and type(left_rook) is Rook and left_rook.colour == self.colour:
                #castling queenside
                if len(check_direction(self.position, 'left', pieces, self.colour)) == 3:
                    result, occupied = check_space(self.position, 'left', pieces, self.colour, offset=2)
                    if result: moves.append(result)

            if right_rook and type(right_rook) is Rook and right_rook.colour == self.colour:
                #castling kingside
                if len(check_direction(self.position, 'right', pieces, self.colour)) == 2:
                    result, occupied = check_space(self.position, 'right', pieces, self.colour, offset=2)
                    if result: moves.append(result)
        
        return moves
        
class Queen(Piece):
    value = 5

    def __str__(self):
        return f'{self.colour}Q'

    def generate_moves(self, pieces):
        moves = []

        #check each direction
        directions = ['up','down','left','right','up_r','down_r','up_l','down_l']
        for d in directions:
            moves.extend(check_direction(self.position, d, pieces, self.colour))

        return moves

def check_direction(position, direction, pieces, colour):
    #check a direction until a piece is hit
    #used for rook, bishop, queen

    moves = []
    result, occupied = check_space(position, direction, pieces, colour)
    while (result):
        moves.append(result)
        if occupied: break
        result, occupied = check_space(result, direction, pieces, colour)

    return moves

def check_space(position, direction, pieces, colour, offset=1):
    #check a space within a distance of 1

    #i, j
    directions = {
        'up': (-1,0),
        'down': (1,0),
        'left': (0,-1),
        'right': (0,1),
        'up_r': (-1,1),
        'up_l': (-1,-1),
        'down_r': (1,1),
        'down_l': (1,-1),
    }

    i, j = directions[direction]

    #offset of 2 is only used for initial pawn move and castling
    i *= offset
    j *= offset
    
    k = position[0]
    l = position[1]

    if colour == 'b':
        #reverse direction
        i *= -1
 
    #return if empty space or opposite colour
    if (0 <= i+k < 8) and (0 <= j+l < 8): 
        if pieces[i+k][j+l] == 0:
            return (i+k,j+l), False
        elif pieces[i+k][j+l].colour != colour:
            return (i+k,j+l), True

    return False, False

class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class ChessGame:
    def __init__(self):
        self.board = Board()

    def to_move(self,state):
        return state.player

    def is_cutoff(self,state,depth): 
        #max depth reached in search tree       
        if depth == 3: 
            return True
        return False

    def is_terminal(self,state,player):
        #if either king is dead

        w_king = state.find_opp_king('b')
        b_king = state.find_opp_king('w')

        if not w_king.isAlive or not b_king.isAlive:
            return True
    
    def actions(self,state,player):
        #return all moves for player
        return state.generate_full_moves(player)

    def result(self,state,a):
        #make a copy of the board and make the move
        board = copy.deepcopy(state)
        board.move_piece(a.start, a.end, state.player)
        return board

    def eval(self,state,player):
        #compute value of state for player
        #sum the value for each alive piece for each player
        #also add a small incentive for moving forward

        w_val = 0
        b_val = 0

        for p in state.w_pieces:
            if p.isAlive: w_val += p.value + (0.25 * abs(p.position[0] - p.start_pos[0]))
        for p in state.b_pieces:
            if p.isAlive: b_val += p.value + (0.25 * abs(p.position[0] - p.start_pos[0]))

        if player == 'w':
            return w_val - b_val
        
        return b_val - w_val

    def is_check(self,state,player):
        #is the current state a check for player

        king = state.find_opp_king(player)
        all_moves = state.generate_all_moves(player)

        if king.position in all_moves:
            return True
        return False

    def is_checkmate(self, state):
        #will only be run after is_check

        all_opp_moves = state.generate_full_moves(state.player) #opposing player's moves
        for m in all_opp_moves:
            #try every opposing move and see if it breaks the check
            result = self.result(state,m)
            if not self.is_check(result,result.player):
                return False

        return True

    def __str__(self):
        return self.board.to_str()

class Board:
    size = 8

    def __init__(self):
        self.player = 'w'
        self.w_pieces = []
        self.b_pieces = []
        self.pieces = [] #8x8 array

    def init_board(self):
        #outside of __init__ so that board copies don't need to run this
        self.w_pieces = [
            Rook('w', (7,0)),
            Rook('w',(7,7)),
            Knight('w',(7,1)),
            Knight('w',(7,6)),
            Bishop('w',(7,2)),
            Bishop('w',(7,5)),
            Queen('w',(7,3)),
            King('w',(7,4)),
        ]
        self.b_pieces = [
            Rook('b', (0,0)),
            Rook('b',(0,7)),
            Knight('b',(0,1)),
            Knight('b',(0,6)),
            Bishop('b',(0,2)),
            Bishop('b',(0,5)),
            Queen('b',(0,3)),
            King('b',(0,4)),
        ]
        for j in range(self.size):
            self.b_pieces.append(Pawn('b', (1,j)))
            self.w_pieces.append(Pawn('w', (6,j)))
        
        self.pieces = [[0 for i in range(self.size)] for j in range(self.size)]
        self.init_pieces()

    def init_pieces(self):
        #place pieces into the array

        for p in self.w_pieces:
            i, j = p.position
            self.pieces[i][j] = p 

        for p in self.b_pieces:
            i, j = p.position
            self.pieces[i][j] = p

    def switch_player(self):
        if self.player == 'w':
            self.player = 'b'
        else:
            self.player = 'w'

    def move_piece(self, pos1, pos2, colour):        
        i1, j1 = pos1
        i2, j2 = pos2
        
        #check if there is a piece at the location
        #should have already been verified before calling
        if game.board.pieces[i1][j1] == 0:
            return False

        piece = self.pieces[i1][j1]

        #if there is a piece at the result location
        if self.pieces[i2][j2]:
            self.pieces[i2][j2].isAlive = False

        self.pieces[i2][j2] = self.pieces[i1][j1] #move to that location
        self.pieces[i1][j1] = 0 #replace old location with nothing
        if piece: piece.position = (i2,j2) #update position of piece

        #promotion
        if type(piece) is Pawn:
            if abs(piece.position[0] - piece.start_pos[0]) == 6:
                piece.isAlive = False

                #human player should be able to choose but that wasnt implemented
                #ai will always pick queen because it has highest value
                new_piece = Queen(colour, (i2,j2))
                self.pieces[i2][j2] = new_piece

                if colour == 'w':
                    self.w_pieces.append(new_piece)
                else:
                    self.b_pieces.append(new_piece)

        #castling
        if type(piece) is King:
            if j1-j2 == 2: #if moving left by 2
                #move left rook to the right of king
                self.pieces[i2][j2+1] = self.pieces[i2][0]
                self.pieces[i2][0] = 0
            elif j1-j2 == -2: #if moving right by 2
                #move right rook to the left of king
                self.pieces[i2][j2-1] = self.pieces[i2][7]
                self.pieces[i2][7] = 0

        self.switch_player()
    
    def is_move_valid(self,pos1,pos2,colour):
        i1, j1 = pos1
        i2, j2 = pos2

        #check if there is a piece at the location
        if game.board.pieces[i1][j1] == 0:
            return False

        piece = self.pieces[i1][j1]

        if piece.colour != colour: #if trying to move piece that is not the player's
            return False
        if (i2,j2) not in piece.generate_moves(self.pieces): #if not valid move
            return False

        #should also check if the move puts self in check but it doesnt

        return True

        
    def generate_all_moves(self, colour):
        #only the results, used for check and checkmate
        moves = []
        piece_list = []

        if colour == 'w':
            piece_list = self.w_pieces 
        elif colour == 'b':
            piece_list = self.b_pieces

        for p in piece_list:
            if p.isAlive: 
                moves.extend(p.generate_moves(self.pieces))

        return moves

    def generate_full_moves(self, colour):
        #starting point and result, for move evaluation
        moves = []
        piece_list = []

        if colour == 'w':
            piece_list = self.w_pieces 
        elif colour == 'b':
            piece_list = self.b_pieces

        for p in piece_list:
            if p.isAlive: 
                for m in p.generate_moves(self.pieces):
                    moves.append(Move(p.position, m))

        return moves

    def find_opp_king(self, colour):
        #get the opposing king

        if colour == 'w':
            for p in self.b_pieces:
                if type(p) is King:
                    return p
        elif colour == 'b':
            for p in self.w_pieces:
                if type(p) is King:
                    return p

        return None

    def to_str(self, pov='w'):
        #print the board in a grid
        #point of view is changed based on player

        output = ''
        location = 0
        for i in range(self.size):
            if pov == 'w': 
                output += str(7-i+1) + '  '
            else: 
                output += str(i+1) + '  '
            for j in range(self.size):
                if pov == 'w':
                    location = i
                else:
                    location = 7-i

                if self.pieces[location][j] == 0:
                    output += '.  '
                else:
                    output += str(self.pieces[location][j]) + '  '
                if self.pieces[location][j] == 0:
                    output += ' '
            output += '\n\n'
        output += '   '
        for i in range(self.size):
            output += chr(i+65) + '   '

        return output

def coord_to_index(coords):
    #only used for player input
    #computer will communicate with array indices

    #a1 is bottom left white side
    #we want to convert a1 to (0,0)
    coords = coords.upper()
    if not re.match("^[A-H][1-8]$", coords):
        return (-1,-1)

    f, r = [*coords] #file, rank

    return (8-(ord(r)-48), ord(f)-65)

def index_to_coord(index):
    f, r = index
    return chr(r+65) + chr(8-f+48)


#algorithm from textbook page 200
def alpha_beta_search(game,state):
    org_player = game.to_move(state) #original player
    value, move = max_value(game, state, float('-inf'), float('inf'), 0, org_player)
    return move, value

def max_value(game,state,alpha,beta,depth,org_player):
    player = game.to_move(state) #player for generating actions

    if game.is_cutoff(state,depth): #depth = 3
        return game.eval(state,org_player), None

    if game.is_terminal(state,org_player): #if either king is dead
        return game.eval(state,org_player), None

    v = float('-inf')
    for a in game.actions(state, player):
        v2, a2 = min_value(game, game.result(state, a), alpha, beta, depth+1,org_player)
        if v2 > v:
            v,move = v2,a
            alpha = max(alpha,v)
        if v >= beta:
            return v, move
    return v, move

def min_value(game,state,alpha,beta,depth,org_player):
    player = game.to_move(state) #player for generating actions

    if game.is_cutoff(state,depth): #depth = 3
        return game.eval(state,org_player), None

    if game.is_terminal(state,org_player): #if either king is dead
        return game.eval(state,org_player), None

    v = float('inf')
    for a in game.actions(state, player):
        v2,a2 = max_value(game,game.result(state,a),alpha,beta, depth+1,org_player)
        if v2 < v:
            v,move = v2,a
            beta = min(beta,v)
        if v <= alpha:
            return v,move
    return v,move

#start chess
print('Moves are in the form: (start) (end), ex. a2 a3')
while(1):
    print('Select number of players: 1 or 2')
    try: 
        n_players = int(input())
    except:
        continue
    if n_players == 1 or n_players == 2:
        break
while(n_players == 1):
    print('Select colour: w or b')
    p_colour = input()
    if p_colour == 'w' or p_colour == 'b':
        break

if n_players == 2:
    p_colour = 'w'

#start the game
game = ChessGame()
game.board.init_board()
print(game.board.to_str(p_colour))
#print(game.board)

#input loop for getting moves and printing board
while(1):
    to_move = game.to_move(game.board)

    if p_colour == to_move: #player move
        while(1):
            print(f'enter {to_move} move')
            p_input = input()

            if n_players == 1 and p_input == 'retire': #let the ai take over
                p_colour = 'r'
                break

            move = p_input.split(' ')
            try:
                i,j = coord_to_index(move[0])
                k,l = coord_to_index(move[1])

                #move piece if valid move
                if game.board.is_move_valid((i,j),(k,l), to_move):
                    game.board.move_piece((i,j), (k,l), to_move)
                    break

            except Exception as e:
                #print(e)
                continue

        if n_players == 2: 
            #switch colour
            p_colour = game.to_move(game.board)

        print(game.board.to_str(p_colour))
        
    else: #ai move
        print(f'{to_move} move')
        print('thinking...')

        move, value = alpha_beta_search(game, game.board)
        game.board.move_piece(move.start, move.end, to_move)

        print(game.board.to_str(p_colour))
        print(f'{to_move} moves from {index_to_coord(move.start)} to {index_to_coord(move.end)} with a value of {value}\n')

    #there is no rule implemented to prevent player from putting itself into check
    #can still lose without checkmate
    if game.is_terminal(game.board, to_move):
        game.board.switch_player()
        print(f'{game.board.player} wins!')
        break

    if game.is_check(game.board, to_move):
        print(f'{to_move} check')
        if game.is_checkmate(game.board):
            print(f'{to_move} checkmate')
            game.board.switch_player()
            print(f'{game.board.player} wins!')
            break
