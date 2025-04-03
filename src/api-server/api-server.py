"""
(C) Copyright 2025 Pietro Francesco Libri

This file is part of Nome-Programma.

    Nome-Programma is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Nome-Programma is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Nome-Programma.  If not, see <http://www.gnu.org/licenses/>.

"""

from fastapi import FastAPI
from pydantic import BaseModel

"""
API-SERVER: 
Runs the logic of the game
Communicates with the HTML-SERVER via REST API
"""

class Player:
    """
    Represents a player of the game
    """
    def __init__(self, name):
        self.name: str = name

    def __eq__(self, other):
        return self.name == other.name

class Board:
    """
    Represents the tic-tac-toe board
    """

    """Represents the marks on the board for the players"""
    player1_mark = 1
    player2_mark = 2

    def __init__(self, player1: Player, player2: Player):
        
        self.player1: Player = player1
        self.player2: Player = player2
        self.last_turn = self.player2
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.actions: int = 9

    def play(self, player, x, y): #la funzione ritorna 0 se il turno è andato a buon fine, player se il player ha vinto, 1 se è parità
        """
        Modifies the board
        Args:
            player: Player owner of the move
            x: X Position on the board to modify
            y: Y Position on the board to modify
        Returns:
            player if the move leads to victory
            3 if no player won but the board is full
            0 if the move is successfull 
            -1 if the move is not permitted
        """
        
        """Selects the mark to be impressed on the board"""
        mark: int
        match player:
            case self.player1:
                mark = Board.player1_mark
            case self.player2:
                mark = Board.player2_mark
            case _:
                mark = 0
        
        """Check if the move is invalid"""
        if self.board[y][x] != 0:
            return -1
        
        """Change the board"""
        self.board[y][x] = mark

        """Decrements the actions counter"""
        self.actions -= 1
        
        """Change the variable that keep memory of the last turn player"""
        self.last_turn = player

        """Check if the board has a victory configuration"""
        if self.check_victory() == 0:
            return player
        
        """Check if the board is full"""
        if self.check_end() == 0:
            return 3

        return 0
    
    def check_victory(self):
        """
        Check for a victory configuration

        Returns:
            0 if the board is in a victory configuration
            -1 otherwise
        """
            
        """Check for line configuration"""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] and self.board[i][1]== self.board[i][2] and self.board[i][0] != 0:
                return 0
        
        """Check for column configuration"""
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[1][i]== self.board[2][i] and self.board[0][i] != 0:
                return 0
        
        """Check for first diagonal configuration"""
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return 0
        
        """Check for second diagonal configuration"""
        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return 0
        
        return -1

    def check_end(self): #la funzione ritorna 0 solo se non ci sono più celle vuote
        """
        Check if the board is full looking to the variable that counts the actions done on the board
        Returns:
            0 if the board is full
            -1 otherwise
        """
        
        if self.actions == 0:
            return 0
        else:
            return -1
                
"""Create the FastAPI app"""
app = FastAPI()

"""Defines the global variables for the board and the players"""
board: Board
player1: Player
player2: Player 

class ServerResponse(BaseModel):
    """Represents the standard response given by this server"""
    response: int

class NameResponse(BaseModel):
    """Represents the standard response when receiving name from html-server"""
    name_1: str
    name_2: str

class CellResponse(BaseModel):
    """Represents the standard response when receiving cell position from html-server"""
    x: int
    y: int

class MoveResponse(BaseModel):
    """Represents the standard response given by this server when a move is done"""
    player: int
    player_name: str
    x: int
    y: int
    response: int

        
@app.post("/start_game")
def start_game(names: NameResponse):
    """
    Initializes the game
    Called when POST on /start_game on this server

    Args:
        names: names of the two player 
    Returns:
        ServerResponse with response 0 if successfull
    """ 

    """Recalls the global variables in this scope"""
    global board
    global player1
    global player2

    """Unwraps the NameResponse"""
    name_1 = names.name_1
    name_2 = names.name_2

    """Creates the instances for the players and the board"""
    player1 = Player(name_1)
    player2 = Player(name_2)
    board = Board(player1, player2)

    print("Gioco creato con successo")
    print("Giocatore 1: ", player1.name)
    print("Giocatore 2: ", player2.name)

    return ServerResponse(response=0)

@app.post("/play_game")
def play_game(cell: CellResponse):
    """
    Tries to make a move on the board
    Called when POST on /play_game on this server

    Args:
        cell: cell clicked by the player
    Returns:
        MoveResponse with
          the number of the player
          the name of the player
          the cell coordinates tried
          the response: 
            0 if the move is successfull
            1 if the first player won
            2 if the second player won
            3 if tie
            -1 if the move is not permitted
    """

    """Recalls the global variables in this scope"""
    global board
    global player1
    global player2

    """Unwraps the cell"""
    x = cell.x
    y = cell.y

    print("Ricevuta mossa: ", x,y)

    player: Player
    player_num: int

    """Check which player has to play this move"""
    if board.last_turn == player1:
            player = player2
            player_num = 2
    elif board.last_turn == player2:
            player = player1
            player_num = 1
    
    print("La mossa viene effettuata dal giocatore: ", player.name)

    """Tries to play the move"""
    result = board.play(player, x, y)

    """Returns based on result value"""

    if type(result) == type(player1):
        print("Vittoria del giocatore: ", player.name)
        if result == player1:
            return MoveResponse(player=player_num,response=1,x=x, y=y, player_name = player.name) #vittoria player1
        elif result == player2:
            return MoveResponse(player=player_num,response=2,x=x, y=y, player_name = player.name) #vittoria player2
    elif result == 0:
        print("Azione effettuata con successo")
        return MoveResponse(player=player_num,response=0,x=x, y=y, player_name = player.name) #azione effettuata
    elif result == 3:
        print("Parità")
        return MoveResponse(player=player_num,response=3,x=x, y=y, player_name = player.name) #parità
    elif result == -1:
        print("Mossa non valida")
        return MoveResponse(player=player_num, response=-1,x=x,y=y,player_name=player.name) #mossa non valida

