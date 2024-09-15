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

# Full-screen toggle variable
is_fullscreen = False

# Function to toggle full-screen
def toggle_fullscreen():
    global is_fullscreen, window
    if is_fullscreen:
        window = pygame.display.set_mode((width, height))  # Windowed mode
    else:
        # Get the current screen resolution
        info = pygame.display.Info()
        window = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)  # Full-screen mode
    is_fullscreen = not is_fullscreen

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
    # Center the message horizontally
    msg_rect = mesg.get_rect(center=(width / 2, y_offset))
    window.blit(mesg, msg_rect)

def show_score_and_speed(score, speed, top_score):
    # Set a common height for all displays at the top
    common_height = 0

    # Score display at the left of the screen
    score_surface = font.render(f'Score: {score}', True, current_scheme["SCORE_COLOR"])
    score_rect = score_surface.get_rect(topleft=(10, common_height))  # Position for score at the top left
    window.blit(score_surface, score_rect)

    # Speed display at the center of the screen
    speed_text = "Slow" if speed == 5 else "Medium" if speed == 10 else "Fast"
    speed_surface = font.render(f'Speed: {speed_text}', True, current_scheme["SCORE_COLOR"])
    speed_rect = speed_surface.get_rect(center=(width // 2, common_height + 20))  # Adjusted position for speed
    window.blit(speed_surface, speed_rect)

    # Top score display at the right of the screen
    top_score_surface = font.render(f'Top Score: {top_score}', True, current_scheme["SCORE_COLOR"])
    top_score_rect = top_score_surface.get_rect(topright=(width - 10, common_height))  # Position for top score at the top right
    window.blit(top_score_surface, top_score_rect)

def title_screen():
    while True:
        window.fill(current_scheme["BACKGROUND"])
        
        title = font.render('Snake Game', True, current_scheme["TEXT_COLOR"])
        title_rect = title.get_rect(center=(width//2, height//4))
        window.blit(title, title_rect)
        
        start_text = font.render("Press ENTER to Start", True, current_scheme["SNAKE_COLOR"])
        start_rect = start_text.get_rect(center=(width//2, height//2 + 20))  # Moved closer to controls
        window.blit(start_text, start_rect)
        
        quit_text = font.render("Press F to Toggle Fullscreen", True, current_scheme["SNAKE_COLOR"])
        quit_rect = quit_text.get_rect(center=(width//2, height//2 + 60))  # Moved closer to controls
        window.blit(quit_text, quit_rect)

        # Render controls separately
        arrow_keys_text = font.render("Arrow keys to move the snake", True, current_scheme["SNAKE_COLOR"])
        arrow_keys_rect = arrow_keys_text.get_rect(center=(width//2, height//2 + 100))  # Position for arrow keys
        window.blit(arrow_keys_text, arrow_keys_rect)

        space_text = font.render("Press SPACE to pause the game", True, current_scheme["SNAKE_COLOR"])
        space_rect = space_text.get_rect(center=(width//2, height//2 + 140))  # Position for space
        window.blit(space_text, space_rect)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_f:  # Change from Q to F
                    toggle_fullscreen()  # Call the fullscreen toggle function
                    return True

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
                    return speed_options[selected][1]  # Return the selected speed value

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
            option_rect = option.get_rect(center=(width//2 - 100, height//2 + i * 50))  # Adjusted x-coordinate to move left
            window.blit(option, option_rect)
        
        # Draw the large background square for the color preview
        preview_background_rect = pygame.Rect(width//2 + 100, height//2 - 20, 160, 180)  # Position for the preview
        pygame.draw.rect(window, current_scheme["SCORE_COLOR"], preview_background_rect)  # Use a color for the background

        # Draw color preview for the selected scheme
        if selected < len(color_options):
            scheme = color_options[selected]
            pygame.draw.rect(window, color_schemes[scheme]["BACKGROUND"], preview_background_rect)
            
            # Draw color squares in their own rows
            snake_rect = pygame.Rect(preview_background_rect.x + 10, preview_background_rect.y + 10, 30, 30)
            food_rect = pygame.Rect(preview_background_rect.x + 10, snake_rect.y + 40, 30, 30)
            text_rect = pygame.Rect(preview_background_rect.x + 10, food_rect.y + 40, 30, 30)
            score_rect = pygame.Rect(preview_background_rect.x + 10, text_rect.y + 40, 30, 30)

            pygame.draw.rect(window, color_schemes[scheme]["SNAKE_COLOR"], snake_rect)
            pygame.draw.rect(window, color_schemes[scheme]["FOOD_COLOR"], food_rect)
            pygame.draw.rect(window, color_schemes[scheme]["TEXT_COLOR"], text_rect)
            pygame.draw.rect(window, color_schemes[scheme]["SCORE_COLOR"], score_rect)
            
            # Draw full words in separate rows below the color squares
            small_font = pygame.font.SysFont('arial', 20)  # Smaller font size
            label_s = small_font.render("SNAKE", True, (255, 255, 255))  # White color for visibility
            label_f = small_font.render("FOOD", True, (255, 255, 255))
            label_t = small_font.render("TEXT", True, (255, 255, 255))
            label_sc = small_font.render("SCORE", True, (255, 255, 255))
            
            # Position the labels in separate rows
            window.blit(label_s, (snake_rect.x + 40, snake_rect.y))  # Position next to the square
            window.blit(label_f, (food_rect.x + 40, food_rect.y))
            window.blit(label_t, (text_rect.x + 40, text_rect.y))
            window.blit(label_sc, (score_rect.x + 40, score_rect.y))  # Adjusted to reduce space below the last label
        
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

    # Ensure food does not spawn in the first two rows
    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(2, int((height - snake_block) // 20.0))) * 20.0 + 40.0  # Start from row 2

    score = 0

    while not game_over:
        while game_close:
            window.fill(current_scheme["BACKGROUND"])
            message("Game Over! Press Q-Quit or C-Play Again", current_scheme["TEXT_COLOR"], y_offset=height / 2)  # Centered vertically
            show_score_and_speed(score, snake_speed, top_score)  # Show score on game over screen
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
                elif event.key == pygame.K_f:  # Change from Q to F
                    toggle_fullscreen()  # Call the fullscreen toggle function

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
        show_score_and_speed(score, snake_speed, top_score)  # Show score during the game

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(2, int((height - snake_block) // 20.0))) * 20.0 + 40.0  # Ensure food spawns in valid area
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
        if not title_screen():  # Add title screen
            break
        color_selection()
        selected_speed = speed_selection()
        restart, top_score = gameLoop(selected_speed, top_score)
        if not restart:
            break

    pygame.quit()
    quit()

# Replace gameLoop() call with main()
main()
