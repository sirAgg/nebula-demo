class ButtonInput():
    def __init__(self, function):
        self.prev_state = False
        self.func = function

    def pressed(self):
        state = self.func()

        ret = state and not self.prev_state
        self.prev_state = state

        return ret
