from genworlds.objects.abstracts.object import AbstractObject

class CustomObject(AbstractObject):
    def __init__(self, name, id, description, host_world_id=None, actions=[]):
        super().__init__(name, id, description, host_world_id, actions)
        self.event_listeners = []

    def register_event_listener(self, event_type, listener):
        """
        Register an event listener for a specific event type.
        """
        self.event_listeners.append((event_type, listener))

    def unregister_event_listener(self, event_type, listener):
        """
        Unregister an event listener for a specific event type.
        """
        if (event_type, listener) in self.event_listeners:
            self.event_listeners.remove((event_type, listener))
        else:
            print(f"Listener for event type {event_type} not found.")

    def receive_event(self, event):
        """
        Simulates receiving an event.
        """
        event_type = type(event).__name__
        for listener_event_type, listener in self.event_listeners:
            if listener_event_type.__name__ == event_type:
                listener(event)

# # Example usage
# def event_listener(event):
#     print(f"Received event: {event}")

# custom_object = CustomObjects(name="Custom Object", id="1", description="A custom object")
# custom_object.register_event_listener("TestEvent", event_listener)

# # Simulate receiving a test event
# class TestEvent:
#     pass

# test_event = TestEvent()
# custom_object.receive_event(test_event)

# # Unregister the event listener
# custom_object.unregister_event_listener("TestEvent", event_listener)
