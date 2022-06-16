from datetime import date, datetime, timedelta, time
from player import Player
from scoreboard import Scoreboard
from random import randint, choices
from string import ascii_lowercase
import csv

STARTING_SCORE = 501
TRAINING_ID_PREFIX = "xx"


class Training501:

    def __init__(self):
        self.metadata = {}
        self.darts = {}

    def play_game(self):
        self.game_start()
        self.game_development(self.temp_player, self.temp_scoreboard)
        self.game_end()

    def game_start(self):
        self.temp_player = Player(STARTING_SCORE)
        self.temp_scoreboard = Scoreboard()
        self.add_temp_metadata()
        print("Training 501 leg")
        print(f"Hi {self.temp_player.name}, game on!")

    def add_temp_metadata(self):
        self.temp_game_date = date.today()
        self.temp_game_id = self.create_game_id()
        self.temp_game_start_time = datetime.now().time().replace(microsecond=0)

    def create_game_id(self):
        numeric_part = randint(0, 9)
        letters_part = "".join(choices(ascii_lowercase, k=3))
        return f"{TRAINING_ID_PREFIX}{numeric_part}{letters_part}"

    def game_development(self, player, scoreboard):
        """This function make a player play a training 501 leg"""
        self.play_visit(player, scoreboard)
        # calculate temp score
        temp_score = scoreboard.get_subtracted_score(player)
        # check if busted, end game or should continue
        if scoreboard.has_busted(player, temp_score):
            print("No score!")
            player.scores.append(player.scores[-1])
            self.game_development(player, scoreboard)
            return
        elif temp_score > 0:
            player.scores.append(temp_score)
            self.game_development(player, scoreboard)
            return
        else:  # end of the game
            player.scores.append(temp_score)
            return

    def play_visit(self, player, scoreboard):
        # Show Points
        print(f"\nYour score is {player.scores[-1]}")
        # Ask Thrown Darts
        visit = player.throw_darts()
        # Check if darts are valid
        if not scoreboard.check_visit(visit):
            if 'undo' in visit:
                player.undo()
            else:
                print("Sorry, you have entered invalid values. Retry!")
            self.play_visit(player, scoreboard)
        else:
            player.darts.append(visit)

    def game_end(self):
        self.add_final_metadata(self.temp_scoreboard, self.temp_player)
        self.add_darts(self.temp_player)

        # TODO: remove temp things from self
        self.remove_temp_attributes()

        print(f"Congratulations! You've completed the training")

    def add_final_metadata(self, scoreboard, player):
        self.temp_game_end_time = datetime.now().time().replace(microsecond=0)
        self.temp_total_time = self.calculate_total_time()
        self.temp_n_darts = scoreboard.calculate_n_darts(player)
        self.metadata[self.temp_game_id] = {
            "id": self.temp_game_id,
            "player": self.temp_player.name,
            "date": self.temp_game_date,
            "start_time": self.temp_game_start_time,
            "end_time": self.temp_game_end_time,
            "total_time": self.temp_total_time,
            "n_darts": self.temp_n_darts
        }

    def calculate_total_time(self):
        delta_time = timedelta(hours=self.temp_game_end_time.hour - self.temp_game_start_time.hour,
                               minutes=self.temp_game_end_time.minute - self.temp_game_start_time.minute,
                               seconds=self.temp_game_end_time.second - self.temp_game_start_time.second)
        str_time = time(delta_time.seconds // 3600, delta_time.seconds // 60, delta_time.seconds % 60)
        return str_time

    def add_darts(self, player):
        visit_list = []
        visit_n = 0
        for visit in player.darts:
            visit_n += 1
            for _ in visit:
                visit_list.append(visit_n)

        self.darts[self.temp_game_id] = {
            "visit": visit_list,
            "darts": [dart for visit in player.darts for dart in visit]
        }

    def remove_temp_attributes(self):
        temp_attr_list = [attr for attr in list(self.__dict__.keys()) if "temp_" in attr]
        for attr in temp_attr_list:
            self.__delattr__(attr)

    def save_game(self, file_to_write):
        with open(file=file_to_write, mode="a") as my_file:
            wr = csv.writer(my_file)
            for id in self.metadata.keys():
                wr.writerow(list(self.metadata[id].values()))
                wr.writerow(self.darts[id]["visit"])
                wr.writerow(self.darts[id]["darts"])
