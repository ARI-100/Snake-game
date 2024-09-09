import random
import colorsys
import pygame

# Initialize Pygame
pygame.init()
# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

# Define color schemes
color_schemes = {
    "Default": {
        "BACKGROUND": hex_to_rgb('#2C3E50'),  # Dark blue-gray
        "SNAKE_COLOR": hex_to_rgb('#2ECC71'),  # Emerald green
        "FOOD_COLOR": hex_to_rgb('#E74C3C'),  # Soft red
        "TEXT_COLOR": hex_to_rgb('#ECF0F1'),  # Off-white
        "SCORE_COLOR": hex_to_rgb('#3498DB')  # Bright blue
    },
    "Ocean Breeze": {
        "BACKGROUND": hex_to_rgb('#1ABC9C'),  # Turquoise
        "SNAKE_COLOR": hex_to_rgb('#9B59B6'),  # Amethyst
        "FOOD_COLOR": hex_to_rgb('#E67E22'),  # Carrot
        "TEXT_COLOR": hex_to_rgb('#F1C40F'),  # Sunflower
        "SCORE_COLOR": hex_to_rgb('#E74C3C')  # Soft red
    },
    "Night Mode": {
        "BACKGROUND": hex_to_rgb('#000000'),  # Black
        "SNAKE_COLOR": hex_to_rgb('#1ABC9C'),  # Turquoise
        "FOOD_COLOR": hex_to_rgb('#F39C12'),  # Orange
        "TEXT_COLOR": hex_to_rgb('#ECF0F1'),  # Off-white
        "SCORE_COLOR": hex_to_rgb('#3498DB')  # Bright blue
    }
}

# Set default color scheme
current_scheme = color_schemes["Default"]

# Generate a gradient for the snake
def generate_gradient(start_color, end_color, steps):
    start_hsv = colorsys.rgb_to_hsv(*[x/255 for x in start_color])
    end_hsv = colorsys.rgb_to_hsv(*[x/255 for x in end_color])
    gradient = []
    for i in range(steps):
        ratio = i / (steps - 1)
        h = start_hsv[0] + (end_hsv[0] - start_hsv[0]) * ratio
        s = start_hsv[1] + (end_hsv[1] - start_hsv[1]) * ratio
        v = start_hsv[2] + (end_hsv[2] - start_hsv[2]) * ratio
        rgb = colorsys.hsv_to_rgb(h, s, v)
        gradient.append(tuple(int(x * 255) for x in rgb))
    return gradient

SNAKE_GRADIENT = generate_gradient(current_scheme["SNAKE_COLOR"], hex_to_rgb('#27AE60'), 10)

# Snake properties
snake_block = 20
snake_speed = 5  # Changed from 15 back to 5

# Initialize clock
clock = pygame.time.Clock()

# Font for score display
font = pygame.font.SysFont('arial', 35)

def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        color = SNAKE_GRADIENT[i % len(SNAKE_GRADIENT)]
        pygame.draw.rect(window, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_offset=None):
    mesg = font.render(msg, True, color)
    if y_offset is None:
        y_offset = height / 3
    window.blit(mesg, [width / 6, y_offset])

def show_score_and_speed(score, speed, top_score):
    # Score display
    score_surface = font.render(f'Score: {score}', True, current_scheme["SCORE_COLOR"])
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    window.blit(score_surface, score_rect)

    # Speed display
    speed_text = "Slow" if speed == 5 else "Medium" if speed == 10 else "Fast"
    speed_surface = font.render(f'Speed: {speed_text}', True, current_scheme["SCORE_COLOR"])
    speed_rect = speed_surface.get_rect()
    speed_rect.topright = (width - 10, 10)
    window.blit(speed_surface, speed_rect)

    # Top score display
    top_score_surface = font.render(f'Top Score: {top_score}', True, current_scheme["SCORE_COLOR"])
    top_score_rect = top_score_surface.get_rect()
    top_score_rect.topright = (width - 10, 50)  # Adjusted position
    window.blit(top_score_surface, top_score_rect)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def speed_selection():
    speed_options = [("Slow", 5), ("Medium", 10), ("Fast", 15)]
    selected = 1  # Default to Medium
    
    while True:
        window.fill(current_scheme["BACKGROUND"])
        
        title = font.render('Select Snake Speed', True, current_scheme["TEXT_COLOR"])
        title_rect = title.get_rect(center=(width//2, height//4))
        window.blit(title, title_rect)
        
        for i, (text, _) in enumerate(speed_options):
            color = current_scheme["SNAKE_COLOR"] if i == selected else current_scheme["TEXT_COLOR"]
            option = font.render(text, True, color)
            option_rect = option.get_rect(center=(width//2, height//2 + i * 50))
            window.blit(option, option_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(speed_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(speed_options)
                elif event.key == pygame.K_RETURN:
                    return speed_options[selected][1]

def color_selection():
    global current_scheme, SNAKE_GRADIENT
    color_options = list(color_schemes.keys())
    selected = 0  # Default to the first color scheme
    
    while True:
        window.fill(current_scheme["BACKGROUND"])
        
        title = font.render('Select Color Scheme', True, current_scheme["TEXT_COLOR"])
        title_rect = title.get_rect(center=(width//2, height//4))
        window.blit(title, title_rect)
        
        for i, scheme in enumerate(color_options):
            color = current_scheme["SNAKE_COLOR"] if i == selected else current_scheme["TEXT_COLOR"]
            option = font.render(scheme, True, color)
            option_rect = option.get_rect(center=(width//2, height//2 + i * 50))
            window.blit(option, option_rect)
            
            # Draw color preview for the selected scheme
            if i == selected:
                preview_rect = pygame.Rect(width//2 + 150, height//2 - 100, 200, 50)
                pygame.draw.rect(window, color_schemes[scheme]["BACKGROUND"], preview_rect)
                pygame.draw.rect(window, color_schemes[scheme]["SNAKE_COLOR"], [preview_rect.x + 10, preview_rect.y + 10, 30, 30])
                pygame.draw.rect(window, color_schemes[scheme]["FOOD_COLOR"], [preview_rect.x + 60, preview_rect.y + 10, 30, 30])
                pygame.draw.rect(window, color_schemes[scheme]["TEXT_COLOR"], [preview_rect.x + 110, preview_rect.y + 10, 30, 30])
                pygame.draw.rect(window, color_schemes[scheme]["SCORE_COLOR"], [preview_rect.x + 160, preview_rect.y + 10, 30, 30])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(color_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(color_options)
                elif event.key == pygame.K_RETURN:
                    current_scheme = color_schemes[color_options[selected]]
                    SNAKE_GRADIENT = generate_gradient(current_scheme["SNAKE_COLOR"], hex_to_rgb('#27AE60'), 10)
                    return

def save_top_score(top_score):
    with open("top_score.txt", "w") as file:
        file.write(str(top_score))

def load_top_score():
    try:
        with open("top_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False

        # Draw the pause message at the bottom
        message("Game Paused. Press Space to Resume", current_scheme["TEXT_COLOR"], y_offset=height - 50)
        pygame.display.update()
        clock.tick(5)

def gameLoop(snake_speed, top_score):
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(40, height - snake_block) / 20.0) * 20.0

    score = 0

    while not game_over:
        while game_close:
            window.fill(current_scheme["BACKGROUND"])
            message("Game Over! Press Q-Quit or C-Play Again", current_scheme["TEXT_COLOR"])
            show_score_and_speed(score, snake_speed, top_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        return True, top_score  # Signal to restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    pause_game()

        # Check if snake hits the boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        window.fill(current_scheme["BACKGROUND"])
        pygame.draw.rect(window, current_scheme["FOOD_COLOR"], [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score_and_speed(score, snake_speed, top_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(40, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 10

        # Update top score if current score is higher
        if score > top_score:
            top_score = score

        clock.tick(snake_speed)

    # Save the top score when the game ends
    save_top_score(top_score)

    return False, top_score  # Signal to quit the game

def main():
    top_score = load_top_score()  # Load the top score at the start
    while True:
        color_selection()  # Add color selection menu
        selected_speed = speed_selection()
        restart, top_score = gameLoop(selected_speed, top_score)
        if not restart:
            break

    pygame.quit()
    quit()

# Replace gameLoop() call with main()
main()
