import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
BALL_RADIUS = 10
INITIAL_SQUARE_SIZE = WIDTH - 100
DECREASE_RATE = 3
VELOCITY = [25, 25]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

ball_pos = [WIDTH // 2, HEIGHT // 2]
square_size = INITIAL_SQUARE_SIZE
bounce_count = 0

# Initial colors for the ball and square
ball_color = [random.randint(0, 255) for _ in range(3)]
square_color = [random.randint(0, 255) for _ in range(3)]

def random_velocity_change(velocity):
    change = random.uniform(-1, 1)
    return velocity + change

def smooth_color_change(color):
    return [(c + random.randint(-2, 2)) % 256 for c in color]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_pos[0] += VELOCITY[0]
    ball_pos[1] += VELOCITY[1]

    left_bound = (WIDTH - square_size) // 2
    right_bound = (WIDTH + square_size) // 2
    top_bound = (HEIGHT - square_size) // 2
    bottom_bound = (HEIGHT + square_size) // 2

    if ball_pos[0] - BALL_RADIUS <= left_bound or ball_pos[0] + BALL_RADIUS >= right_bound:
        VELOCITY[0] = -VELOCITY[0]
        VELOCITY[0] = random_velocity_change(VELOCITY[0])
        ball_pos[0] += VELOCITY[0]
        bounce_count += 1
        square_size -= DECREASE_RATE

    if ball_pos[1] - BALL_RADIUS <= top_bound or ball_pos[1] + BALL_RADIUS >= bottom_bound:
        VELOCITY[1] = -VELOCITY[1]
        VELOCITY[1] = random_velocity_change(VELOCITY[1])
        ball_pos[1] += VELOCITY[1]
        bounce_count += 1
        square_size -= DECREASE_RATE

    if square_size <= BALL_RADIUS * 2:
        square_size = BALL_RADIUS * 2

    # Update colors smoothly
    ball_color = smooth_color_change(ball_color)
    square_color = smooth_color_change(square_color)

    # Create a trailing effect
    screen.fill(BLACK)
    trail_surface = pygame.Surface((WIDTH, HEIGHT))
    trail_surface.set_alpha(50)  # Adjust the alpha for trail intensity
    trail_surface.fill(BLACK)
    screen.blit(trail_surface, (0, 0))

    # Draw the square and the ball with updated colors
    pygame.draw.rect(screen, square_color, [left_bound, top_bound, square_size, square_size], 2)
    pygame.draw.circle(screen, ball_color, ball_pos, BALL_RADIUS)

    # Display bounce count
    font = pygame.font.Font(None, 74)
    text = font.render(f"Bounces: {bounce_count}", True, ball_color)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(60)
