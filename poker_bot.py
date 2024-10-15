import os
from openai import OpenAI
import base64
import pyscreenshot as ImageGrab
import pygetwindow as gw
import time
from datetime import datetime


client = OpenAI(
    # ENTER YOUR CHAT GPT KEY
    api_key=""
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

#Set your Directory to where you want to have your screenshots saved
base_directory = ""

def select_window():
    # List all open windows
    windows = gw.getAllTitles()
    windows = [w for w in windows if w]  # Filter out empty titles

    # Display windows to user for selection
    print("Available windows:")
    for i, title in enumerate(windows):
        print(f"{i + 1}. {title}")

    # Get user's choice
    choice = int(input("Select a window by number: ")) - 1

    # Get the selected window
    dimensions = gw.getWindowGeometry(windows[choice])
    selected_window = {'title':windows[choice],
                       'left':dimensions[0],
                        'top':dimensions[1],
                        'width':dimensions[2],
                        'height':dimensions[3]
                        }
    return selected_window

def track_window(window):
    _, _, files = next(os.walk(base_directory))
    file_count = len(files)
    while True:
        messages = [
                {
                    "role": "system",
                    "content": """You are a professional poker player that plays online poker. 
                    Your goal is to maximize your total chips by playing in a game theory optimally.
                    For each response provide a decision of whether to fold, check, call, or raise.
                    In the event that you specificy raise, you must also specify how much you want to raise.
                    You should return your decisions in JSON format.
                    Keep your response short and to the point."""
                }
            ]
        # Update window's position and size
        start_time = datetime.now()
        window_rect = window['left'], window['top'], window['width'], window['height']
        print(f"Window Position: (x: {window['left']}, y: {window['top']}), Size: (width: {window['width']}, height: {window['height']})")
        # part of the screen
        im=ImageGrab.grab(bbox=(window['left'], window['top'], window['width'], window['height']))
        file_count += 1
        path_to_image = f'{base_directory}{file_count}.png'
        im.save(path_to_image)
        end_time = datetime.now()
        run_time = (end_time - start_time).total_seconds()
        print(f'Time to Save Screenshot: {run_time}')

        base64_image = encode_image(path_to_image)

        end_time = datetime.now()
        run_time = (end_time - start_time).total_seconds()
        print(f'Time to Encode Screenshot: {run_time}')

        messages.append({
            "role": "user",
            "content": ["What should I do?", {"image": base64_image}],
        })
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format={ "type": "json_object" }
        )

        reply = completion.choices[0].message.content

        messages.append({"role": "assistant", "content": reply})
        print(f'First reply: {reply}')
        end_time = datetime.now()
        run_time = (end_time - start_time).total_seconds()
        print(f'Time to Run: {run_time}')
        next_image = input("Enter Key to Trigger Logic")


if __name__ == "__main__":
    selected_window = select_window()
    if selected_window:
        print(f"Tracking window: {selected_window['title']}")
        track_window(selected_window)
    else:
        print("No window selected.")











