from csv import writer
from model import Player
from names import get_full_name
from random import randint, getrandbits


def get_test_players(total_player: int = 20, min_skill: int = 1, max_skill: int = 10):
    return [
        Player(
            name=get_full_name(),
            skill=randint(min_skill, max_skill),
            status=bool(getrandbits(1)),
        )
        for _ in range(total_player)
    ]


def main():
    dummy_list = get_test_players()
    with open("test_data.csv", "w", newline="") as file:
        data_writer = writer(file)
        data_writer.writerow(["name", "skill", "status"])
        for player in dummy_list:
            data_writer.writerow([player.name, player.skill, player.status])


if __name__ == "__main__":
    main()
