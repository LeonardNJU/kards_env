import copy
from action.action import ActionType, Action
from event.event_manager import EventManager
from game.field import Field
from object import unit
from player.player import Player
from utils.constant import FIELD_WIDTH, FIRST_PLAYER_CARDS, SECOND_PLAYER_CARDS
from event.event import Event, EventType
from utils.symbols import UnitType
from utils.unit_registry import unit_registry

from utils.logger import setup_logger
from ui.utils import show_banner
from game.utils import get_opponent_player_id
from ui.field_render import field_render

logger = setup_logger(__name__)


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.players = [player1, player2]
        self.field = Field()
        self.current_turn = 0
        self.current_player_id = 0
        self.event_manager = EventManager()

    def start(self):
        # Show the players' names and put HQ on board
        logger.info(
            f"Starting game between {self.players[0].name} and {self.players[1].name}"
        )
        self.place_HQ()
        self.event_manager.register(EventType.UNIT_DIED, self.delete_obj_on_death)
        self.reschedule_phase()

        self.combat_phase()

    def delete_obj_on_death(self, event: Event):
        """Delete the object from the field when it dies."""
        obj = event.data["object"]
        if isinstance(obj, unit.Unit):
            logger.info(f"Unit {obj.name} has died.")
            self.field.remove(obj)
            owner_id = obj.owner
            self.players[owner_id].obj_on_field.remove(obj)
        else:  # HQ
            logger.info(f"Object {obj.name} has died.")
            owner_id = obj.owner
            self.winning(get_opponent_player_id(owner_id))

    def reschedule_phase(self):
        show_banner("Reschedule phase")
        # Logic for rescheduling phase would go here
        self.players[0].reschedule_phase(FIRST_PLAYER_CARDS)
        self.players[1].reschedule_phase(SECOND_PLAYER_CARDS)

    def combat_phase(self):
        show_banner("Combat phase")
        while True:
            self.start_player_turn()
            self.act_player_turn()
            self.end_player_turn()

    def place_HQ(self):
        """Place HQ for both players on the field."""
        logger.info("Placing HQ on board")
        self.players[0].place_HQ()
        self.players[0].HQ.bind_owner(0)
        self.players[1].place_HQ()
        self.players[1].HQ.bind_owner(1)
        self.field.insert_object(self.players[0].HQ, 0)
        self.field.insert_object(self.players[1].HQ, 2)

    def start_player_turn(self):
        """Start the current player's turn."""
        player = self.players[self.current_player_id]
        show_banner(f"{player.name} turn starts")
        # A new game turn
        if self.current_player_id == 0:
            self.current_turn += 1

        # add kredits slot until the max slot is reached
        player.add_kredits_slot()
        player.refill_kredits()

        # except the first turn, each player draws a card at the start of their turn
        if self.current_turn != 1 or self.current_player_id != 0:
            player.draw_card()

        for u in self.players[self.current_player_id].obj_on_field:
            if isinstance(u, unit.Unit):
                u.start_turn_effects(self.event_manager)

    def act_player_turn(self):
        """Handle the actions of the current player during their turn."""
        action = None
        while not action or action.type != ActionType.END_TURN:
            self.show()
            if action := self.players[self.current_player_id].choose_action():
                try:
                    self.execute_action(action)
                except Exception as e:
                    logger.warning(f"Error executing action: {e}")
                    continue

    def end_player_turn(self):
        """End the current player's turn."""
        show_banner(f"{self.players[self.current_player_id].name} turn ends.")
        for u in self.players[self.current_player_id].obj_on_field:
            if isinstance(u, unit.Unit):
                u.end_turn_effects(self.event_manager)
        self.current_player_id = get_opponent_player_id(self.current_player_id)
        self.show()

    def show(self):
        print("#" * FIELD_WIDTH)
        print(f"Current turn: {self.current_turn}")
        opponent = self.players[get_opponent_player_id(self.current_player_id)]
        us = self.players[self.current_player_id]
        print(
            f"[{opponent.kredits}/{opponent.kredits_slot}] {opponent.name}  -  {opponent.card_manager.get_hand_size()} cards"
        )
        print(field_render(self.field, self.current_player_id))
        print(f"[{us.kredits}/{us.kredits_slot}] {us.name}")
        us.card_manager.show_hand()
        print("#" * FIELD_WIDTH)

    def execute_action(self, action: Action):
        """Executes the given action.
        Will check if the action is valid and then perform it on the game field.

        Args:
            action (Action): The action to be executed.
        """
        match action.type:
            case ActionType.END_TURN:
                pass
            case ActionType.PLAY_CARD:
                self.execute_play_card(action)
            case ActionType.ATTACK:
                self.execute_attack(action)
            case ActionType.MOVE:
                if not self.field.move_unit(
                    action.from_idx,
                    action.to_idx,
                    self.current_player_id,
                    self.players[self.current_player_id].kredits,
                ):
                    # if the move was not successful, log a warning
                    logger.warning(
                        f"Player {self.current_player_id} failed to move unit from {action.from_idx} to {action.to_idx}."
                    )
                else:
                    self.players[
                        self.current_player_id
                    ].kredits -= self.field.get_obj_by_pos(
                        f"f{str(action.to_idx)}", self.current_player_id
                    ).oil
            case ActionType.SURRENDER:
                logger.info(
                    f"Player {self.players[self.current_player_id].name} has surrendered."
                )
                self.winning(get_opponent_player_id(self.current_player_id))
            case _:
                raise ValueError(f"Unknown action type: {action.type}")

    def execute_attack(self, action):
        attacker = self.field.get_obj_by_pos(
            action.attacker_idx, self.current_player_id
        )

        if not attacker or not isinstance(attacker, unit.Unit):
            logger.warning(
                f"Player {self.current_player_id} tried to attack with an invalid unit at position {action.attacker_idx}."
            )
            raise ValueError(f"Invalid attacker at position {action.attacker_idx}.")
        if not attacker.can_attack():
            logger.warning(
                f"Player {self.current_player_id} tried to attack with a unit that cannot attack: {attacker.name}."
            )
            raise ValueError(f"Unit {attacker.name} cannot attack.")
        if attacker.oil > self.players[self.current_player_id].kredits:
            logger.warning(
                f"Player {self.current_player_id} tried to attack with a unit that has insufficient kredits: {attacker.name}."
            )
            raise ValueError(
                f"Unit {attacker.name} has insufficient kredits to attack."
            )
            # distance check
        if (
            action.attacker_idx[0] + action.defender_idx[0]
            not in [
                "sf",
                "fe",
            ]
            and attacker.type != UnitType.ARTILLERY
        ):
            logger.warning(f"Unit {attacker.name} has insufficient range to attack.")
            raise ValueError(f"Unit {attacker.name} has insufficient range to attack.")
        defender = self.field.get_obj_by_pos(
            action.defender_idx, self.current_player_id
        )

        # can attack
        attacker.attack(defender, self.event_manager)
        self.players[self.current_player_id].kredits -= attacker.oil
        attacker.attacked()

    def execute_play_card(self, action: Action):
        player = self.players[self.current_player_id]

        # checkers
        if player.kredits < action.card.kredits:
            logger.warning(
                f"Player {player.name} tried to play a card with insufficient kredits: {action.card.name}"
            )
            raise ValueError("Not enough kredits to play this card.")

        self.play_card(action)
        self.event_manager.dispatch(
            Event(
                EventType.CARD_PLAYED,
                {"owner_id": self.current_player_id, "card": action.card},
            )
        )
        player.kredits -= action.card.kredits
        player.card_manager.use_hand_card(action.card)

    def play_card(self, action: Action):
        for ef in action.card.effects:
            match ef["action"]:
                case "deploy":
                    unit = unit_registry.get_unit_by_name(ef["unit"])
                    # copy
                    unit = copy.deepcopy(unit)
                    if "deploy_position" not in action.card_args or not isinstance(
                        action.card_args["deploy_position"], int
                    ):
                        logger.error(
                            f"Invalid deploy position: {action.card_args['deploy_position']}"
                        )
                        raise ValueError(
                            f"Invalid deploy position: {action.card_args['deploy_position']}"
                        )
                    self.field.insert_object(
                        unit,
                        Field.player_id_to_row(self.current_player_id),
                        action.card_args["deploy_position"],
                    )
                    unit.bind_owner(self.current_player_id)
                    self.players[self.current_player_id].obj_on_field.append(unit)
                    if unit.abilities:
                        for ability in unit.abilities:
                            if "trigger" in ability:
                                match ability["trigger"]:
                                    case "on_damaged":
                                        self.event_manager.register(
                                            EventType.TAKE_DAMAGE,
                                            lambda e: (
                                                self.effect2func(ability["effect"])
                                                if e.data["object"] == unit
                                                else None
                                            ),
                                        )
                                    case "on_deployed":
                                        self.event_manager.register(
                                            EventType.UNIT_DEPLOYED,
                                            lambda e: (
                                                self.effect2func(ability["effect"])
                                                if e.data["object"] == unit
                                                else None
                                            ),
                                        )
                                    case _:
                                        logger.error(
                                            f"Unknown ability trigger: {ability['trigger']}"
                                        )

    def effect2func(self, effect: dict):
        """Convert an effect dictionary to a function."""
        match effect["action"]:
            case "draw_card":
                if effect["target"] == "self":
                    return self.players[self.current_player_id].draw_card(
                        effect["count"]
                    )
            case _:
                raise ValueError(f"Unknown effect action: {effect['action']}")

    def winning(self, winner_id: int):
        """Declare the winner of the game."""
        logger.info(f"Player {self.players[winner_id].name} wins!")
        exit(0)
