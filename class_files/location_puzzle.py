class Location_puzzle:

    def __init__(self, location, story, options, exit):
        self.location = location
        self.story = story
        self.options = options
        self.exit = exit

    def choose_option(self):
        for o in self.options:
            print(self.options[o]["text"])
        while True:
            x = input()
            for c in self.options.keys():

                if x == c:
                    print(self.options[x]["action"])
                    del self.options[x]
                    break










