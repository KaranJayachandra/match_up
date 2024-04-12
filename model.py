from csv import reader
from pathlib import Path
from dataclasses import dataclass
from random import randint, sample
from math import floor

PLAYERS_PER_COURT = 4


@dataclass
class Player:
    name: str
    skill: int
    status: bool


@dataclass
class Team:
    player_1: str
    player_2: str


@dataclass
class Game:
    court: int
    team_1: Team
    team_2: Team


class PlayerList:
    def __init__(self, location: Path = "players.csv"):
        with open(location, newline="") as file:
            data_reader = reader(file)
            next(data_reader, None)
            self.players = [
                (
                    Player(
                        name=row[0],
                        skill=row[1],
                        status=(row[2] == "True"),
                    )
                )
                for row in data_reader
            ]

    def get_active_players(self):
        return [player for player in self.players if player.status]

    def get_player(self, player_request: str):
        return [player for player in self.players if player.name == player_request]

    def toggle_player(self, player_request: Player):
        self.players = [
            (
                Player(
                    name=player.name,
                    skill=player.skill,
                    status=not player.status,
                )
                if player.name == player_request
                else player
            )
            for player in self.players
        ]

    def __str__(self):
        display_string = ""
        for player in self.players:
            display_string += player.__str__() + "\n"
        return display_string


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


class GameList:

    def set_court_count(self, count: int):
        self.court = count
        self.reset()

    def new_round(self, players: PlayerList):
        number_of_games = min(floor(len(players) / PLAYERS_PER_COURT), self.court)
        number_of_players = number_of_games * PLAYERS_PER_COURT
        print(number_of_games)
        print(number_of_players)
        print(len(players))
        selection = sample(players, number_of_players)
        grouped_selection = divide_chunks(selection, PLAYERS_PER_COURT)
        self.games = [
            Game(
                court=idx + 1,
                team_1=Team(
                    player_1=selected_chunk[0].name, player_2=selected_chunk[1].name
                ),
                team_2=Team(
                    player_1=selected_chunk[2].name, player_2=selected_chunk[3].name
                ),
            )
            for idx, selected_chunk in enumerate(grouped_selection)
        ]

    def reset(self):
        self.games = []
