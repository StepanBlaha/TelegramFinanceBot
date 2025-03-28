class DependencyContainer:
    def __init__(self, Client, AI, Utils, Plot, Admin, Dataframe, Indicators):
        self.Client = Client
        self.AI = AI
        self.Utils = Utils
        self.Plot = Plot
        self.Admin = Admin
        self.Dataframe = Dataframe
        self.Indicators = Indicators

    def get(self, class_name):
        return getattr(self, class_name)