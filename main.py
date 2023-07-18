import openai

text = "Create text based adventure game from a description of the game. a response should be in this format\nDescription of what happens after paragraph\n\nQuestion paragraph\n\nA) answer 1\nB) answer 2\nC) answer 3"
chat = [{'role': 'user', 'content': text}]
start_sequence = "\n\nQuestion: "
restart_sequence = "\n\nAnswer"


def answer():
    chat.append({'role': 'user', 'content': new})
    try:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat,
            temperature=.5,
            max_tokens=256
        ).choices[0].message
    except openai.error.APIConnectionError:
        input('Cannot connect servers press enter to retry')
        result = answer()
    return result


try:
    while True:
        new = input('you: ')
        chat.append({'role': 'user', 'content': new})
        completion = answer()
        chat.append(completion)
        print(completion.content)
except KeyboardInterrupt:
    pass
# A fantasy where you are wizard trying to get all the spells
