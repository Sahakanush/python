import data
import random
import re


count = 3
points = "0$"
score = "0$"

def shorten_question(question, correct):
    pass

def phone_a_friend():
    pass

def audience():
    pass

def help(question, correct, turn):
    global count
    if count == 0:
        print("Help options are limited.")
        return False
    print("You have 3 help options. \nAnd a chance to use it", count, "times. \n1. 50:50 \t 2. Phone-a-Friend \t 3. Ask the Audience ")
    choice = input("Choose [1, 2, 3]: ")
    if choice == "1":
        shorten_question(question, correct)
        count -= 1
    elif choice == "2":
        phone_a_friend()
        count -= 1
    elif choice == "3":
        audience()
        count -= 1
    else:
        print("Please use the allowed options [1, 2, 3]")
        help()
        
def check_answer(question, correct, turn):
    global count, points
    if count == 0:
        answer = input("Your answer please [you dont have help options anymore]: ")
    else:
        answer = input("Your answer please [if you need any help, write h]: ")

    if answer.lower() == "h":
        result = help(question, correct, turn)
        if result == False:
            check_answer(question, correct, turn)
    elif answer.lower() == correct:
        print("TRUE")
        points = data.prize(turn)
        if points == "1000000$":
            return "Win"
        else:
            print("You won", points)
    elif answer.lower() in ["a","b","c","d"]:
        print("You earned ", data.scored_points(turn))
        print("Game is over")
        exit()
    else:
        print("Please use the allowed options [a,b,c,d]")
        check_answer(question, correct, turn)

def generate_answers(answers, correct):
    random.shuffle(answers)
    option = ["a", "b", "c", "d"]
    for i in range(4):
        print(" ", option[i], ".", answers[i], sep="")
        if answers[i] == correct:
            correct_option = option[i]
    return correct_option

def generate_question(q, turn):
    print(turn, ".", sep="", end=" ")
    question = random.choice(list(q.keys()))
    return question

def win():
    print("Congratulations !!!\nYou won 1.000.000$ !!!")

def game(q):
    i = 1
    while len(q) > 0:
        question = generate_question(q, i)  
        print(question)    
        correct_option = generate_answers(q[question]["answer_choices"], q[question]["correct_answer"])
        result = check_answer(q, correct_option, i)
        if result == "Win":
            win()
        print()
        i += 1
        q.pop(question)

def get_content(file):
    with open(file, 'r') as file:
        questions_data = file.readlines()  
    return questions_data

def is_valid_question(questions):
    pattern = re.compile(r'^([^?]+)\?:([^,]+),([^,]+),([^,]+),([^,]+)$')
    for i in questions:
        valid_question = bool(pattern.match(i))
        if not valid_question:
            return False
    return True

def get_questions(questions_data):
    data = {}
    for i in questions_data:
        parts = i.split(':')
        if len(parts) == 2:
            question = parts[0].strip()
            answer_choices = [choice.strip() for choice in parts[1].split(',')]
            correct_answer = parts[1][0].strip()

            data[question] = {
                'answer_choices': answer_choices,
                'correct_answer': correct_answer,
            }
    return data

if __name__ == "__main__":
    file_path = "questions.txt"
    file_content = get_content(file_path)
    valid_content = is_valid_question(file_content)
    if valid_content:
        content = get_questions(file_content)
        game(content)
    else:
        print("The imported data is not valid.")
        exit()
