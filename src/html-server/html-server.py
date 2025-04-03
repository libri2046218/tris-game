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

See LICENSE file for details.

This file includes code from third-party libraries:
- Jinja2 (BSD 3-Clause License)
- Requests (Apache License 2.0)

See THIRD_PARTY_LICENSES file for full details on third-party licenses.

"""

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests
from pydantic import BaseModel
import os

"""Creates the FastAPI app"""
app = FastAPI()

"""Creates the Jinja2Templates"""
templates = Jinja2Templates(directory="./templates")

"""Creates the local data structures representing the board graphics"""
cell_class = ["cell","cell","cell","cell","cell","cell","cell","cell","cell"]
cell_body = ["","","","","","","","",""]
empty_cell = "cell"
x_cell = "cell x"
o_cell = "cell o"

def reset_board():
    """Resets the board graphics"""
    global cell_class
    global cell_body
    cell_class = ["cell","cell","cell","cell","cell","cell","cell","cell","cell"]
    cell_body = ["","","","","","","","",""]

"""
Address of the API-SERVER
check if running from orchestrated containers 
"""
if os.environ.get('IN_CONTAINER', False): 
    API_BASE_URL = "http://api-server:8000"
else:
    API_BASE_URL = "http://127.0.0.1:8000"

@app.get("/")
def index(request: Request):
    """
    Called when GET on / on this server
    Returns:
        HTML Home Page
    """

    print("Requested / ")
    
    return templates.TemplateResponse("index.html", {"request":request})

class NameResponse(BaseModel):
    """Represents the standard response from HTML Form in index.html page"""
    player1: str
    player2: str

@app.post("/start-game")
def start_game(request: Request, names:NameResponse = Form(...)):
    """
    Called when POST on /start-game on this server
    Args:
        names: names of the players inserted in the HTML Form
    Returns:
        HTML Game Page if successfull
        HTML Error Page if error occured
    """

    print("Requested /start-game")

    """Recall the global variables in this scope"""
    global cell_class
    global cell_body

    """Wraps player names to be sent via POST request"""
    data = {"name_1": names.player1,
            "name_2": names.player2}
    
    print("Inserted players: ", names.player1, names.player2)

    """Tries sending POST request to API-SERVER"""
    try:
        response = requests.post(f"{API_BASE_URL}/start_game", json=data)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        print("ERROR in start_game", e)
        return templates.TemplateResponse("error.html", {"request": request})

    """Reset the board"""
    reset_board()

    return templates.TemplateResponse("game.html", {"request":request})

class PositionResponse(BaseModel):
    """Represents the standard response from HTML Form in game.html page"""
    position: int

"""Converts position in 0:8 rapresentation in 0,0:2,2 rapresentation"""
pos_to_coord = {0:(0,0), 1: (1,0), 2: (2,0), 3: (0,1), 4: (1,1), 5: (2,1), 6: (0,2), 7: (1,2), 8: (2,2)}

@app.post("/move")
def move(request: Request, cell: PositionResponse = Form(...)):
    """
    Called when POST on /move on this server
    Args:
        cell: cell position clicked on the HTML page
    Returns:
        HTML Game page unchanged if move is not permitted
        HTML Game page changed if move is successfull
        HTML Won page if one of the players won
        HTML Tie page if tie
        HTML Error page if error occured
    """

    """Recalls global variables in this scope"""
    global pos_to_coord
    global cell_class
    global cell_body

    """Unwraps the cell"""
    position = cell.position

    """Converts the cell position rapresentation and wraps the data to be sent via POST request"""
    x,y = pos_to_coord[position]
    data = {"x": x,
            "y": y}
    
    """Tries to make the move sending POST request to API-SERVER"""
    try:
        response = requests.post(f"{API_BASE_URL}/play_game", json=data)
        response.raise_for_status()
        result = response.json()
    
    except requests.RequestException as e:
        print("ERROR in move", e)
        return templates.TemplateResponse("error.html", {"request":request})
    
    """Check if the move is invalid"""
    if result.get("response") == -1:
        return templates.TemplateResponse("game.html", {"request": request, 
                                                    "cell_class_0" : cell_class[0],
                                                    "cell_class_1" : cell_class[1],
                                                    "cell_class_2" : cell_class[2],
                                                    "cell_class_3" : cell_class[3],
                                                    "cell_class_4" : cell_class[4],
                                                    "cell_class_5" : cell_class[5],
                                                    "cell_class_6" : cell_class[6],
                                                    "cell_class_7" : cell_class[7],
                                                    "cell_class_8" : cell_class[8],
                                                    "cell_body_0" : cell_body[0],
                                                    "cell_body_1" : cell_body[1],
                                                    "cell_body_2" : cell_body[2],
                                                    "cell_body_3" : cell_body[3],
                                                    "cell_body_4" : cell_body[4],
                                                    "cell_body_5" : cell_body[5],
                                                    "cell_body_6" : cell_body[6],
                                                    "cell_body_7" : cell_body[7],
                                                    "cell_body_8" : cell_body[8],})

    """Unwraps the result"""
    name = result.get("player_name")

    """Check the player mark (x or o)"""
    match result.get("player"):
        case 1:
            cell_class[position] = x_cell
            cell_body[position] = "x"
        case 2:
            cell_class[position] = o_cell
            cell_body[position] = "o"

    "Check the response of the API-SERVER"
    match result.get("response"):
        case 1:
            return templates.TemplateResponse("won.html", {"request": request, "player": name})
        case 2:
            return templates.TemplateResponse("won.html", {"request": request, "player": name})
        case 0:
            
            return templates.TemplateResponse("game.html", {"request": request, 
                                                    "cell_class_0" : cell_class[0],
                                                    "cell_class_1" : cell_class[1],
                                                    "cell_class_2" : cell_class[2],
                                                    "cell_class_3" : cell_class[3],
                                                    "cell_class_4" : cell_class[4],
                                                    "cell_class_5" : cell_class[5],
                                                    "cell_class_6" : cell_class[6],
                                                    "cell_class_7" : cell_class[7],
                                                    "cell_class_8" : cell_class[8],
                                                    "cell_body_0" : cell_body[0],
                                                    "cell_body_1" : cell_body[1],
                                                    "cell_body_2" : cell_body[2],
                                                    "cell_body_3" : cell_body[3],
                                                    "cell_body_4" : cell_body[4],
                                                    "cell_body_5" : cell_body[5],
                                                    "cell_body_6" : cell_body[6],
                                                    "cell_body_7" : cell_body[7],
                                                    "cell_body_8" : cell_body[8],})

        case 3:
            return templates.TemplateResponse("tie.html", {"request": request})
        

    
    