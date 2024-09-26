from flask import Flask, jsonify, request, send_from_directory
import json
from game import Game  # Assuming game.py contains the Game class

app = Flask(__name__)
game_instance = Game()

# Route to serve the HTML file
@app.route('/')
def index():
    return send_from_directory('', 'functionallity.html')

# Route to start the game
@app.route('/start_game', methods=['GET'])
def start_game():
    game_instance.__init__()  # Reset the game
    current_room = game_instance.current_room
    return jsonify({
        "description": "You are at the entrance of the facility.",
        "current_room": current_room,
        "agent_alive": game_instance.agent_alive
    })

# Route to process a choice
@app.route('/process_choice', methods=['POST'])
def process_choice():
    data = request.get_json()
    room = data['room']
    choice = data['choice']

    # Process based on current room and choice
    if room == "entrance":
        game_instance.current_room = game_instance.entrance()
    elif room == "dark_hallway":
        game_instance.current_room = game_instance.dark_hallway()
    elif room == "glowing_door":
        game_instance.current_room = game_instance.glowing_door()

    next_room = game_instance.current_room
    description = f"You are in {next_room}."
    return jsonify({
        "description": description,
        "next_room": next_room,
        "agent_alive": game_instance.agent_alive
    })

if __name__ == "__main__":
    app.run(debug=True)
