import data
import random
import re

def shorten_answers(answers):
    correct = answers[0]
    random_q = random.choice(answers)

def phone_a_friend():
    print("phone_a_friend")

def audience():
    print("audience")

def help(choice, answers):
    if choice == "50:50":
        shorten_answers(answers)
    elif choice == "Phone-a-Friend":
        phone_a_friend()
    elif choice == "Ask the Audience":
        audience()

def check_answer(answer, correct_option):
    if answer.lower() == "h":
        return "Help"
    elif answer.lower() == correct_option:
        return True
    elif answer.lower() in ["a","b","c","d"]:
        return False
    else:
        return "Wrong option"

def generate_answers(answers, correct):
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

def retry(q, question, answer, correct_option, i, help_options):
    print()
    print("You chose an incorrect option. Let's try the same question again.")
    print(question)
    print(answer)

    retry_input = input("Your answer please [if you need any help, write h]: ")
    result = check_answer(retry_input, correct_option)
    
    if result == "Help":
        print("You have", len(help_options), "help options.")
        print_options(help_options)
        choice = input("\nPlease choose an option: ")
        valid_option = help_valid_option(help_options, choice)
        if not valid_option:
            pass
        else:
            help(help_options[int(choice)-1], q[question]["answer_choices"])
            help_options.remove(help_options[int(choice)-1])
    elif result == "Wrong option":
        retry(q, question, answer, correct_option, i, help_options)
    elif result:
        if i == 15:
            print("Congratulations, you won $1,000,000 !!")
            exit
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

def print_options(help_options):
    for i in range(len(help_options)):
        print(i+1, ".", help_options[i], end="  ")

def help_valid_option(help_options, option):
    if 0 < int(option) <= len(help_options):
        return True
    else:
        return False
    
def game(q):
    i = 1
    help_options = ["50:50", "Phone-a-Friend", "Ask the Audience"]
    while len(q) > 0:
        question = generate_question(q)     
        answer, correct_option = generate_answers(q[question]["answer_choices"], q[question]["correct_answer"])
        print(i, ".", question, sep="") 
        print(answer)
        print(correct_option)

        if len(help_options) == 0:
            incoming_info = input("Your answer please [you dont have help options anymore]: ")
        else:
            incoming_info = input("Your answer please [if you need any help, write h]: ")

        result = check_answer(incoming_info, correct_option)
        if result == "Help":
            print("You have", len(help_options), "help options.")
            print_options(help_options)
            choice = input("\nPlease choose an option: ")
            valid_option = help_valid_option(help_options, choice)
            if not valid_option:
                pass
            else:
                help(help_options[int(choice)-1], q[question]["answer_choices"])
                help_options.remove(help_options[int(choice)-1])
        elif result == "Wrong option":
            retry(q, question, answer, correct_option, i, help_options)
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