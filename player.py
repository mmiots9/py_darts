class Player:

    def __init__(self, score):
        self.name = None
        self.scores = [score]
        self.darts = []
        self.ask_name()

    def throw_darts(self):
        visit_hits = input("1st dart, 2nd dart, 3rd dart (write 'undo' to undo last visit): ").lower()
        visit_list = [hit.strip() for hit in visit_hits.split(sep = ",")]
        return visit_list

    def undo(self):
        if len(self.scores) == 1:
            print("Sorry, you can't undo prior to throw the first darts")
            return
        self.scores = self.scores[:-1]
        self.darts = self.darts[:-1]

    def ask_name(self):
        """This function asks for player name and return it"""
        self.name = input("What is the player name?\n")
