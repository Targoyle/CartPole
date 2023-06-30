import math
import pygame
from pygame.locals import *

GRAVITY = 9.8  # m/s2

POLE_LENGTH = 1.0  # m
POLE_MASS = 0.1  # kg
CART_MASS = 1.0  # kg
TOTAL_MASS = POLE_MASS + CART_MASS
HALF_POLE_LENGTH = POLE_LENGTH / 2.0
POLE_MOMENT = POLE_MASS * HALF_POLE_LENGTH
CART_FORCE = 2.0

WINDOW_SIZE = (800, 480)
FPS = 60
SCALE = 200
CART_WIDTH = 40  # px

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (31, 119, 180)
ORANGE = (255, 127, 14)

def draw_world(screen, cart, pole_angle):
    screen.fill(WHITE)

    cart_x = WINDOW_SIZE[0] / 2.0 + cart * SCALE
    cart_y = WINDOW_SIZE[1] / 2.0
    pygame.draw.rect(screen, BLUE, pygame.Rect(cart_x -CART_WIDTH // 2, cart_y, CART_WIDTH, 20))

    pole_x = cart_x + HALF_POLE_LENGTH * SCALE * math.sin(pole_angle)
    pole_y = cart_y - HALF_POLE_LENGTH * SCALE * math.cos(pole_angle)
    pygame.draw.line(screen, ORANGE, (cart_x, cart_y), (pole_x, pole_y), 5)

    pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("CartPole")
    pygame.display.set_icon(pygame.Surface((1,1)))

    screen = pygame.display.set_mode(WINDOW_SIZE, flags=pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    cart = 0.0
    cart_velocity = 0.0
    pole_angle = 0.0
    pole_angular_velocity = 0.0
    force = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    force -= CART_FORCE
                elif event.key == K_d:
                    force += CART_FORCE
            elif event.type == KEYUP:
                if event.key == K_a:
                    force += CART_FORCE
                elif event.key == K_d:
                    force -= CART_FORCE

        sin_theta = math.sin(pole_angle)
        cos_theta = math.cos(pole_angle)

        pole_acceleration = (
            GRAVITY * sin_theta - cos_theta * (force + POLE_MASS * HALF_POLE_LENGTH * pole_angular_velocity ** 2 * sin_theta) / TOTAL_MASS
            ) / (HALF_POLE_LENGTH * (4.0/3.0 - POLE_MASS * cos_theta ** 2 / TOTAL_MASS))
        cart_acceleration = (
            force + POLE_MOMENT * (pole_angular_velocity ** 2 * sin_theta - pole_acceleration * cos_theta)) / TOTAL_MASS

        cart_velocity += cart_acceleration / FPS
        cart += cart_velocity / FPS

        pole_angular_velocity += pole_acceleration / FPS
        pole_angle += pole_angular_velocity / FPS

        if (cart * SCALE - CART_WIDTH / 2) < -WINDOW_SIZE[0] / 2.0:
            cart = (-WINDOW_SIZE[0] / 2 + CART_WIDTH / 2) / SCALE
            cart_velocity = -cart_velocity
        elif (cart * SCALE + CART_WIDTH / 2) > WINDOW_SIZE[0] / 2.0:
            cart = (WINDOW_SIZE[0] / 2 - CART_WIDTH / 2) / SCALE
            cart_velocity = -cart_velocity

        draw_world(screen, cart, pole_angle)

        clock.tick(FPS)

if __name__ == "__main__":
    main()
