class Event:
    def __init__(self, event):
        self.event = event
    def __str__(self): 
        return self.event
    def __cmp__(self, other):
        return cmp(self.event, other.event)
    def __hash__(self):
        return hash(self.event)

# Static fields; an enumeration of instances:
Event.activate = Event("activate")
Event.motion_detected = Event("motion detected")
Event.deactivate = Event("deactivate")
Event.timeout = Event("timeout")
