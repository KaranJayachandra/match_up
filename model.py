from csv import reader
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Player:
    name: str
    skill: int
    status: bool


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
