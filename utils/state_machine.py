from typing import Dict, Type
from utils.state import State

class StateMachine:
    def __init__(self, map_states:Dict[str, Type[State]], initial_state:str):
        """
        Initializes the state machine with a dictionary of states and an optional initial state.
        """
        self.states = map_states
        self.current_state = map_states[initial_state]()

    def change_state(self, new_state: str, *enter_args):
        """
        Changes the current state to a new state.
        """
        assert new_state in self.states, f"State '{new_state}' doesn't exist in the state machine."
        self.current_state.exit()
        self.current_state = self.states[new_state]()
        self.current_state.enter(*enter_args)

    def update(self, event=None):
        """
        Updates the current state.
        """
        self.current_state.update(event)

    def render(self, screen):
        """
        Renders the current state.
        But only if rendering is needed.
        """
        self.current_state.render(screen)
    def on_message(self, message: str):
        """
        Callback for receiving messages from the server.
        """
        self.current_state.on_message(message)