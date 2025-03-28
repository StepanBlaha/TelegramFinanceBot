
class FunctionsBase:
    def __init__(self, Client, AI, Utils, Indicators, Plot, Dataframe):
        self.client = Client()
        self.ai = AI()
        self.utils = Utils()
        self.indicators = Indicators()
        self.plot = Plot()
        self.dataframe = Dataframe()