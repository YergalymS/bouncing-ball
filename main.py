import pygame
import sys
import random

pygame.init()

pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
BALL_RADIUS = 10
INITIAL_SQUARE_SIZE = WIDTH - 100
DECREASE_RATE = 3
VELOCITY = [20, 20]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball")

bounce_sound = pygame.mixer.Sound('instrumental.wav')

ball_pos = [WIDTH // 2, HEIGHT // 2]
square_size = INITIAL_SQUARE_SIZE
bounce_count = 0

tail_length = 12  # Number of tail segments
tail_positions = []

# Initial colors for the ball and square
random_color = [random.randint(128, 255) for _ in range(3)]

bounce_sound.play()

def random_velocity_change(velocity):
    change = random.uniform(-1, 1)
    return velocity + change

def smooth_color_change(color, step=1):
    return [(c + random.randint(-step, step)) % 128 + 128 for c in color]

def fade_color(color, factor):
    return [int(c * factor) for c in color]

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
        # bounce_sound.play()

    if ball_pos[1] - BALL_RADIUS <= top_bound or ball_pos[1] + BALL_RADIUS >= bottom_bound:
        VELOCITY[1] = -VELOCITY[1]
        VELOCITY[1] = random_velocity_change(VELOCITY[1])
        ball_pos[1] += VELOCITY[1]
        bounce_count += 1
        square_size -= DECREASE_RATE
        # bounce_sound.play()

    if square_size <= BALL_RADIUS * 2:
        square_size = BALL_RADIUS * 2

    # Update colors smoothly
    random_color = smooth_color_change(random_color, step=2)

    # Update tail positions
    tail_positions.append(list(ball_pos))
    if len(tail_positions) > tail_length:
        tail_positions.pop(0)


    screen.fill(BLACK)


    # Draw the square and the ball with updated colors
    pygame.draw.rect(screen, random_color, [left_bound, top_bound, square_size, square_size], 5)

    for i, pos in enumerate(tail_positions):
        fade_factor = (i + 1) / tail_length  # Fade factor based on position in the tail
        faded_color = fade_color(random_color, fade_factor)
        pygame.draw.circle(screen, faded_color, pos, BALL_RADIUS, 2)



    # pygame.draw.circle(screen, random_color, ball_pos, BALL_RADIUS)
    # pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS, 2)

    # Display bounce count
    font = pygame.font.Font(None, 74)
    text = font.render(f"Bounces: {bounce_count}", True, random_color)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(60)
