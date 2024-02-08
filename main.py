import data
import random
import re

def shorten_answers(answers, answers_list):
    correct = answers_list[0]
    answers_list.remove(correct)
    random_a = random.choice(answers_list)
    options_list = answers.split('\n')

    for i in options_list:
        if correct in i or random_a in i:
            print(i)
        else:
            print("X")


def phone_a_friend(correct_answer):
    print(data.phone_answers(), correct_answer)

def audience(answers, answers_list):
    correct = answers_list[0]
    options_list = answers.split('\n')
    correct_percent = random.randint(50, 100)
    wrong_percent1 = random.randint(0, 100-correct_percent)
    wrong_percent2 = random.randint(0, 100-correct_percent-wrong_percent1)
    wrong_percent3 = 100-correct_percent-wrong_percent1-wrong_percent2
    percents = [wrong_percent1, wrong_percent2, wrong_percent3]
    for i in options_list:
        if correct in i:
            print(i, " --->", correct_percent, "%")
        else:
            print(i, " --->", random.choice(percents) ,"%")
            percents.pop()

def help(choice, answers, answers_list, question, i):
    if choice == "50:50":
        print_question(question, i)
        shorten_answers(answers, answers_list)
    elif choice == "Phone-a-Friend":
        phone_a_friend(answers_list[0])
        print_question(question, i, answers)
    elif choice == "Ask the Audience":
        print_question(question, i)
        audience(answers, answers_list)

def check_answer(answer, correct_option):
    if answer.lower() == "h":
        return "Help"
    elif answer.lower() == correct_option:
        return True
    elif answer.lower() in ["a","b","c","d"]:
        return False
    else:
        return "Wrong option"

def generate_answers(answers_data, correct):
    answers = answers_data.copy()
    option = ["a", "b", "c", "d"]
    random.shuffle(answers)
    answer = []
    for i in range(4):
        answer.append(" " + option[i] + "." + answers[i])
        if answers[i] == correct:
            correct_option = option[i]
    answers = '\n'.join(answer)
    return answers, correct_option

def generate_question(q):
    question = random.choice(list(q.keys()))
    return question

def win():
    print("Congratulations !!!\nYou won 1.000.000$ !!!")

def print_options(help_options):
    for i in range(len(help_options)):
        print(i+1, ".", help_options[i], end="  ")

def help_valid_option(help_options, option):
    if not option.isdigit():
        return False
    elif 0 < int(option) <= len(help_options):
        return True
    else:
        return False
    
def print_question(q, i, a=""):
    print(i, ".", q, sep="") 
    print(a)
    
def input_answer():
    incoming_info = input("Your answer please [if you need any help, write h]: ")
    return incoming_info

def check_result(result, answers, question, i, correct_option, answers_list):
    help_options = ["50:50", "Phone-a-Friend", "Ask the Audience"]   #  it is refreshed again on each call the function
    if result == "Help":
        print("You have", len(help_options), "help options.")
        print_options(help_options)
        choice = input("\nPlease choose an option: ")
        valid_option = help_valid_option(help_options, choice)
        if not valid_option:
            pass
        else:
            help(help_options[int(choice)-1], answers, answers_list, question, i)
            help_options.remove(help_options[int(choice)-1])
            incoming = input_answer()
            result = check_answer(incoming, correct_option)
            check_result(result, answers, question, i, correct_option, answers_list)
    elif result == "Wrong option":
        print_question(question, i, answers)
        incoming = input_answer()
        result = check_answer(incoming, correct_option)
        check_result(result, answers, question, i, correct_option, answers_list)
    elif result:
        if i == 15:
            print("Congratulations, you won $1,000,000 !!")
            exit()
        elif i == 5 or i == 10:
            print("Congratulations, You've won", data.scored_points(i), " intact")
        else:
            print("Congratulations, You've won", data.prize(i))
    elif not result:
        print("Your answer is wrong, game over")
        if i >= 10:
            print("You won", data.scored_points(10))
        elif i >= 5:
            print("You won", data.scored_points(5))
        else:
            print("You won 0$")
        exit()

def game(q):
    i = 1
    while len(q) > 0:
        question = generate_question(q)    
        answer, correct_option = generate_answers(q[question]["answer_choices"], q[question]["correct_answer"])
        print_question(question, i, answer)
        incoming = input_answer()
        result = check_answer(incoming, correct_option)
        check_result(result, answer, question, i, correct_option, q[question]["answer_choices"])
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
            correct_answer = answer_choices[0]

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