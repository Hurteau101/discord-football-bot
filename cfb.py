from prizepicks import PrizePicks

class CFB(PrizePicks):
    def __init__(self):
        super().__init__()
        self.projection_id = 15
        self.cfb_data = self.api_call(projection_id=self.projection_id)







