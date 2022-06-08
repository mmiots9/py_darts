from datetime import date
from player import Player
from scoreboard import Scoreboard

STARTING_SCORE = 501


class Training501:

    def __init__(self):
        self.date = date.today()
        self.starting_score = STARTING_SCORE
        self.player = Player(self.starting_score)
        self.scoreboard = Scoreboard()

        print("Training 501 leg")
        print(f"Hi {self.player.name}, game on!")
        self.play_game(self.player, self.scoreboard)

    def play_game(self, player, scoreboard):
        """This function make a player play a training 501 leg"""

        self.play_visit(player, scoreboard)

        # calculate temp score
        temp_score = scoreboard.get_subtracted_score(player)

        # check if busted, end game or should continue
        if scoreboard.has_busted(player, temp_score):
            print("No score!")
            player.scores.append(player.scores[-1])
            self.play_game(player, scoreboard)
            return
        elif temp_score > 0:
            player.scores.append(temp_score)
            self.play_game(player, scoreboard)
            return
        else: # end of the game
            player.scores.append(temp_score)
            scoreboard.add_na(player)
            print(f"Congratulations!")
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

