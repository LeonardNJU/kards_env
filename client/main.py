# main file for starting the client application
from client.src.states.pregame import PregameState
from utils.constant import SCREEN_HEIGHT, SCREEN_WIDTH
from utils.state_machine import StateMachine

import pygame
import time

# 初始化 pygame
pygame.init()

# 设置显示窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KARDS Env")

gMachine = StateMachine(
    {"PREGAME": PregameState, "RESCHEDULE": None, "GAME": None, "DONE": None}, "PREGAME"
)

def main():
    running = True
    while running:
        start_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gMachine.update(event)
        gMachine.render(screen)
        pygame.display.flip()
        elapsed_time = time.time() - start_time
        if elapsed_time < 1 / 60:  # Maintain 60 FPS
            time.sleep(1 / 60 - elapsed_time)

    pygame.quit()

if __name__ == "__main__":
    main()
