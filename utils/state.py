class State:
    def __init__(self):
        pass
    def enter(self, *enter_args):
        """Called when entering the state."""
        pass
    def exit(self):
        """Called when exiting the state."""
        pass
    def update(self, event=None):
        """Called to update the state.
        :param event: Optional event to process during update.
        update only on events.
        """
        pass
    def render(self, screen):
        """Called to render the state."""
        pass
    def on_message(self, message: str):
        """Callback for receiving messages from the server."""
        pass