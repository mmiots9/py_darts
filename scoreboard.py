VALID_SCORES = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12,
                '13': 13, '14': 14, '15': 15, '16': 16, '17': 17, '18': 18, '19': 19, '20': 20, '25': 25, 'd1': 2,
                'd2': 4, 'd3': 6, 'd4': 8, 'd5': 10, 'd6': 12, 'd7': 14, 'd8': 16, 'd9': 18, 'd10': 20, 'd11': 22,
                'd12': 24, 'd13': 26, 'd14': 28, 'd15': 30, 'd16': 32, 'd17': 34, 'd18': 36, 'd19': 38, 'd20': 40,
                'd25': 50, 't1': 3, 't2': 6, 't3': 9, 't4': 12, 't5': 15, 't6': 18, 't7': 21, 't8': 24, 't9': 27,
                't10': 30, 't11': 33, 't12': 36, 't13': 39, 't14': 42, 't15': 45, 't16': 48, 't17': 51, 't18': 54,
                't19': 57, 't20': 60, '0': 0, 'NA': 0}


class Scoreboard:

    def __init__(self):
        self.valid_scores = VALID_SCORES

    def check_visit(self, visit):
        return all(visit[i] in self.valid_scores for i in range(len(visit)))

    def has_busted(self, player, temp_score):
        return temp_score == 1 or \
               temp_score < 0 or \
               (temp_score == 0 and not self.check_closing(player))

    def calculate_visit_score(self, player):
        visit = player.darts[-1]
        visit_score = sum(self.to_num_scores(visit))
        return visit_score

    def to_num_scores(self, dart_list):
        return [self.valid_scores[dart] for dart in dart_list]

    def get_subtracted_score(self, player):
        visit_score = self.calculate_visit_score(player)
        new_score = player.scores[-1] - visit_score
        return new_score

    def check_closing(self, player):
        return "d" in player.darts[-1][-1]

    def calculate_n_darts(self, player):
        return len([dart for visit in player.darts for dart in visit])
