import openai
import random
import json
import pyshorteners
s = pyshorteners.Shortener()

f = open("test.md", "w")
f.write('')
f.close()
text = "can you be a DM for Medieval Fantasy dnd 5e game where you make and pick the setting and adventure for 1 player you will tell us the options and we will pick. use markdown. images should only be made with functions. you can not have more than 4 images"
chat = [{'role': 'user', 'content': text}]
start_sequence = "\n\nQuestion: "
restart_sequence = "\n\nAnswer"
images = 0

def image(prompt):
    global images
    if images > 4:
        return 'Error: can not generate more than 4 images per response'
    images += 1
    url = s.tinyurl.short(openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )['data'][0]['url'])
    dalle = f'![{prompt}]({url})'
    print(dalle)
    return dalle


def dice(sides):
    return str(random.randint(1,sides+1))


def answer():
    chat.append({'role': 'user', 'content': new})
    try:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat,
            temperature=.5,
            max_tokens=500,
            functions=[
                {
                    "name": "dice",
                    "description": "roles a dice with n number of sides",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sides": {
                                "type": "integer",
                                "description": "number of sides on the dice",
                            }
                        },
                        "required": ["sides"]
                    },
                },
                {
                    "name": "AIimage",
                    "description": "Uses dall-e 2 to create a image and returns the markdown to display the image. the url will be a tinyurl to make it shorter",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "prompt to give dall-e 2",
                            }
                        },
                        "required": ["prompt"]
                    },
                }
            ]
        )
        if result.choices[0].message.content == None:
            if result.choices[0].message.function_call.name == 'dice':
                chat.append(
                    {
                        "role": "function",
                        "name": 'dice',
                        "content": dice(json.loads(result.choices[0].message.function_call.arguments)["sides"]),
                    }
                )
            elif result.choices[0].message.function_call.name == 'AIimage':
                chat.append(
                    {
                        "role": "function",
                        "name": 'AIimage',
                        "content": image(json.loads(result.choices[0].message.function_call.arguments)["prompt"]),
                    }
                )
            result = answer()
        else:
            result = result.choices[0].message
    except openai.error.APIConnectionError:
        input('Cannot connect servers press enter to retry')
        result = answer()
    except openai.error.ServiceUnavailableError:
        input('Server over load press enter to retry')
        result = answer()
    return result


try:
    while True:
        images = 0
        new = input('\033[92m   you: \033[0m')
        f = open("test.md", "a")
        f.write(f"""
### You
{new}

---""")
        f.close()
        chat.append({'role': 'user', 'content': new})
        completion = answer()
        chat.append(completion)
        f = open("test.md", "a")
        f.write(f"""
### AI
{completion.content}

---""")
        f.close()
except KeyboardInterrupt:
    pass
# A fantasy where you are wizard trying to get all the spells
