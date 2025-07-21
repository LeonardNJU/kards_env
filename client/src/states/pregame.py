from utils.constant import FONT_LARGE_SIZE, FONT_MEDIUM_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from comm.client import Client
from utils.state import State
import pygame
import json

# -*- coding: utf-8 -*-

from utils.logger import setup_logger

logger = setup_logger("PregameState")


class PregameState(State):
    """
    Pregame state for the game

    First connect to the server, then wait for self ready
    Will tell server when ready status switches

    Will listen to server for other player's status and msgs

    Change status to reschedule state when server tells ready for both players
    """

    def __init__(self):
        self.conn = Client("localhost", 12345, self.on_message)

        self.self_name = None
        self.self_major = None
        self.self_allies = None
        self.self_ready = False

        self.opponent_name = None
        self.opponent_major = None
        self.opponent_allies = None
        self.opponent_ready = False

        self.title_font = pygame.font.SysFont("Arial", FONT_LARGE_SIZE)
        self.status_font = pygame.font.SysFont("Arial", FONT_MEDIUM_SIZE)

    def update(self, event=None):
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # switch ready status
                    self.conn.send("READY" if not self.self_ready else "NOT_READY")

    def on_message(self, message: str):
        """
        Callback for receiving messages from the server

        message format:
        {
            "state": "PREGAME",
            "self": {
                "name": "Player1",
                "major": "Major1",
                "allies": "Ally1",
                "ready": True,
            }
            "opponent": {
                "name": "Player2",
                "major": "Major2",
                "allies": "Ally2",
                "ready": False
            }
        }
        """
        msg = json.loads(message)
        if msg.get("state") == "SERVER_INIT":
            logger.debug("server connected.")
        elif msg.get("state") == "PREGAME":
            self.self_name = msg["self"]["name"]
            self.self_major = msg["self"]["major"]
            self.self_allies = msg["self"]["allies"]
            self.self_ready = msg["self"]["ready"]

            self.opponent_name = msg["opponent"]["name"]
            self.opponent_major = msg["opponent"]["major"]
            self.opponent_allies = msg["opponent"]["allies"]
            self.opponent_ready = msg["opponent"]["ready"]

            logger.debug(f"Updated state: {msg}")
        elif msg.get("state") == "RESCHEDULE":
            # Change to reschedule state
            from main import gMachine

            gMachine.change_state(
                "RESCHEDULE", self.conn
            )  # TODO: should rebind `on_message` callback in enter func
            logger.debug("Changing to RESCHEDULE state")
            gMachine.on_message(message)  # Pass the message to the new state
        else:
            # Should not happen, but just in case
            logger.error(f"Unknown state in message: {msg.get('state')}")
        logger.debug(f"Received message: {message}")

    def render(self, screen):
        screen.fill((30, 30, 30))  # 背景色

        # 标题字体
        title_surface = self.title_font.render("KARDS Env", True, (255, 255, 255))

        if self.self_name is None or self.opponent_name is None:
            # 有任意一方未上线
            screen.blit(
                title_surface,
                ((SCREEN_WIDTH - title_surface.get_width()) // 2, SCREEN_HEIGHT// 4),
            )

            finding_surface = self.status_font.render(
                "Finding Opponent...", True, (200, 200, 200)
            )
            screen.blit(
                finding_surface,
                ((SCREEN_WIDTH - finding_surface.get_width()) // 2, SCREEN_HEIGHT// 2),
            )
        else:
            # 双方已上线，显示双方信息卡片
            # 上半部分
            screen.blit(
                title_surface,
                ((SCREEN_WIDTH - title_surface.get_width()) // 2, SCREEN_HEIGHT//8 ),
            )

            # 下半部分：双方信息
            info_y = 250
            padding_x = 100

            # 我方信息
            self_info = [
                f"Name: {self.self_name} [{'READY' if self.self_ready else 'NOT READY!'}]",
                f"Major: {self.self_major}",
                f"Allies: {self.self_allies}",
            ]
            for idx, text in enumerate(self_info):
                line_surface = self.status_font.render(text, True, (200, 200, 200))
                screen.blit(line_surface, (padding_x, info_y + idx * 40))

            # 对手信息
            opponent_info = [
                f"Name: {self.opponent_name} [{'READY' if self.opponent_ready else 'NOT READY!'}]",
                f"Major: {self.opponent_major}",
                f"Allies: {self.opponent_allies}",
            ]
            for idx, text in enumerate(opponent_info):
                line_surface = self.status_font.render(text, True, (200, 200, 200))
                screen.blit(
                    line_surface,
                    (
                        SCREEN_WIDTH - padding_x - line_surface.get_width(),
                        SCREEN_HEIGHT - info_y + idx * 40 - 3*40,
                    ),
                )

            # VS 居中
            vs_surface = self.title_font.render("VS", True, (255, 255, 255))
            screen.blit(
                vs_surface,
                ((SCREEN_WIDTH - vs_surface.get_width()) // 2, SCREEN_HEIGHT // 2 - vs_surface.get_height() // 2,
            ))
