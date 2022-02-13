class Puzzle:

    def __init__(self, location, options={}):
        self.location = location
        self.options = options


    def get_option_stories(self):
        story = ""
        for key in self.options.values():
            story += key["storyline"] + "  "
        return story.capitalize()


    def update_option(self, option):
        if option in self.options.keys():
            self.options[option]["storyline"] = self.options[option]["new_story"]
            if self.options[option]["option"][1] == "Active":
                self.options[option]["option"][1] = "Inactive"