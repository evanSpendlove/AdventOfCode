def countYeses(group) -> int:
    return len(set(group.replace('\n', '')))

def countAllYeses(group) -> int:
    group = group.replace('\n', ' ').split()
    questions = set(group[0])
    for person in group:
        questions = questions.intersection(set(person))
    return len(questions)

with open('input.in', 'r') as f:
    lines = f.read().split("\n\n")
    print(f"Sum of yeses: {sum([countYeses(group) for group in lines])}")
    print(f"Sum of all yeses: {sum([countAllYeses(group) for group in lines])}")
