import pygame
import sys
import time
import cv2

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agent's Secret Mission")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Font setup
FONT_TITLE = pygame.font.Font("PixelGame.otf", 124)
FONT_CENTER = pygame.font.Font("ethnocentric rg.otf", 30)
FONT_LEFT = pygame.font.Font("ethnocentric rg it.otf", 30)
FONT_RIGHT = pygame.font.Font("ethnocentric rg.otf", 30)

# Story scenes
good_scenes = [
    {
        "id": '1',
        "text": ("You approach the enemy base on a Zodiac boat under the cover of the night. "
                 "Ahead is a submerged access tunnel, "
                 "but you notice a secondary path leading to a drainage pipe along the cliffs."),
        "options": [
            "1. Swim through the access tunnel",
            "2. Climb the cliffs to the drainage pipe",
        ],
        "outcomes": ['2', '11']
    },
    {
        "id": '2',
        "text": ("You reach the grate and use your laser cutter to slip inside undetected, "
                 "but as you approach the entrance, two guards appear doing their nightly routine. "
                 "What do you do?"),
        "options": [
            "1. Hide behind crates and wait for them to pass",
            "2. Attack the guards head-on"
        ],
        "outcomes": ['transmission_cutscene_1', '11']
    },
    {
        "id": '3',
        "text": "Now what should you do...",
        "options": [
            "1. Look for an outfit to change into",
            "2. Sneak through the vents",
            "3. Go through the front entrance"
        ],
        "outcomes": ['4A', '4B', '11']
    },
    {
        "id": '4A',
        "text": "You successfully found an outfit.",
        "options": [
            "1. Go through the front entrance",
            "2. Try to speak to the guards to find the control room"
        ],
        "outcomes": ['5A', '5B']
    },
    {
        "id": '4B',
        "text": "You sneak into the vent and are met with a split decision.",
        "options": [
            "1. Go left",
            "2. Go right"
        ],
        "outcomes": ['11', '5C']
    },
    {
        "id": '5A',
        "text": "You make it in but need to find the control room.",
        "options": [
            "1. Go downstairs",
            "2. Go upstairs"
        ],
        "outcomes": ['5B', '5C']
    },
    {
        "id": '5B',
        "text": "You have made your way into the basement and locate the control room.",
        "options": [
            "1. Pick the lock",
            "2. Break the door down"
        ],
        "outcomes": ['6', '11']  # Possible transition into asteroid game
    },
    {
        "id": '5C',
        "text": "You have found the Commander's office but the door is locked with a biometric system.",
        "options": [
            "1. Hack the system",
            "2. Go back downstairs"
        ],
        "outcomes": ['11', '5A']
    },
    {
        "id": '6',
        "text": ("You make it into the control room and neutralize the technicians using "
                 "the tranquilizer darts you were equipped with. You disable the defensive systems and "
                 "successfully exit."),
        "options": [
            "1. Go through the elevator shaft",
            "2. Create a diversion for the lower-level guards"
        ],
        "outcomes": ['7A', '7B']
    },
    {
        "id": '7A',
        "text": ("You pry open the elevator doors and climb the cables to the top floor. Halfway up, a loose wire sparks, "
                 "almost revealing your position, but you make it to the top undetected. You have located the Commander's office, "
                 "but biometric locks guard it."),
        "options": [
            "1. Send a drone to incapacitate the guards",
            "2. Create a distraction in a nearby hallway to lure the guards away"
        ],
        "outcomes": ['8A', '11']  # Possible transition into asteroid game
    },
    {
        "id": '7B',
        "text": ("You overload a nearby server, causing a small explosion in the lower level. Guards scramble to investigate, "
                 "leaving the top floor and the route to it lightly defended. The commotion buys you time, but increases the overall alert level of the base."),
        "options": [
            "1. Hack the door",
            "2. Create a distraction in a nearby hallway to lure the guards away"
        ],
        "outcomes": ['11', '8B']
    },
]

bad_scenes = [
    {
        "id": '11',
        "text": "Bad ending: You were caught. Better luck next time!",
        "options": [
            "Restart Mission"
        ],
        "outcomes": ['Restart Mission']
    },
    {
        "id": '12',
        "text": "Good ending: Mission accomplished! You successfully retrieved the intel.",
        "options": [],
        "outcomes": []
    }
]
transmission_cutscenes = [
    {
        "id": 'transmission_cutscene_1',
        "text": "Agent, are you there? Ok, good. You must make it into the security room and disable the defensive system. "
                "After that, you will be able to reach the commander's office and retrieve the intel. "
                "Keep in mind that there are enemies all over the base, outfitted to the teeth, "
                "but with your training, they stand no chance. Good luck agent and god speed. "
                "Over and Out." 
    }
    
]

# Combine all scenes into a dictionary for easy lookup
scenes = {scene["id"]: scene for scene in good_scenes + bad_scenes}

# Game state
current_scene = None
ending = None
game_started = False
show_instructions = False
animated_text = ""
text_index = 0
animation_speed = 100
last_update_time = 0
options_fade_in = False
options_alpha = 0
options_fade_speed = 2

# Draw the start screen
def draw_start_screen():
    screen.fill(BLACK)
    title_lines = {"Agent", "Escapade"}
    y_offset = HEIGHT // 4

    for line in title_lines:
        title_surface = FONT_TITLE.render(line, True, GREEN)
        title_rect = title_surface.get_rect(topleft=(20, y_offset))
        screen.blit(title_surface, title_rect)
        y_offset += title_surface.get_height() + 10
    
    # Display the "Start Mission" button
    start_button_text = "Start Mission"
    start_button_color = GREEN if is_mouse_hovering(pygame.Rect(WIDTH - 400, HEIGHT - 150, 180, 400)) else WHITE
    start_button = FONT_LEFT.render(start_button_text, True, start_button_color)
    start_button_rect = start_button.get_rect(bottomright=(WIDTH - 20, HEIGHT - 100))
    screen.blit(start_button, start_button_rect)

    # Display the "Instructions" button
    instruction_button_text = "Instructions"
    instruction_button_color = GREEN if is_mouse_hovering(pygame.Rect(WIDTH - 200, HEIGHT - 100, 180, 40)) else WHITE
    instruction_button = FONT_LEFT.render(instruction_button_text, True, instruction_button_color)
    instruction_button_rect = instruction_button.get_rect(bottomright=(WIDTH - 20, HEIGHT - 50))
    screen.blit(instruction_button, instruction_button_rect)


# Draw the cut scene
def draw_cut_scene(video_capture, current_time):
    global animated_text, text_index, last_update_time
    screen.fill(BLACK)
    
    ret, frame = video_capture.read()
    if not ret:
        # If the video is over, reset the video capture
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video_capture.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Rotate the frame 90 degrees counter-clockwise
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Resize the frame to fit the screen
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_surface = pygame.surfarray.make_surface(frame)
        # Center the frame on the screen
        screen.blit(frame_surface, (0, 0))

    # Draw the cut scene text
    cut_scene_text = "Your mission soldier, should you choose to accept it, is to infiltrate the enemy base, disable their security system, and retrieve the intel. God speed agent."
    if text_index < len(cut_scene_text):
        if current_time - last_update_time > 1000 // animation_speed:
            animated_text += cut_scene_text[text_index]
            text_index += 1
            last_update_time = current_time
    draw_text_wrapped(animated_text, FONT_CENTER, GREEN, 20, HEIGHT // 2 + 50, WIDTH - 40)

    # Draw the next button
    next_button = FONT_LEFT.render("Next", True, GREEN)
    next_button_rect = next_button.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    screen.blit(next_button, next_button_rect)

# Draw transmission cut scene
def draw_transmission_cutscene(cutscene_id, current_time):
    global animated_text, text_index, last_update_time
    screen.fill(BLACK)
    
    transmission_text = transmission_cutscenes[cutscene_id]["text"]
    if text_index < len(transmission_text):
        if current_time - last_update_time > 1000 // animation_speed:
            animated_text += transmission_text[text_index]
            text_index += 1
            last_update_time = current_time
    draw_text_wrapped(animated_text, FONT_CENTER, GREEN, 20, 50, WIDTH - 40)

    # Draw the continue button
    continue_button = FONT_LEFT.render("Continue", True, GREEN)
    continue_button_rect = continue_button.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    screen.blit(continue_button, continue_button_rect)

def is_mouse_hovering(rect):
    return rect.collidepoint(pygame.mouse.get_pos())

# Draw the ending screen
def draw_ending():
    screen.fill(WHITE)
    if ending == "good":
        text = FONT_RIGHT.render("Congratulations! You got the good ending!", True, BLACK)
    else:
        text = FONT_RIGHT.render("You got the bad ending. Better luck next time!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    draw_restart_button()

# Draw the restart button
def draw_restart_button():
    restart_button = FONT_RIGHT.render("Restart Mission", True, BLACK)
    restart_button_rect = restart_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_button, restart_button_rect)

# Draw wrapped text
def draw_text_wrapped(text, font, color, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + i * font.get_height()))

# Draw a regular scene
def draw_scene(scene, current_time):
    global animated_text, text_index, last_update_time, options_fade_in, options_alpha
    screen.fill(BLACK)

    if text_index < len(scene["text"]):
        if current_time - last_update_time > 1000 // animation_speed:
            animated_text += scene["text"][text_index]
            text_index += 1
            last_update_time = current_time
    else:
        options_fade_in = True

    draw_text_wrapped(animated_text, FONT_CENTER, GREEN, 20, 50, WIDTH - 40)

    if options_fade_in:
        options_alpha = min(255, options_alpha + options_fade_speed)
        for i, option in enumerate(scene["options"]):
            option_surface = FONT_LEFT.render(option, True, WHITE)
            option_surface.set_alpha(options_alpha)
            option_rect = option_surface.get_rect(bottomleft=(20, HEIGHT - 100 + i * 50))
            screen.blit(option_surface, option_rect)


# Draw instructions screen
def draw_instructions(current_time):
    global animated_text, text_index, last_update_time
    screen.fill(BLACK)
    instructions_text = "Instructions: You are an agent on a secret mission. Make choices to determine the outcome of the story. Good luck!"
    if text_index < len(instructions_text):
        if current_time - last_update_time > 1000 // animation_speed:
            animated_text += instructions_text[text_index]
            text_index += 1
            last_update_time = current_time
    draw_text_wrapped(animated_text, FONT_CENTER, GREEN, 20, 50, WIDTH - 40)

    # Draw the back button
    back_button = FONT_LEFT.render("Back", True, GREEN)
    back_button_rect = back_button.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    screen.blit(back_button, back_button_rect)

# Reset the game state (for transitioning between scenes)
def reset_game_state():
    global animated_text, text_index, options_fade_in, options_alpha, last_update_time
    animated_text = ""
    text_index = 0
    options_fade_in = False
    options_alpha = 0
    last_update_time = pygame.time.get_ticks()

# Reset the entire game (for restarting)
def reset_game():
    global current_scene, ending, game_started, show_instructions, start_screen
    current_scene = None
    ending = None
    game_started = False
    show_instructions = False
    reset_game_state()

# Main game loop
def main():
    global current_scene, ending, game_started, show_instructions, animated_text, text_index, options_fade_in, options_alpha, last_update_time, option_rect
    video_capture = cv2.VideoCapture("cut_scene.mp4")

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video_capture.release()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Start screen logic
                if not game_started and not show_instructions:
                    
                    # Check if "Start Mission" or "Instructions" is clicked
                    if pygame.Rect(WIDTH - 200, HEIGHT - 150, 180, 40).collidepoint(x, y):
                        game_started = True
                        current_scene = "cut_scene"
                        reset_game_state()
                    elif pygame.Rect(WIDTH - 200, HEIGHT - 100, 180, 40).collidepoint(x, y):
                        show_instructions = True
                        reset_game_state()

                # Instructions logic
                elif show_instructions:
                    back_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
                    if back_button_rect.collidepoint(x, y):
                        show_instructions = False
                        reset_game_state()

                # Ending logic
                elif ending is not None:
                    restart_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
                    if restart_button_rect.collidepoint(x, y):
                        reset_game()

                # Handle cutscenes
                elif current_scene == 'cut_scene':
                    next_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
                    if next_button_rect.collidepoint(x, y):
                        current_scene = '1'  # Start from the first scene
                        reset_game_state()

                elif current_scene == 'transmission_cutscene_1':
                    continue_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
                    if continue_button_rect.collidepoint(x, y):
                        current_scene = '3'  # Transition to Scene 3
                        reset_game_state()

                # Regular scene decision logic
                elif current_scene is not None and current_scene not in ['cut_scene', 'transmission_cutscene_1'] and options_alpha >= 255:
                    scene = scenes.get(current_scene)
                    if scene and scene["options"]:
                        for i in range(len(scene["options"])):
                            option_rect = pygame.Rect(20, HEIGHT - 100 + i * 50 - FONT_LEFT.get_height(), 300, FONT_LEFT.get_height())
                            if option_rect.collidepoint(x, y):
                                outcome = scene["outcomes"][i]

                                if isinstance(outcome, str) and outcome.startswith('transmission_cutscene'):
                                    # Handle transition to cutscenes
                                    current_scene = outcome
                                elif outcome in scenes:
                                    # Handle transition to next scenes or endings
                                    current_scene = outcome
                                elif outcome == 'Restart Mission':
                                    ending = "bad"
                                elif outcome == '12':
                                    ending = "good"
                                else:
                                    # Undefined outcome
                                    print(f"Undefined outcome: {outcome}")
                                
                                reset_game_state()
                

        # Render appropriate screen
        if not game_started and not show_instructions:
            draw_start_screen()
        elif show_instructions:
            draw_instructions(current_time)
        elif current_scene == 'cut_scene':
            draw_cut_scene(video_capture, current_time)
        elif current_scene == 'transmission_cutscene_1':
            draw_transmission_cutscene(current_time)
        elif current_scene in scenes:
            scene = scenes[current_scene]
            draw_scene(scene, current_time)
        elif ending == "good" or ending == '11':
            draw_ending()




        # mouse_pos = pygame.mouse.get_pos()
        # if not game_started and not show_instructions:

        #     start_button_rect = pygame.Rect(WIDTH - 200, HEIGHT - 150, 180, 40)
        #     instruction_button_rect = pygame.Rect(WIDTH - 200, HEIGHT - 100, 180, 40)

        #     start_button_color = WHITE if is_mouse_hovering(start_button_rect) else GREEN
        #     instruction_button_color = WHITE if is_mouse_hovering(instruction_button_rect) else GREEN

        #     start_button = FONT_LEFT.render("Start Mission", True, start_button_color)
        #     instruction_button = FONT_LEFT.render("Instructions", True, instruction_button_color)

        #     screen.blit(start_button, start_button_rect)
        #     screen.blit(instruction_button, instruction_button_rect)

        # elif current_scene in scenes:
        #     scene = scenes[current_scene]
        #     if options_fade_in:
        #         for i, option in enumerate(scene["options"]):
        #             option_rect = pygame.Rect(20, HEIGHT - 100 + i * 50 - FONT_LEFT.get_height(), 300, FONT_LEFT.get_height())
        #             option_color = GREEN if is_mouse_hovering(option_rect) else WHITE
        #             option_surface = FONT_LEFT.render(option, True, option_color)
                    
        #             screen.blit(option_surface, option_rect)


        pygame.display.flip()

if __name__ == "__main__":
    main()
