from event.event import EventType, Event


class EventManager:
    def __init__(self):
        self.listeners = {etype: [] for etype in EventType}

    def register(self, event_type: EventType, listener: callable):
        self.listeners[event_type].append(listener)

    def unregister(self, event_type: EventType, listener: callable):
        self.listeners[event_type].remove(listener)

    def dispatch(self, event: Event):
        for listener in self.listeners[event.type]:
            listener(event)
