import random

def prize(i):
    points = {1:"100$",
              2:"200$",
              3:"300$",
              4:"500$",
              5:"1000$",
              6:"2000$",
              7:"4000$",
              8:"8000$",
              9:"16000$",
              10:"32000$",
              11:"64000$",
              12:"125000$",
              13:"250000$",
              14:"500000$",
              15:"1000000$"
              }
    return points[i]

def scored_points(turn):
    scored = {
        5:"1000$",
        10:"32000$"
    }
    if turn >= 10:
        return scored[10]
    if turn >= 5:
        return scored[5]
    
def phone_answers():
    responses = [
        "Hmm, I think the right answer is...",
        "Let me think... I'm pretty sure it's...",
        "Oh, that's a tough one. I'd go with...",
        "I remember reading about this. I'd say it's...",
        "I'm not entirely sure, but I'd guess..."
    ]
    return random.choice(responses)