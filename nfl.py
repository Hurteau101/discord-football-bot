from prizepicks import PrizePicks


class NFL(PrizePicks):
    def __init__(self):
        super().__init__()
        self.projection_id = 9
        self.nfl_data = self.api_call(projection_id=self.projection_id)







