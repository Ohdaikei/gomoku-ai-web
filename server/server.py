from flask import Flask, request, jsonify
import random
from flask_cors import CORS
from game import Game, BLACK, WHITE, EMPTY
from ai import AI

app = Flask(__name__)
# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app)

@app.route("/ai-move", methods=["POST"])
def ai_move():
    data = request.get_json()
    board = data.get("board")
    ai_color = data.get("aiColor", "black")

    game = Game()
    game.reset(ai_color, board)

    ai = AI(game.state())

    move, _ = ai.mcts_search()

    if move is None:
        return jsonify({"x" : -1, "y" : -1})
    
    x, y = move
    return jsonify({"x" : x, "y" : y})

# server.py 最後
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
