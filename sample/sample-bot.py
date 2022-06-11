# sample-bot.py - a sample bot using python-droit

from droit.Bot import Bot
from droit.pyvnt import Action, ConditionalAction


bot = Bot()
bot.init() # loop = True, genOutput = True
bot.import_rules_from_file("sample/german-sample.dds")


def getInput(*args, **kwargs) -> str:
    return input("Droit> ")

def outputData(output : str):
    print(output)


bot.events["input_await"].actions.append(
    Action(getInput, callback="input_received")
)

bot.events["input_received"].actions.append(
    ConditionalAction(lambda inp : inp == "exit", "quit")
)

bot.events["output_ready"].actions.append(
    Action(outputData, callback="output_sent")
)

bot.start()