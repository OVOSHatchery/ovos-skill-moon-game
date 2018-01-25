# Author: Jordan Madrid
# Date: 11/25/2016
# Title: Apollo 11 Space Game


# First, I need to import a few things.
from sys import argv
from sys import exit
from os.path import exists

script, first_name, last_name = argv

# Introduction. This where you go to the gate and the guard asks for your ID.
def introduction(first_name,last_name):
    print "You pull up to the gated compound in your car and greet the guard."
    print "'Hello, sir, please present your ID.'"
    print "Present ID (Yes/No)? "
    choiceid = raw_input("> ").lower()

    if choiceid == "yes":
        print "The guard says excitedly:"
        print """
        'Hello! Welcome to the Kennedy Space Center. Today is the day we make history against the Russian communists. Today is the day Neil Armstrong, Michael Collins, Edwin Aldrin and you go to the moon.'
        """ % (first_name,last_name)
        print "'Please head to the briefing center.'\n"
        briefing(first_name,last_name)

    elif choiceid == "no":
        print "'Sir, I won't ask you again, please present your ID.' The guard says sternly."
        print "Present ID (Yes/No)?"
        choiceid2 = raw_input("> ").lower()
        if choiceid2 == "yes":
            print "'Thank you. We are glad to have you on board today for the moon launch.' He says reservedly." % (first_name,last_name)
            print "'Please head to the briefing center.'\n"
            briefing(first_name,last_name)
        if choiceid2 == "no":
            dead("'Sir, get your hands on the ground.' he screams. 'You are now arrested.'")

    else:
        dead("'Sir, get your hands on the ground.' he screams. 'You are now arrested.'")

# Here is the briefing part of my adventure.
def briefing(first_name,last_name):
    print "You drive to the briefing center and park."
    print "You walk into the esteemed building and goosebumps go down your neck."
    print "You find the briefing room and open the doors...\n"
    print "'Welcome! yells out a voice." % (first_name,last_name)
    print "Do you respond warmly, harshly or not at all?\n"

    choice_response = raw_input("> ").lower()

    if "warm" in choice_response:
        print "'I always knew you were a nice guy, %s %s!' he says.\n" % (first_name,last_name)
    elif "harsh" in choice_response:
        print "'You must have had a rough night. I don't blame you.' He responds.\n"
    elif "not at" in choice_response:
        print "A silent type. Got it."
    else:
        print "You're an odd duck, aren't you?\n"

    print "'Alright everyone, I'm Flight Director Gene Kranz, nice to meet you.\n"
    print """
    I've called you all here because we have an import mission. We are going to the moon, and you four are the tip of the spear. Things may go wrong, but here at Mission Control we will do everything in our power to make sure that doesn't happen. I will close with, good luck to everyone.
    """
    print "'Any questions or comments?'\n"
    print "1) What's our survival percentage, Gene?"
    print "2) That was a terrible speech."
    print "3) Let's do this."

    choice_response2 = raw_input("Please type 1, 2, or 3: ")

    if choice_response2 == "1":
        print "'Margaret Hamilton's calculated it to be around 25%.' He responded grimly."
    elif choice_response2 == "2":
        print "'Well, thank you. Your reputation precedes you.' He smiles cheekishly." % (first_name,last_name)
    elif choice_response2 == "3":
        print "Every responds 'hooah'!"
    else:
        pass
    print "\nAll right boys, suit up! Gene yells."
    outfit()


# Here is the third part of my astronaut adventure, putting on clothes.
def outfit():
    print "\nYou walk to the changing room where you get on your astronaut suit.\n"
    astronaut_suit = ["gloves", "body suit", "helmet", "boots"]
    print "Choose one of the following items to put on:"
    print astronaut_suit

    while len(astronaut_suit) > 0:
        choice_suit = raw_input("> ").strip()
        if choice_suit in astronaut_suit and len(astronaut_suit) > 2:
            astronaut_suit.remove(choice_suit)
            print "Nice, you put on %s" % choice_suit
            print "These items are left to put on:"
            print astronaut_suit
        elif len(astronaut_suit) == 2:
            astronaut_suit.remove(choice_suit)
            print "Nice, you put on the %s" % choice_suit
            print "The last item for you to put on:", astronaut_suit
        elif len(astronaut_suit) == 1:
            astronaut_suit.remove(choice_suit)
            print "You are done putting on things! Congratulations."
            board()
        else:
            print "You didn't select an item"
            print "These items are left to put on:"
            print astronaut_suit

def board():
    print "\nAs one of the astronauts going to the Moon, you start boarding the Saturn V rocket.\n"
    print "\nAs you are walking onto the rocket, you notice something peculiar about the launch door.\n"

    print "Press 1: Examine the pecularity."
    print "Press 2: Ignore it."

    rocketLaunch = raw_input("> ")

    if rocketLaunch == "1":
        print "An engineer comes over and examines the problem."
        print "'Looks like a minor tear in the hull, I'll get the boys to get it fixed but it will be a couple hours.' he says."
        launch(first_name)

    elif rocketLaunch == "2":
        print "You board the rocket, strap in and the ignition starts up."
        print "Suddenly, one of your gauges flashes red."
        print "Mission control contacts you over your microphone and recommends you evacuate the spacecraft."
        print "Do you evacuate or stay on the ship?"

        evacuation = raw_input("> ")

        if "evacuate" in evacuation:
            print "Your ejection pod deploys, you feel the g-forces and black out."
            print dead("You wake up in a hospital and have no memory of anything.")
        elif "stay" in evacuation:
            print "You colleagues deploy their escape pods."
            print dead("Miraculously, the ship holds and you are now in orbit, on your way to the moon without support.")
        else:
            print dead("You freeze with your inaction, the ship holds and you are now in orbit,on your way to the moon without support.")

    else:
        print dead("You board the ship, only for it to blow up immediately.")

def launch(first_name):
    print "After a few hours, you board the ship once more and strap in."
    print "Aldrin says '%s, the launch codes are 90210, punch them in one at a time, making sure to press enter after each time.'" % (first_name)
    launch_codes = []
    final_launch = ["9", "0", "2", "1", "0"]

    for i in range(0,5):
        number_input = raw_input("> ")
        launch_codes.append(number_input)
        print "You typed in %s" % number_input

    if launch_codes == final_launch:
        print "Launch sequence confirmed."
        print "'Here we go, gentleman!' Said Armstrong."
        moon_landing()

    if launch_codes != final_launch:
        print "ERROR: INCORRECT LAUNCH CODES."
        print dead("Initiating self-destruct sequence.")

def moon_landing():
    print "You are now orbiting above the moon with your three compatriots."
    print "Do you try to land on the moon with the lander vehicle or stay in orbit?"
    landing_choice = raw_input("> ").lower()

    if "land" in landing_choice:
        print "Aldrin, Armstrong and you board the lander vehicle and launch to the moon."
        land()
    if "stay" in landing_choice:
        print "Collins and you stay in the main vehicle to support Aldrin and Armstrong in orbit."
        stay()

def stay():
    print "While the other jettison to the moon, you two have a chat while monitoring their signal."
    print "You notice Collins is nervous and twitchy."
    print "He starts asking you a series of yes or no questions."
    kind_or_mean = ["'Do you like me?'", "'Do you think we'll survive?'", "'Do you trust the team?'",
                    "'Does mission control have confidence in us?'",
                    "'Do you think we aren't alone in the universe?'", "'Am I going to die on this trip?'"]
    collin_sanity = 0

    for question in range(0,5):
        print kind_or_mean.pop()
        fear_choice = raw_input("> ").lower()
        if "yes" in fear_choice:
            print "That's comforting!"
            collin_sanity += 1
        elif "no" in fear_choice:
            print "oh No!"
        else:
            print "I don't know what you're talking about!"

    if collin_sanity > 2:
        print "'Thanks you've calmed my nerves, let's get those boys home.' He says."
        return_home()
    else:
        print dead("'You're right, there is no reason to live!' Collins hits the airlock and you both are sucked into space.")

def land():
    print "As you are about to land, the 1201 and 1202 alarms start going off inside the lander."
    print "Armstrong and Aldrin are torn and they look to you to decide."
    print "Do you ignore the alarms or abort the mission and go back?"
    abort_choice = raw_input("> ").lower()
    if "ignore" in abort_choice:
        print "You tell them to ignore the alarms."
        print "Margaret Hamilton's code automatically ignores non-essential tasks and guides the lander to the moon."
        print "You land gently on the moon and the rest is history.\n"
        moon_launch()
    if "abort" in abort_choice:
        print dead("You accidently press the wrong button and hit the moon going 7152 feet per second.")

def moon_launch():
    print "After finishing your exploration, all three of you go into the lander to take off."
    print "Armstrong accidently breaks a lever."
    print "You see a pencil that may act as a makeshift lever, do you push it into the lever slot (Yes/No)?"
    pencil_choice = raw_input("> ").lower()
    if pencil_choice == "yes":
        print "You push it in and pull down on the pencil."
        print "The engines roar to life and the lander takes off."
        return_home()
    if pencil_choice == "no":
        print "Armstrong becomes increasingly despondent, and blames both of you."
        print dead("He attacks you, severing your oxygen accidently.")

def return_home():
    print "The lander safely returns from the moon to the ship."
    print "It attaches to the ship and makes it safely back to earth, entering earth's orbit flawlessly."
    print "You touch down in the ocean, only to have the U.S. forces pick you up"
    print "You receive several awards for your daring mission to the moon! Great job and congratulations!"
    exit(0)

def dead(why):
    print why, "Try again (yes/no)?"
    try_again = raw_input("> ").lower()
    if try_again == "yes":
        introduction(first_name, last_name)
    else:
        print "Thanks for playing!"
        exit(0)

introduction(first_name, last_name)