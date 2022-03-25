class TextInputManager():

    def read(self):

        mapping = {
            "event_1": "event_1",
            "event_2": "event_2",
        }
        user_input = input("Input:")
        try:
            return [mapping[user_input]]
        except KeyError:
            print("Input not recognized")
            return []
