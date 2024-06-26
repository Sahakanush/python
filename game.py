import pygame
import sys
import random
# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Who Wants to Be a Millionaire")

# Load the background image and resize it to match the window size
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
ORANGE = (255, 165, 0)


# Load questions from file
def load_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            question = parts[0]
            answers = parts[1].split(",")
            correct_answer = answers[0]
            random.shuffle(answers)  # Shuffle answers
            questions.append((question, answers, correct_answer))
    return questions

questions = load_questions('questions.txt')

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Function to create buttons
def create_button(text, font, color, hover_color, x, y, width, height):
    button_surface = pygame.Surface((width, height))
    button_rect = button_surface.get_rect()
    button_rect.topleft = (x, y)

    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_rect.collidepoint(mouse_pos)

    if is_hover:
        pygame.draw.rect(button_surface, hover_color, (0, 0, width, height))
    else:
        pygame.draw.rect(button_surface, color, (0, 0, width, height))

    draw_text(text, font, BLACK, button_surface, 10, 10)

    return button_surface, button_rect

def create_points_button(question_number, scored):
    points_text = f"Points: {points[question_number]} \n Scored point: {scored}"
    points_button, points_button_rect = create_button(points_text, points_font, GRAY, GRAY, 50, 50, 400, 50)
    return points_button, points_button_rect

def start_window():
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        draw_text("Who Wants to Be a Millionaire", pygame.font.Font(None, 48), ORANGE, screen, 200, 100)

        # Create Start button
        start_button, start_button_rect = create_button("Start", pygame.font.Font(None, 36), GRAY, WHITE, 300, 300, 200, 50)
        screen.blit(start_button, start_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False

# Call the start_window function before the main loop
start_window()
pygame.time.wait(500)
# Main loop
running = True
clock = pygame.time.Clock()

# Points dictionary
points = {
    1: "0$",
    2: "100$",
    3: "200$",
    4: "300$",
    5: "500$",
    6: "1000$",
    7: "2000$",
    8: "4000$",
    9: "8000$",
    10: "16000$",
    11: "32000$",
    12: "64000$",
    13: "125000$",
    14: "250000$",
    15: "500000$",
    16: "1000000$"
}

# Initial points
scored = "0$"
current_points = 0

def handle_button_click(clicked_answer, correct_answer):
    global current_points
    if clicked_answer == correct_answer:
        current_points += 100  # Increase points by 100 for correct answer
        print("Correct answer! Next question:", correct_answer)
        return True
    else:
        print("Wrong answer! The correct answer is:", correct_answer)
        return False

def get_random_question():
    if questions:
        return questions.pop(random.randint(0, len(questions) - 1))
    else:
        return None

current_question = get_random_question()

question_counter = 1

# Font for points display
points_font = pygame.font.Font(None, 24)

# Variables for tracking selected answer button
selected_answer_button = None
answer_selected = False
answer_button_clicked = False
help_options = ["50:50", "Friend-call", "Audience"]

# Function to perform the 50:50 lifeline
def fifty_fifty(answers, correct_answer):
    ind1 = answers.index(correct_answer)
    remaining_answers = [correct_answer]
    answers.remove(correct_answer)
    second_option =random.choices(answers)
    ind2 = answers.index(second_option[0])
    remaining_answers.append(second_option[0])
    return remaining_answers, ind1, ind2

# Function to perform the Phone a Friend lifeline

def phone_a_friend(correct_answer):
    result_text = "Your friend says: " + correct_answer
    display_lifeline_result(result_text)

def display_lifeline_result(result_text):
    font = pygame.font.Font(None, 24)
    result_surface = pygame.Surface((400, 150))
    result_surface.fill(WHITE)
    lines = result_text.split('\n')  # Split the result text into lines
    y_offset = 25  # Initial Y offset for the first line
    for line in lines:
        text = font.render(line, True, BLACK)
        result_surface.blit(text, (50, y_offset))
        y_offset += 25  # Increment Y offset for the next line
    screen.blit(result_surface, (200, 250))
    pygame.display.flip()
    pygame.time.wait(5000)

# Function to perform the Phone a Friend lifeline
def phone_a_friend(correct_answer):
    result_text = "Your friend says: " + correct_answer
    display_lifeline_result(result_text)

# Function to perform the Ask the Audience lifeline
def ask_the_audience(answers):
    correct = answers[0]
    correct_percent = random.randint(50, 100)
    wrong_percent1 = random.randint(0, 100-correct_percent)
    wrong_percent2 = random.randint(0, 100-correct_percent-wrong_percent1)
    wrong_percent3 = 100-correct_percent-wrong_percent1-wrong_percent2
    percents = [wrong_percent1, wrong_percent2, wrong_percent3]
    print(percents)
    result_text = "Audience response percentages: \n"
    for i in range(len(answers)):
        if correct in answers[i]:
            result_text += f"{answers[i]}: {correct_percent:.2f}%  \n"
        else:
            result_text += f"{answers[i]}: {percents[-1]}%  \n"
            percents.pop()
    display_lifeline_result(result_text)

def display_congratulations_screen(win):
    screen.fill((255, 255, 255))  # Fill the screen with white
    font = pygame.font.Font(None, 36)
    
    # Load the image
    win_image = pygame.image.load("win.jpg")
    win_image_rect = win_image.get_rect(center=(width // 2, height // 2 - 100))
    screen.blit(win_image, win_image_rect)
    
    # Render and display the message
    text = font.render(f"Congratulations! You Win {win}!", True, (0, 0, 0))  # Black color
    text_rect = text.get_rect(center=(width // 2, height // 2 + 100))
    screen.blit(text, text_rect)
    
    # Create Quit button
    quit_button = pygame.Rect(width // 2 - 100, 500, 200, 50)
    
    # Render button text
    font = pygame.font.Font(None, 24)
    quit_text = font.render("Quit", True, (0, 0, 0))
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    pygame.draw.rect(screen, (200, 200, 200), quit_button)  # Default color
        
    screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 15))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

flag50_50 = "off"
while running:
    user_answer = False
    is_50_50 = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                mouse_pos = pygame.mouse.get_pos()
                for button_surface, button_rect, answer_text, correct_answer in answer_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        selected_answer_button = button_surface, button_rect
                        answer_selected = True
                        user_answer = handle_button_click(answer_text, correct_answer)
                        answer_button_clicked = True
                # Check if help buttons are clicked
                if fifty_fifty_button_rect.collidepoint(mouse_pos):
                    remaining_answers, ind1, ind2 = fifty_fifty([answer for _, _, answer, _ in answer_buttons], current_question[2])
                    print("Remaining answers after using 50:50 lifeline:", remaining_answers)
                    help_options.remove("50:50")
                    flag50_50 = "on"
                elif phone_friend_button_rect.collidepoint(mouse_pos):
                    phone_a_friend(current_question[2])
                    help_options.remove("Friend-call")
                elif ask_audience_button_rect.collidepoint(mouse_pos):
                    ask_the_audience([answer for _, _, answer, _ in answer_buttons])
                    help_options.remove("Audience")
    # Fill the screen with the background image
    screen.blit(background_image, (0, 0))

    # Create question and answer buttons
    if current_question:
        question, answers, correct_answer = current_question

        question_button, question_button_rect = create_button(question, pygame.font.Font(None, 36), GRAY, GRAY, 50, 450, 700, 50)
        
        answer_buttons = []
        for idx, answer in enumerate(answers):
            if flag50_50 == "on":
                if idx == int(ind2) or idx == int(ind1):
                    answer_buttons.append(create_button(answer, pygame.font.Font(None, 28), GRAY, WHITE, 50 + idx * 200, 550 , 200, 30) + (answer, correct_answer))
                else:
                    continue
            else:
                answer_buttons.append(create_button(answer, pygame.font.Font(None, 28), GRAY, WHITE, 50 + idx * 200, 550 , 200, 30) + (answer, correct_answer))

        if "50:50" in help_options:
            fifty_fifty_button, fifty_fifty_button_rect = create_button("50:50", pygame.font.Font(None, 24), GRAY, WHITE, 650, 50, 100, 40)
            screen.blit(fifty_fifty_button, fifty_fifty_button_rect)
        if "Friend-call" in help_options:
            phone_friend_button, phone_friend_button_rect = create_button("Phone a Friend", pygame.font.Font(None, 18), GRAY, WHITE, 650, 100, 150, 40)
            screen.blit(phone_friend_button, phone_friend_button_rect)
        if "Audience" in help_options:
            ask_audience_button, ask_audience_button_rect = create_button("Ask the Audience", pygame.font.Font(None, 18), GRAY, WHITE, 650, 150, 150, 40)
            screen.blit(ask_audience_button, ask_audience_button_rect)

        # Draw buttons
        screen.blit(question_button, question_button_rect)
        for button_surface, button_rect, _, _ in answer_buttons:
            screen.blit(button_surface, button_rect)

    # Draw points button
    #points_button, points_button_rect = create_button(f"Points: {points[question_counter]}", points_font, GRAY, GRAY, 50, 50, 130, 50)
    #screen.blit(points_button, points_button_rect)
    
    if question_counter == 5:
        scored = "1000$"
    elif question_counter == 10:
        scored = "32000$"
    points_button, points_button_rect = create_points_button(question_counter, scored)
    screen.blit(points_button, points_button_rect)
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

    # Display result after answer is selected
    if answer_selected:
        flag50_50 = "off"
        pygame.time.wait(1000)  # Wait 5 seconds
        if user_answer:
            question_counter += 1
            if question_counter <= 15:
                current_question = get_random_question()
                answer_selected = False
                selected_answer_button = None
                answer_button_clicked = False
            else:
                print("Congratulations! You Win!")
                display_congratulations_screen(points[16])
        else:
            display_congratulations_screen(scored)

    # Draw selected answer button in orange
    if selected_answer_button:
        button_surface, button_rect = selected_answer_button
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)
        if answer_button_clicked:
            pygame.draw.rect(button_surface, ORANGE, (0, 0, button_rect.width, button_rect.height))
            screen.blit(button_surface, button_rect)
# Quit Pygame
pygame.quit()
sys.exit()
