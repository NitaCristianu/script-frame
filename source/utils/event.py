class EventManager:
    def __init__(self):
        self.events = []  # List to store events
        self.listeners = {}  # Dictionary to store listeners for each event type

    def add_listener(self, event_type, callback):
        """Add a listener function for a specific event type."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def remove_listener(self, event_type, callback):
        """Remove a listener function for a specific event type."""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    def fire_event(self, event_type, **data):
        """Post a custom event with data."""
        self.events.append((event_type, data))

    def process_events(self):
        """Process and dispatch all events in the event list."""
        while self.events:
            event_type, data = self.events.pop(0)
            if event_type in self.listeners:
                for callback in self.listeners[event_type]:
                    callback(**data)
            