from os import getenv
from model import PlayerList, GameList
from flask import Flask, abort, render_template
from dotenv import load_dotenv

load_dotenv()


print("Importing player list...\n")
PLAYER_LIST = PlayerList(location="data.csv")
print("List of player:\n")
print(PLAYER_LIST)
GAME_LIST = GameList()
GAME_LIST.set_court_count(4)

app = Flask("Match Up! Backend")
env_config = getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.j2")


@app.route("/player-toggle/<player_request>", methods=["POST"])
def toggle_player(player_request):
    selection = PLAYER_LIST.get_player(player_request)
    if len(selection) != 1:
        abort(404)
    PLAYER_LIST.toggle_player(player_request)
    selection = PLAYER_LIST.get_player(player_request)
    return render_template(
        "player.j2",
        player=selection[0],
    )


@app.route("/player-list", methods=["GET"])
def get_list_of_players():
    return render_template(
        "players.j2",
        players=PLAYER_LIST.players,
    )


@app.route("/new-games", methods=["POST"])
def new_games():
    GAME_LIST.new_round(PLAYER_LIST.get_active_players())
    return render_template(
        "games.j2",
        games=GAME_LIST.games,
    )


@app.route("/reset-games", methods=["POST"])
def reset_games():
    GAME_LIST.reset()
    return render_template(
        "no_games.j2",
    )


@app.route("/game-list", methods=["GET"])
def get_list_of_games():
    if len(GAME_LIST.games) == 0:
        return render_template(
            "no_games.j2",
        )
    else:
        return render_template(
            "games.j2",
            games=GAME_LIST.games,
        )
