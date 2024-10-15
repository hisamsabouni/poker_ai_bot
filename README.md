# poker_ai_bot
This is a simple python based project that can take a screenshot of a selected window you are using to play poker online. The screenshot is automatically ran through the ChatGPT api and returns a decision on how to proceed with the hand.

Make sure you enter your Open AI api key on line 11 to process your requests. 

```
client = OpenAI(
    # ENTER YOUR CHAT GPT KEY
    api_key=""
)
```

Make sure you set your base dicretory to a folder where you want to have your screenshots saved (before they are uploaded to OpenAI)
```
#Set your Directory to where you want to have your screenshots saved
base_directory = ""
```

Once you set the two variables above you can run from your command line by simply running 
```
python poker_bot.py
```

The project is open source. Feel free to make any suggestions or improvements. 

Key Issues
- Response time is too slow (averaging about 7 seconds)
  - That is without maintaining a history of hands played which could be useful to learn how players are responding
  - This gets very slow if we start embedding past images in the message history
- Base prompt can definitely be improved and a model could be fine tuned on poker hands. 
