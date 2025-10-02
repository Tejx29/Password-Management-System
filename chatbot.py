import aiml
import os

def load_bot():
    bot = aiml.Kernel()
    brain_file = "data/bot_brain.brn"
    if os.path.isfile(brain_file):
        bot.bootstrap(brainFile=brain_file)
    else:
        bot.learn("data/chatbot.aiml")
        bot.saveBrain(brain_file)
    return bot
