from events import Event

class State:
    def __init__(self):
        print("Enter " + self.__str__())

    def on_event(self, event):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


class SleepState(State):
    def on_event(self, event):
        if event == Event.activate:
            return ActiveState()
        
        return self


class ActiveState(State):
    def on_event(self, event):
        if event == Event.deactivate:
            return SleepState()

        if event == Event.motion_detected:
            return TriggeredState()
    
        return self


class TriggeredState(State):
    def on_event(self, event):
        if event == Event.deactivate:
            return SleepState()

        if event == Event.timeout:
            return AlarmState()

        return self


class AlarmState(State):
    def on_event(self, event):
        if event == Event.deactivate:
            return SleepState()

        return self

