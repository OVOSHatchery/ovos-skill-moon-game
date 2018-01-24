# NO LICENSE

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill

from os.path import dirname
import sys
sys.path.append(dirname(__file__))
from intent_tools import IntentParser, IntentLayers


__author__ = 'jarbas'


class Apollo11GameSkill(MycroftSkill):
    def __init__(self):
        super(Apollo11GameSkill, self).__init__()
        self.playing = False
        self.equiped = []
        self.items = ["gloves", "boots", "helmet", "body suit"]

    def initialize(self):
        self.parser = IntentParser(self.emitter)
        self.layers = IntentLayers(self.emitter)

        # build layer 0, start game
        intent = IntentBuilder("StartApollo11Intent"). \
            require("StartKeyword"). \
            require("GameKeyword").build()
        self.register_intent(intent, self.handle_start_intent)

        intent = IntentBuilder("StopApollo11Intent"). \
            require("StopKeyword"). \
            require("GameKeyword").build()
        self.register_intent(intent, self.handle_stop_intent)

        layer = ["StartApollo11Intent"]
        self.layers.add_layer(layer)  # 0

        layer = ["StopApollo11Intent", "Yes1Apollo11Intent",
                 "No1Apollo11Intent"]
        self.layers.add_layer(layer)  # 1

        layer = ["StopApollo11Intent", "Yes2Apollo11Intent",
                 "No2Apollo11Intent"]
        self.layers.add_layer(layer)  # 2

        layer = ["StopApollo11Intent", "WarmApollo11Intent",
                 "HarshApollo11Intent", "NoAnswerApollo11Intent"]
        self.layers.add_layer(layer)  # 3

        layer = ["StopApollo11Intent", "SurvivalApollo11Intent",
                 "BadSpeechApollo11Intent", "LetsDoItApollo11Intent"]
        self.layers.add_layer(layer)  # 4

        layer = ["StopApollo11Intent", "BoardApollo11Intent",
                 "SuitApollo11Intent", "HelmetApollo11Intent",
                 "GlovesApollo11Intent", "BootsApollo11Intent"]
        self.layers.add_layer(layer)  # 5

    # game start
    def handle_intro(self):
        self.speak_dialog("reach_gate")
        self.speak_dialog("guard")
        self.layers.activate_layer(1)
        self.speak_dialog("present_id", expect_response=True)

    # layer 1
    def handle_yes1(self, message):
        self.speak_dialog("guard_yes")
        self.briefing_question1()

    def handle_no1(self, message):
        self.speak_dialog("guard_no")
        self.speak_dialog("present_id", expect_response=True)
        self.layers.activate_layer(2)

    # layer 2
    def handle_yes2(self, message):
        self.speak_dialog("guard_yes_alternate")
        self.briefing_question1()

    def handle_no2(self, message):
        self.speak_dialog("guard_dead")
        self.handle_stop_intent(None)

    def briefing_question1(self):
        self.speak_dialog("guard_next")
        self.speak_dialog("briefing")
        self.speak_dialog("briefing_question", expect_response=True)
        self.layers.activate_layer(3)

    # briefing 1 - layer 3
    def handle_warm(self, message):
        self.speak_dialog("briefing_warm")
        self.briefing_question2()

    def handle_harsh(self, message):
        self.briefing_question2()
        self.speak_dialog("briefing_harsh")

    def handle_silence(self, message):
        self.speak_dialog("briefing_silence")
        self.briefing_question2()

    def briefing_question2(self):
        self.layers.activate_layer(4)
        self.speak_dialog("briefing_question2", expect_response=True)

    # briefing 2 - layer 4
    def suit_up(self):
        self.layers.activate_layer(5)
        self.speak_dialog("briefing_end")
        self.speak_dialog("suit_up")

    def handle_percentage(self, message):
        self.speak_dialog("briefing_percentage")
        self.suit_up()

    def handle_terrible(self, message):
        self.speak_dialog("briefing_terrible")
        self.suit_up()

    def handle_lets_do_this(self, message):
        self.speak_dialog("briefing_lets_do_this")
        self.suit_up()

    # space suit - layer 5
    def handle_board(self, message):
        if self.items != self.equiped:
            self.speak_dialog("boarding_fail")
            return
        self.layers.activate_layer(6)
        self.speak_dialog("boarding")

    def handle_helmet(self, message):
        item = "helmet"
        if item in self.equiped:
            self.speak_dialog("already_equipped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equiped.append(item)

    def handle_boots(self, message):
        item = "boots"
        if item in self.equiped:
            self.speak_dialog("already_equiped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equiped.append(item)

    def handle_gloves(self, message):
        item = "gloves"
        if item in self.equiped:
            self.speak_dialog("already_equiped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equiped.append(item)

    def handle_body_suit(self, message):
        item = "body suit"
        if item in self.equiped:
            self.speak_dialog("already_equiped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equiped.append(item)
    # boarding - layer 6

    # control

    def handle_start_intent(self, message):
        if not self.playing:
            self.playing = True
            self.speak_dialog("start.game")
            self.handle_intro()
        else:
            self.speak_dialog("already.started")

    def handle_stop_intent(self, message):
        if self.playing:
            self.speak_dialog("stop.game")
            self.stop()

    def stop(self):
        if self.playing:
            self.layers.reset()
            self.playing = False
            self.equiped = []

    def converse(self, utterances, lang="en-us"):
        if not self.playing:
            return False
        intent, skill_id = self.parser.determine_intent(utterances[0], lang)
        # will an intent from this skill trigger ?
        if skill_id == self.skill_id:
            # let it pass
            return False
        # take action
        if self.layers.current_layer == 1 or self.layers.current_layer == 2:
            self.speak_dialog("guard_dead")
            self.handle_stop_intent(None)
        elif self.layers.current_layer == 3:
            self.speak_dialog("briefing_other")
            self.briefing_question2()
        elif self.layers.current_layer == 4:
            self.suit_up()
        
        return True


def create_skill():
    return Apollo11GameSkill()