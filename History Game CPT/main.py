import pygame
import random
from constants import *

# Initialize Pygame
pygame.init()

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Patriation of the Constitution")

# Load background image
background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load player and enemy images
player_image = pygame.image.load("images/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (150, 300))  # Adjust size if needed

enemy_image = pygame.image.load("images/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (150, 300))  # Adjust size if needed

# Font for text
font = pygame.font.Font(None, 36)
action_font = pygame.font.Font(None, 33)
title = pygame.font.SysFont('Comic Sans MS', 50)

story_page = 0
in_story_mode = True
story_part2_trigger = False
in_start_screen = True
in_dialogue_mode = False  # Track whether we're in dialogue mode
player_bouncing = False
enemy_bouncing = False

# Main game loop
running = True
player_turn = True
selected_attack = None
in_battle = False
damage = 0
player_delay = 0
enemy_delay = 0
enemy_thinking = False
thinking_timer = 0
action_text = "What will you do?"
current_dialogue = ""
current_level = 1

# Character Class
class Character:
    def __init__(self, name, health, attacks, x, y, image):
        self.name = name
        self.health = health
        self.max_health = health
        self.attacks = attacks
        self.x = x
        self.y = y
        self.image = image

    def take_turn(self, opponent, attack):
        min_damage, max_damage = self.attacks[attack]
        damage = random.randint(min_damage, max_damage)
        if player_turn:
            ask_question()
            if ask_question is None:
                opponent.health -= damage
            elif ask_question:
                opponent.health -= damage + 20
            else:
                opponent.health -= damage / 2
        if not player_turn:
            opponent.health -= damage
        if opponent.health < 0:
            opponent.health = 0
        return damage

# Load cloud assets
cloud_1 = pygame.image.load("images/clouds.png").convert_alpha()
cloud_1 = pygame.transform.scale(cloud_1, (150, 150))  # Adjust size if needed

# Cloud positions and speeds
clouds = [
    {"image": cloud_1, "x": 100, "y": -23, "speed": 0.1},
    {"image": cloud_1, "x": 300, "y": -50, "speed": 0.12},
    {"image": cloud_1, "x": 500, "y": -10, "speed": 0.13},
    {"image": cloud_1, "x": 700, "y": 1, "speed": 0.11},
]

def draw_and_move_clouds():
    """Draw and move clouds across the screen."""
    for cloud in clouds:
        screen.blit(cloud["image"], (cloud["x"], cloud["y"]))
        cloud["x"] -= cloud["speed"]  # Move clouds to the left
        if cloud["x"] < -cloud["image"].get_width():  # Reset cloud to the right
            cloud["x"] = screen.get_width()


# Create Player and Enemy
player_attacks = {
    "Debate": (10, 12),
    "Bargain": (14, 18),
    "Unity": (10, 30),
    "Inspire": (12, 19)
}
enemy_attacks = {
    "Reject": (10, 14),
    "Delay": (14, 18),
    "Resist": (19, 26)
}

player = Character("Leader of Canada", 250, player_attacks, 100, 300, player_image)
enemy = Character("Opposition Leader", 100, enemy_attacks, 525, 75, enemy_image)

# Storytelling Section
def draw_story(text_lines, current_page):
    screen.fill(BLACK)  # Black background for storytelling
    y_offset = 150  # Starting Y position for text
    max_width = SCREEN_WIDTH - 100  # Allow some padding on the sides

    for line in text_lines[current_page]:
        words = line.split()  # Split the line into words
        current_line = ""  # Temporary line to build word by word

        for word in words:
            test_line = current_line + word + " "
            # Render the test line to see its width
            test_surface = font.render(test_line, True, TEXT_COLOR)
            if test_surface.get_width() > max_width:
                # If the line is too wide, draw the current line and start a new one
                story_text = font.render(current_line, True, TEXT_COLOR)
                text_rect = story_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(story_text, text_rect)
                y_offset += 40  # Move down for the next line
                current_line = word + " "  # Start a new line with the current word
            else:
                current_line = test_line  # Add the word to the current line

        # Draw the last line (after exiting the loop)
        story_text = font.render(current_line, True, TEXT_COLOR)
        text_rect = story_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(story_text, text_rect)
        y_offset += 40  # Move down for the next line

    continue_text = font.render("Press space to continue", True, TEXT_COLOR)
    continue_rect = continue_text.get_rect(centerx=SCREEN_WIDTH // 2, y=500)
    screen.blit(continue_text, continue_rect)

# Storytelling pages
story_pages = [
    [
        "It is the year 1982. Canada is at a historic crossroads.",
        "The Constitution, still tied to Britain, must finally become fully Canadian.",
        "However, Quebec refuses to sign the agreement, highlighting deep tensions in French-English relations.",
        "You play as a English speaking protestor, tasked with uniting the provinces and bringing the Constitution home."
    ],
    [
        "Quebec's demands for recognition as a distinct society have been dismissed by other provinces.",
        "The infamous 'Kitchen Accord' excluded Quebec leaders from the key negotiations.",
        "Now, you must navigate a divided nation. Will Canada emerge united, or will the fractures deepen?",
        "As leader, your decisions will shape the future of a nation struggling to define its identity."
    ],
    [
        "The road ahead is fraught with challenges. Opposition rises from multiple provinces.",
        "Your choices matter: Debate, Bargain, Inspire, or Unity.",
        "Prepare yourself for the final push to patriate the Constitution and forge a united Canada."
    ]
]

# Add a new storytelling stage for Part 2
story_part2 = [
    [
        "You have secured the support of some provinces, but the hardest battles remain.",
        "Quebec's demands for recognition and autonomy grow louder.",
        "The future of the nation hangs in the balance as provincial leaders present new challenges.",
        "It is up to you to bridge the divide and bring all provinces into agreement."
    ],
    [
        "Opposition leaders rally against your efforts, questioning the very idea of unity.",
        "You must rely on negotiation, compromise, and inspiration to win their trust.",
        "Will Canada achieve independence with dignity and unity, or will the dream falter?",
        "The decisions you make will determine the fate of the country."
    ]
]

# Dialogue triggers based on enemy HP
dialogues_triggered = [False, False, False, False]  # Track triggered states
enemy1_dialogues = {
    80: "French Canadian: 'You have always seen us as just another province, but we are a nation within Canada. How can we trust a system that disregards our language, culture, and identity?'",
    50: "French Canadian: 'The Kitchen Accord was not just a political maneuver; it was a betrayal. While Quebec was excluded, decisions were made that affect our future. Is this how you expect us to feel included in Canada?'",
    30: "French Canadian: 'Quebec’s unique culture and French language are constantly under threat in this federation. The Constitution offers rights to individuals, but where are the protections for our collective identity?'",
    10: "French Canadian: 'If Canada cannot recognize Quebec as a distinct society, then perhaps we need to chart our own course. Unity must be built on mutual respect, not domination.'"
}

enemy2_dialogues = {
    200: "René Lévesque: 'Quebec is not like the other provinces. We are a founding people with our own language, culture, and way of life. Federalism must acknowledge and respect these differences if Canada is to survive.'",
    140: "René Lévesque: 'The Constitution must reflect the reality of Canada: a country with two founding peoples, French and English. Yet, we were excluded from the process, and our demands for recognition as a distinct society were ignored.'",
    60: "René Lévesque: 'Forcing Quebec to accept a Constitution that does not address our identity is not unity—it is assimilation. Our language and culture are not negotiable, and we will continue to fight for our rights.'",
    30: "René Lévesque: 'Quebec’s refusal to sign the Constitution is a message to Canada: we cannot be ignored. The balance of power must change, and our place within this federation must be respected if we are to remain part of Canada.'"
}

# Questions with multiple-choice options
questions = [
    {
        "question": "In what year was the Constitution patriated?",
        "options": ["A: 1980", "B: 1982", "C: 1984"],
        "answer": "B"
    },
    {
        "question": "Who was the Prime Minister during the patriation of the Constitution?",
        "options": ["A: Pierre Trudeau", "B: Brian Mulroney", "C: Jean Chrétien"],
        "answer": "A"
    },
    {
        "question": "What part of the Constitution guarantees civil rights?",
        "options": ["A: Charter of Rights and Freedoms", "B: Bill of Rights", "C: Declaration of Independence"],
        "answer": "A"
    },
    {
        "question": "Which province did not sign the Constitution Act of 1982?",
        "options": ["A: Ontario", "B: Alberta", "C: Quebec"],
        "answer": "C"
    },
    {
        "question": "Which Canadian leader opposed the Constitution Act, claiming it ignored Quebec's identity?",
        "options": ["A: René Lévesque", "B: Pierre Trudeau", "C: Lester B. Pearson"],
        "answer": "A"
    },
    {
        "question": "What event in 1980 emphasized the need for a stronger national structure in Canada?",
        "options": ["A: Meech Lake Accord", "B: Charlottetown Accord", "C: Quebec Referendum"],
        "answer": "C"
    },
    {
        "question": "Which document was added to Canada's Constitution during patriation?",
        "options": ["A: Charter of Rights and Freedoms", "B: Proclamation of Independence", "C: Bill of Rights"],
        "answer": "A"
    },
    {
        "question": "Who was the monarch present during the patriation ceremony in 1982?",
        "options": ["A: Queen Victoria", "B: Queen Elizabeth II", "C: King George VI"],
        "answer": "B"
    },
    {
        "question": "What was René Lévesque's role during the patriation process?",
        "options": ["A: Prime Minister of Canada", "B: Premier of Quebec", "C: Governor General"],
        "answer": "B"
    },
    {
        "question": "What was a major reason Quebec opposed the Constitution Act of 1982?",
        "options": ["A: Lack of economic benefits", "B: Exclusion from negotiations",
                    "C: Disagreement over foreign policy"],
        "answer": "B"
    },
    {
        "question": "Which country did Canada gain full independence from with the Constitution Act of 1982?",
        "options": ["A: France", "B: United States", "C: United Kingdom"],
        "answer": "C"
    },
    {
        "question": "What is one lasting impact of the Constitution Act of 1982 on Canada?",
        "options": ["A: Strengthened colonial ties", "B: Guarantee of individual rights",
                    "C: Reduced federal powers"],
        "answer": "B"
    },
    {
        "question": "What did René Lévesque believe the Constitution Act failed to protect?",
        "options": ["A: Economic equality", "B: Quebec's cultural rights", "C: Environmental policies"],
        "answer": "B"
    },
    {
        "question": "Why did Quebecers feel betrayed during the patriation of the Constitution?",
        "options": [
            "A: They were excluded from negotiations.",
            "B: They disagreed with the Charter of Rights.",
            "C: They wanted more financial autonomy."
        ],
        "answer": "A"
    },
    {
        "question": "What did Quebec demand in constitutional negotiations to protect its cultural identity?",
        "options": [
            "A: Exclusive control over immigration",
            "B: Recognition as a distinct society",
            "C: More representation in the Senate"
        ],
        "answer": "B"
    },
    {
        "question": "What ongoing issue in French-English relations stems from the Constitution Act of 1982?",
        "options": [
            "A: Debate over bilingualism",
            "B: Economic inequality between provinces",
            "C: Quebec's refusal to sign the Constitution"
        ],
        "answer": "C"
    }
]

remaining_questions = questions.copy()

# Function to ask a question and determine if the attack should do more damage
def ask_question():
    global remaining_questions
    # If no questions are left, reset the pool of questions
    if not remaining_questions:
        print("All questions have been asked!")
        return None

    # Select a random question from the remaining pool
    selected = random.choice(remaining_questions)

    # Display the question and options
    print(f"\nTrivia Question: {selected['question']}")
    for option in selected["options"]:
        print(option)

    # Ask for player's answer
    player_answer = input("Your answer (A, B, or C): ").strip().upper()

    # Remove the question from the remaining pool
    remaining_questions.remove(selected)

    # Check if the player's answer is correct
    if player_answer == selected['answer']:
        print("Correct! Your attack does extra damage!")
        return True
    else:
        print(f"Wrong! The correct answer was: {selected['answer']}. Your attack does half the damage.")
        return False


def bounce(character, is_attacking):
    """Handles the bounce effect for a character during an attack."""
    if is_attacking:
        character.y -= 20  # Move up
    else:
        character.y += 20  # Move back down

# Function to display the ending screen credit
def display_ending_credit():
    font = pygame.font.Font(None, 100)  # Use default font, size 100
    text = font.render("You Win!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()
    print("\n--- Ending Credit ---")
    print("After the patriation of the Constitution in 1982, Canada gained full sovereignty from Britain.")
    print("The Charter of Rights and Freedoms, introduced as part of the Constitution Act, ensured greater civil rights for Canadians.")
    print("However, Quebec did not sign the agreement, leading to ongoing debates about its place in the federation.")
    print("The patriation of the Constitution remains a significant milestone in Canadian history, marking a new era of independence and unity.")
    print("\nThank you for playing!")
    print("---------------------")
    pygame.time.wait(20000)  # Pause for 20 seconds before quitting
    pygame.quit()

def draw_dialogue(text):
    """Draws a dialogue box with text that pauses the battle."""
    # Darken the background
    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay.set_alpha(150)  # Adjust transparency (0-255, higher is darker)
    dark_overlay.fill(BLACK)
    screen.blit(dark_overlay, (0, 0))

    # Draw enemy closer to the screen
    scaled_enemy_image = pygame.transform.scale(enemy.image, (300, 600))  # Double the size
    enemy_x = SCREEN_WIDTH // 2 - scaled_enemy_image.get_width() // 2
    enemy_y = SCREEN_HEIGHT // 4 - scaled_enemy_image.get_height() // 4
    screen.blit(scaled_enemy_image, (enemy_x, enemy_y))

    # Dialogue box
    pygame.draw.rect(screen, BLACK, (50, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 100, 250), border_radius=10)
    pygame.draw.rect(screen, WHITE, (55, SCREEN_HEIGHT - 295, SCREEN_WIDTH - 110, 240), border_radius=10)
    words = text.split()
    line = ""
    y_offset = SCREEN_HEIGHT - 280
    for word in words:
        test_line = line + word + " "
        if font.render(test_line, True, BLACK).get_width() > SCREEN_WIDTH - 120:
            rendered_line = font.render(line, True, BLACK)
            screen.blit(rendered_line, (70, y_offset))
            line = word + " "
            y_offset += 30
        else:
            line = test_line
    rendered_line = font.render(line, True, BLACK)
    screen.blit(rendered_line, (70, y_offset))
    continue_text = font.render("Click anywhere to continue...", True, RED)
    screen.blit(continue_text, (70, SCREEN_HEIGHT - 30))

def initialize_level(level):
    """Initialize settings for a specific level."""
    global player, enemy, background, action_text, current_dialogue, dialogues_triggered, in_battle
    if level == 2:
        # Change background for level 2
        background = pygame.image.load("images/background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Update enemy stats and image
        enemy.name = "Provincial Leader"
        enemy.health = 250
        enemy.max_health = 250
        enemy.image = pygame.image.load("images/french.png").convert_alpha()
        enemy.image = pygame.transform.scale(enemy.image, (150, 300))
        enemy.attacks = {
            "Reject": (16, 30),
            "Argue": (21, 32),
            "Delay": (28, 34)
        }

        # Reset dialogue and action text
        current_dialogue = ""
        dialogues_triggered[:] = [False] * len(dialogues_triggered)
        in_battle = True

# Function to handle game over
def game_over():
    screen.fill(BLACK)
    ending_text = font.render("Game Over", True, TEXT_COLOR)
    screen.blit(ending_text, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(5000)  # Pause for 5 seconds before quitting
    pygame.quit()

def draw_hp_bar_with_text(character, pos):
    """Draws an HP bar and displays the current HP/Max HP above it."""
    hp_bar_width = 200
    hp_bar_height = 20
    pygame.draw.rect(screen, RED, (pos[0], pos[1], hp_bar_width, hp_bar_height))

    current_hp_width = int(hp_bar_width * (character.health / character.max_health))
    pygame.draw.rect(screen, GREEN, (pos[0], pos[1], current_hp_width, hp_bar_height))

    hp_text = font.render(f'HP: {character.health}/{character.max_health}', True, TEXT_COLOR)
    screen.blit(hp_text, (pos[0], pos[1] - 25))


# Button drawing function
def draw_button(text, x, y, width, height, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    text_rendered = font.render(text, True, TEXT_COLOR)
    screen.blit(text_rendered,
                (x + (width - text_rendered.get_width()) // 2, y + (height - text_rendered.get_height()) // 2))

def handle_start_screen():
    """Handle the start screen and transition to storytelling."""
    start_screen_background = pygame.image.load("images/background2.png").convert()
    start_screen_background = pygame.transform.scale(start_screen_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    global in_start_screen, in_story_mode
    screen.blit(start_screen_background, (0, 0))
    start_text = font.render("Click anywhere to start", True, TEXT_COLOR)
    screen.blit(start_text,(SCREEN_WIDTH//3, SCREEN_HEIGHT//2))
    start_text = title.render("History Game CPT", True, TEXT_COLOR)
    screen.blit(start_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            in_start_screen = False
            in_story_mode = True

while running:
    if in_start_screen:
       handle_start_screen()

    elif in_story_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                story_page += 1
                if story_page >= len(story_pages):  # End of story
                    in_story_mode = False
                    in_battle = True  # Start the battle
            if story_page < len(story_pages):  # Safeguard
                screen.fill(WHITE)
                draw_story(story_pages, story_page)
                pygame.display.flip()
    elif story_part2_trigger:
        story_page += 1
        if story_page >= len(story_part2):
            running = False



    elif in_dialogue_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Exit dialogue mode and return to battle
                in_dialogue_mode = False
                in_battle = True  # Resume battle
    elif in_battle:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if player_turn:
                    if 470 <= mouse_pos[0] <= 620:
                        if 475 <= mouse_pos[1] <= 525:
                            selected_attack = "Debate"
                        elif 530 <= mouse_pos[1] <= 580:
                            selected_attack = "Inspire"
                    elif 625 <= mouse_pos[0] <= 775:
                        if 475 <= mouse_pos[1] <= 525:
                            selected_attack = "Bargain"
                        elif 530 <= mouse_pos[1] <= 580:
                            selected_attack = "Unity"

        if not in_dialogue_mode:
            # Trigger dialogues
            if current_level == 1:
                for threshold, dialogue in enemy1_dialogues.items():
                    if enemy.health <= threshold and not dialogues_triggered[
                        list(enemy1_dialogues.keys()).index(threshold)]:
                        current_dialogue = dialogue
                        in_dialogue_mode = True
                        dialogues_triggered[list(enemy1_dialogues.keys()).index(threshold)] = True
                        break
            elif current_level == 2:
                for threshold, dialogue in enemy2_dialogues.items():
                    if enemy.health <= threshold and not dialogues_triggered[
                        list(enemy2_dialogues.keys()).index(threshold)]:
                        current_dialogue = dialogue
                        in_dialogue_mode = True
                        dialogues_triggered[list(enemy2_dialogues.keys()).index(threshold)] = True
                        break

        screen.blit(background, (0, 0))
        draw_and_move_clouds()
        screen.blit(player.image, (player.x, player.y))
        screen.blit(enemy.image, (enemy.x, enemy.y))
        draw_hp_bar_with_text(player, (80, 280))
        draw_hp_bar_with_text(enemy, (500, 60))

        # Draw buttons
        if in_dialogue_mode:
            draw_dialogue(current_dialogue)
        else:
            mouse_pos = pygame.mouse.get_pos()
            draw_button("Debate", 470, 475, 150, 50, hover=470 <= mouse_pos[0] <= 620 and 475 <= mouse_pos[1] <= 525)
            draw_button("Bargain", 625, 475, 150, 50, hover=625 <= mouse_pos[0] <= 775 and 475 <= mouse_pos[1] <= 525)
            draw_button("Inspire", 470, 530, 150, 50, hover=470 <= mouse_pos[0] <= 620 and 530 <= mouse_pos[1] <= 580)
            draw_button("Unity", 625, 530, 150, 50, hover=625 <= mouse_pos[0] <= 775 and 530 <= mouse_pos[1] <= 580)
            # Player attacks
            if player_turn and selected_attack:
                player_bouncing = True
                bounce(player, is_attacking=True)
                damage = player.take_turn(enemy, selected_attack)
                if ask_question is None:
                    action_text = f"You used {selected_attack} for {damage} damage!"
                elif ask_question:
                    action_text = f"You used {selected_attack} for {damage + 20} damage!"
                else:
                    action_text = f"You used {selected_attack} for {damage / 2} damage!"
                pygame.time.set_timer(pygame.USEREVENT, 200)  # 200 ms delay
                player_turn = False
                enemy_thinking = True
                thinking_timer = pygame.time.get_ticks()
                selected_attack = None

            # Enemy attacks
            elif not player_turn and enemy_thinking and pygame.time.get_ticks() - thinking_timer > 6000:
                enemy_thinking = False
                enemy_attack = random.choice(list(enemy.attacks.keys()))
                enemy_bouncing = True
                bounce(enemy, is_attacking=True)
                damage = enemy.take_turn(player, enemy_attack)
                action_text = f"Enemy used {enemy_attack} for {damage} damage!"
                pygame.time.set_timer(pygame.USEREVENT, 200)  # 200 ms delay
                player_turn = True

            # Handle bounce reset
            if event.type == pygame.USEREVENT:
                if player_bouncing:
                    bounce(player, is_attacking=False)  # Reset player bounce
                    player_bouncing = False
                if enemy_bouncing:
                    bounce(enemy, is_attacking=False)  # Reset enemy bounce
                    enemy_bouncing = False
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

            # Draw text box
            pygame.draw.rect(screen, TEXT_BG_COLOR, pygame.Rect(65, 475 , 400, 105), border_radius=10)
            action_text_rendered = action_font.render(action_text, True, TEXT_COLOR)
            screen.blit(action_text_rendered, (75, 525))

        # Check for win/lose condition
        if player.health <= 0:
            print("You have been defeated!")
            game_over()
            running = False
        if enemy.health <= 0:
            if current_level == 1:
                print("You have successfully took a step forward to uniting the Quebecers with the rest of Canada!")
                current_level += 1
                initialize_level(current_level)
            elif current_level == 2:
                display_ending_credit()  # Display the ending screen credit
                running = False


    pygame.display.flip()


pygame.quit()