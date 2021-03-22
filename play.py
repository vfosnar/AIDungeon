#!/usr/bin/env python3
# ===== SETUP =====
import os
import random
import sys
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from generator.gpt2.gpt2_generator import *
from story import grammars
from story.story_manager import *
from story.utils import *
import argparse

from platform import system
system_name = system()
# =================



def logo():
    # Display logo
    with open("opening.txt", "r", encoding="utf-8") as file:
        starter = file.read()
    print(starter)

def clear():
    # Clear screen
    if(system_name == "Windows"):
        os.system("cls")
    else:
        os.system("clear")

def ui_menu():
    clear()
    logo()
    
    # Prompt user
    print("0) Exit\n1) New Game\n2) Saves")
    choice = get_num_options(3)

    return choice



# ===== SAVES =====
def ui_menu_saves():
    # Load saves file
    save_path = "./saved_stories/"
    saves_file_path = os.path.join(save_path, "saves.json")
    saves = {}
    if(os.path.isfile(saves_file_path)):
        with open(saves_file_path, "r", encoding="utf-8") as file:
            saves = json.loads(file.read())
    
    while 1:
        print()
        print("Select story")
        # Print saves
        hashes_by_index = {}
        print("0) Back")
        for i, story in enumerate(saves):
            print("{0}) {1}".format(i+1, story))
            hashes_by_index[i] = saves[story]["md5"]
        
        # Prompt user
        choice = get_num_options(len(saves) + 1)
        if(choice == 0): return 0, 0, 0

        choice_action = ui_menu_saves_game()
        if(choice_action != 0):
            return choice_action, hashes_by_index[choice - 1], list(saves)[choice - 1]

def ui_menu_saves_game():
    print()
    print("0) Back\n1) Play\n2) Remove")
    choice = get_num_options(3)
    return choice
# =================



# ===== New Game =====
def ui_menu_new():
    with open(YAML_FILE, "r") as stream:
        data = yaml.safe_load(stream)

    print()
    print("Select how to generate story")
    print("0) Back\n1) Random\n2) Prompts")
    choice = get_num_options(3)

    if choice == 0:
        return 0, None, None, None, None
    elif choice == 1:
        return ui_menu_new_random(data)
    
    # Prompts
    print("\n\nPick a setting.")
    settings = data["settings"].keys()
    for i, setting in enumerate(settings):
        print_str = str(i) + ") " + setting
        if setting == "fantasy":
            print_str += " (recommended)"

        console_print(print_str)
    console_print(str(len(settings)) + ") custom")
    choice = get_num_options(len(settings) + 1)

    if choice == len(settings):
        return "custom", None, None, None, None

    setting_key = list(settings)[choice]

    print("\nPick a character")
    characters = data["settings"][setting_key]["characters"]
    for i, character in enumerate(characters):
        console_print(str(i) + ") " + character)
    character_key = list(characters)[get_num_options(len(characters))]

    name = input("\nWhat is your name? ")
    setting_description = data["settings"][setting_key]["description"]
    character = data["settings"][setting_key]["characters"][character_key]

    return setting_key, character_key, name, character, setting_description

def ui_menu_new_random(story_data):
    # random setting
    settings = story_data["settings"].keys()
    n_settings = len(settings)
    n_settings = 2
    rand_n = random.randint(0, n_settings - 1)
    for i, setting in enumerate(settings):
        if i == rand_n:
            setting_key = setting

    # random character
    characters = story_data["settings"][setting_key]["characters"]
    n_characters = len(characters)
    rand_n = random.randint(0, n_characters - 1)
    for i, character in enumerate(characters):
        if i == rand_n:
            character_key = character

    # random name
    name = grammars.direct(setting_key, "character_name")

    return setting_key, character_key, name, None, None

def ui_menu_new_custom():
    context = ""
    console_print(
        "\nEnter a prompt that describes who you are and the first couple sentences of where you start "
        "out ex:\n 'You are a knight in the kingdom of Larion. You are hunting the evil dragon who has been "
        + "terrorizing the kingdom. You enter the forest searching for the dragon and see' "
    )
    prompt = input("Starting Prompt: ")
    return context, prompt

def ui_menu_new_curated(
    setting_key, character_key, name, character, setting_description
):
    name_token = "<NAME>"
    try:
        context = grammars.generate(setting_key, character_key, "context") + "\n\n"
        context = context.replace(name_token, name)
        prompt = grammars.generate(setting_key, character_key, "prompt")
        prompt = prompt.replace(name_token, name)
    except:
        context = (
            "You are "
            + name
            + ", a "
            + character_key
            + " "
            + setting_description
            + "You have a "
            + character["item1"]
            + " and a "
            + character["item2"]
            + ". "
        )
        prompt_num = np.random.randint(0, len(character["prompts"]))
        prompt = character["prompts"][prompt_num]

    return context, prompt

def instructions():
    text = "\nAI Dungeon 2 Instructions:"
    text += '\n Enter actions starting with a verb ex. "go to the tavern" or "attack the orc."'
    text += '\n To speak enter \'say "(thing you want to say)"\' or just "(thing you want to say)" '
    text += "\n\nThe following commands can be entered for any action: "
    text += '\n  "/revert"   Reverts the last action allowing you to pick a different action.'
    text += '\n  "/quit"     Quits the game and saves'
    text += '\n  "/restart"  Starts the game from beginning with same settings'
    text += '\n  "/save"     Makes a new save of your game and gives you the save ID'
    text += '\n  "/print"    Prints a transcript of your adventure (without extra newline formatting)'
    text += '\n  "/help"     Prints these instructions again'
    text += '\n  "/censor off/on" to turn censoring off or on.'
    return text
# ====================



# ===== GAME MENU =====
def ui_game_save(story_manager):
    print()
    print("0) Back\n1) Save as")
    if(story_manager.story.uuid != None): print("2) Save")

    choice = get_num_options(3 if (story_manager.story.uuid != None) else 2)
    if choice == 0: return 0

    savename = None
    if choice == 1: # Save as
        # Set savename
        while 1:
            print()
            print("Enter new save name:")
            savename = input()
            if(savename != ""): break
    
    story_manager.story.save_to_storage(savename)
# =====================



def play_aidungeon_2(a_temp, a_censor, a_generate):
    print("\n========================================================")
    print("Initializing AI Dungeon! (This might take a few minutes)\nwith parameters:\ntemp={0}\ncensor={1}\ngenerate={2}".format(a_temp, a_censor, a_generate))
    print("========================================================\n")

    generator = GPT2Generator(temperature=a_temp, censor=a_censor, generate_num=a_generate)
    story_manager = UnconstrainedStoryManager(generator)

    while True:
        if story_manager.story != None:
            story_manager.story = None

        while story_manager.story is None:
            print("\n\n")
            ui_menu_choice = ui_menu()
            
            if ui_menu_choice == 0: # Exit game
                exit(0)

            if ui_menu_choice == 1: # New game
                (
                    setting_key,
                    character_key,
                    name,
                    character,
                    setting_description,
                ) = ui_menu_new()
                
                if setting_key == 0:
                    continue

                if setting_key == "custom":
                    context, prompt = ui_menu_new_custom()

                else:
                    context, prompt = ui_menu_new_curated(
                        setting_key, character_key, name, character, setting_description
                    )

                print("\nGenerating story...")

                result = story_manager.start_new_story(
                    prompt, context=context
                )

                clear()
                logo()

                console_print(instructions())

                print("\n\n")

                console_print(result)

            else: # Load game
                while 1:
                    choice_action, choice_story_id, choice_story_savename = ui_menu_saves()
                    if(choice_action == 0): # Back
                        break
                    if(choice_action == 2): # Remove save

                        save_path = "./saved_stories/"
                        saves_file_path = os.path.join(save_path, "saves.json")
                        saves = {}
                        # Load current saves
                        if(os.path.isfile(saves_file_path)):
                            with open(saves_file_path, "r", encoding="utf-8") as file:
                                saves = json.loads(file.read())
                        # Remove savefile
                        os.remove(os.path.join(save_path, "story" + choice_story_id + ".json"))
                        saves.pop(choice_story_savename)
                        # Update file
                        with open(saves_file_path, "w", encoding="utf-8") as file:
                            file.write(json.dumps(saves))
                    else:
                        # Load game
                        break
                if(choice_story_id == 0):
                    # "Back" was selected, display menu again
                    continue

                # Load game
                print("\nLoading Game...\n")

                result = story_manager.load_new_story(choice_story_id)

                clear()
                logo()

                console_print(result)

        while True:
            sys.stdin.flush()
            action = input("> ").strip()
            if len(action) > 0 and action[0] == "/":
                split = action[1:].split(" ")  # removes preceding slash
                command = split[0].lower()
                args = split[1:]

                if command == "restart":
                    story_manager.story.actions = []
                    story_manager.story.results = []
                    console_print("Game restarted.")
                    console_print(story_manager.story.story_start)
                    continue

                elif command in ["quit", "exit", "stop", "return", "menu"]:
                    id = ui_game_save(story_manager)
                    if(id != 0):
                        time.sleep(2)
                        story_manager.story = None
                        break

                elif command == "help":
                    console_print(instructions())

                elif command == "censor":
                    if len(args) == 0:
                        if generator.censor:
                            console_print("Censor is enabled.")
                        else:
                            console_print("Censor is disabled.")
                    elif args[0] == "off":
                        if not generator.censor:
                            console_print("Censor is already disabled.")
                        else:
                            generator.censor = False
                            console_print("Censor is now disabled.")

                    elif args[0] == "on":
                        if generator.censor:
                            console_print("Censor is already enabled.")
                        else:
                            generator.censor = True
                            console_print("Censor is now enabled.")

                    else:
                        console_print("Invalid argument: {}".format(args[0]))

                elif command == "save":
                    ui_game_save()
                
                elif command == "print":
                    print("\nPRINTING\n")
                    print(str(story_manager.story))

                elif command == "revert":
                    if len(story_manager.story.actions) == 0:
                        console_print("You can't go back any farther. ")
                        continue

                    story_manager.story.actions = story_manager.story.actions[:-1]
                    story_manager.story.results = story_manager.story.results[:-1]
                    console_print("Last action reverted. ")
                    if len(story_manager.story.results) > 0:
                        console_print(story_manager.story.results[-1])
                    else:
                        console_print(story_manager.story.story_start)
                    continue

                else:
                    console_print("Unknown command: {}".format(command))

            else:
                if action == "":
                    action = ""
                    result = story_manager.act(action)
                    console_print(result)

                elif action[0] == '"':
                    action = "You say " + action

                else:
                    action = action.strip()

                    if "you" not in action[:6].lower() and "I" not in action[:6]:
                        action = action[0].lower() + action[1:]
                        action = "You " + action

                    if action[-1] not in [".", "?", "!"]:
                        action = action + "."

                    action = first_to_second_person(action)

                    action = "\n> " + action + "\n"

                result = "\n" + story_manager.act(action)
                if len(story_manager.story.results) >= 2:
                    similarity = get_similarity(
                        story_manager.story.results[-1], story_manager.story.results[-2]
                    )
                    if similarity > 0.9:
                        story_manager.story.actions = story_manager.story.actions[:-1]
                        story_manager.story.results = story_manager.story.results[:-1]
                        console_print(
                            "Woops that action caused the model to start looping. Try a different action to prevent that."
                        )
                        continue

                if player_won(result):
                    console_print(result + "\n CONGRATS YOU WIN")
                    story_manager.story.get_rating()
                    break
                elif player_died(result):
                    console_print(result)
                    console_print("YOU DIED. GAME OVER")
                    console_print("\nOptions:")
                    console_print("0) Start a new game")
                    console_print(
                        "1) \"I'm not dead yet!\" (If you didn't actually die) "
                    )
                    console_print("Which do you choose? ")
                    choice = get_num_options(2)
                    if choice == 0:
                        story_manager.story.get_rating()
                        break
                    else:
                        console_print("Sorry about that...where were we?")
                        console_print(result)

                else:
                    console_print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--temp", help="adjust creativity of GPT2 model", type=float, default=0.4)
    parser.add_argument("--censor", help="censor output", type=bool, default=False)
    parser.add_argument("--generate", help="length of text generated", type=int, default=60)
    args = parser.parse_args()
    play_aidungeon_2(args.temp, args.censor, args.generate)
