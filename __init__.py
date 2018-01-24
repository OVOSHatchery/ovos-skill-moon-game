# NO LICENSE

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.parse import extractnumber
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
        self.entries = 0
        self.entered_code = []
        self.correct_code = ["9", "0", "2", "1", "0"]
        self.questions = ["Do you like me?",
                          "Do you think we'll survive?",
                          "Do you trust the team?",
                          "Does mission control have confidence in us?",
                          "Do you think we aren't alone in the universe?",
                          "Am I going to die on this trip?"]
        self.current_question = 0
        self.sanity = 0

    def initialize(self):
        self.parser = IntentParser(self.emitter)
        self.layers = IntentLayers(self.emitter)

        # build intents
        intent = IntentBuilder("StartApollo11Intent"). \
            require("StartKeyword"). \
            require("GameKeyword").build()
        self.register_intent(intent, self.handle_start_intent)

        intent = IntentBuilder("StopApollo11Intent"). \
            require("StopKeyword"). \
            require("GameKeyword").build()
        self.register_intent(intent, self.handle_stop_intent)

        # build layers
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

        layer = ["StopApollo11Intent", "ExamineApollo11Intent",
                 "IgnoreApollo11Intent"]
        self.layers.add_layer(layer)  # 6

        layer = ["StopApollo11Intent", "EvacuateApollo11Intent",
                 "StayApollo11Intent"]
        self.layers.add_layer(layer)  # 7

        layer = ["StopApollo11Intent", "CodeResetApollo11Intent"]
        self.layers.add_layer(layer)  # 8

        layer = ["StopApollo11Intent", "LandApollo11Intent",
                 "OrbitApollo11Intent"]
        self.layers.add_layer(layer)  # 9

        layer = ["StopApollo11Intent", "ColinYesApollo11Intent",
                 "ColinNoApollo11Intent"]
        self.layers.add_layer(layer)  # 10

        layer = ["StopApollo11Intent", "AbortLandingApollo11Intent",
                 "IgnoreLandingApollo11Intent"]
        self.layers.add_layer(layer)  # 11

        layer = ["StopApollo11Intent", "PencilYesApollo11Intent",
                 "PencilNoApollo11Intent"]
        self.layers.add_layer(layer)  # 12

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
        self.speak_dialog("suit_up", expect_response=True)

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
        self.speak_dialog("boarding", expect_response=True)

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

    # board ship - layer 6
    def handle_examine(self, message):
        self.layers.activate_layer(8)
        self.speak_dialog("examine")
        self.speak_dialog("codes", expect_response=True)

    def handle_ignore(self, message):
        self.speak_dialog("ignore", expect_response=True)
        self.layers.activate_layer(7)

    # evacuation - layer 7
    def handle_evacuate(self, message):
        self.speak_dialog("evacuate_gameover")
        self.handle_stop_intent(None)

    def handle_stay(self, message):
        self.speak_dialog("stay_dead")
        self.handle_stop_intent(None)

    # launch codes - layer 8
    def check_code(self):
        if self.entered_code == self.correct_code:
            self.layers.activate_layer(9)
            self.speak_dialog("launch")
            self.speak_dialog("moon_landing", expect_response=True)
        else:
            self.speak_dialog("code_dead")
            self.handle_stop_intent(None)

    def handle_reset_code(self, message):
        if self.entries > 3:
            self.speak_dialog("bad.code")
            self.handle_stop_intent(None)
        else:
            self.entries -= 1
            self.speak_dialog("code.reset", {"left": 3 - self.entries})
            self.entered_code = []

    # moon landing - layer 9
    def handle_land(self, message):
        self.speak_dialog("moon_land", expect_response=True)
        self.layers.activate_layer(11)

    def handle_orbit(self, message):
        self.speak_dialog("moon_stay")
        self.layers.activate_layer(10)

    # stay on ship - layer 10
    def next_question(self):
        if self.current_question == len(self.questions) -1:
            if self.sanity > 2:
                self.speak_dialog("colin_calm")
                self.speak_dialog("go_home")
                self.handle_stop_intent(None)
            else:
                self.speak_dialog("colin_dead")
                self.handle_stop_intent(None)
        else:
            self.current_question += 1
            self.speak(self.questions[self.current_question],
                       expect_response=True)

    def handle_orbit_yes(self):
        self.sanity += 1
        self.speak_dialog("colin_yes")
        self.next_question()

    def handle_orbit_no(self):
        self.speak_dialog("colin_no")
        self.next_question()

    # land on moon - layer 11
    def handle_abort(self, message):
        self.speak_dialog("moon_land_abort", expect_response=True)
        self.handle_stop_intent(None)

    def handle_ignore_alarm(self, message):
        self.speak_dialog("moon_land_ignore")
        self.speak_dialog("moon_launch", expect_response=True)
        self.layers.activate_layer(12)

    # moon launch - layer 12
    def handle_pencil_yes(self, message):
        self.speak_dialog("pencil_yes")
        self.speak_dialog("go_home")
        self.handle_stop_intent(None)

    def handle_pencil_no(self, message):
        self.speak_dialog("pencil_no")
        self.handle_stop_intent(None)

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
            self.entries = 0
            self.sanity = 0
            self.current_question = 0
            self.entered_code = []

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
        elif self.layers.current_layer == 5:
            self.handle_board(None)
        elif self.layers.current_layer == 6:
            self.speak_dialog("boarding_dead")
            self.handle_stop_intent(None)
        elif self.layers.current_layer == 7:
            self.speak_dialog("evacuate_dead")
            self.handle_stop_intent(None)
        elif self.layers.current_layer == 8:
            number = extractnumber(utterances[0], lang)
            if number.isdigit():
                self.entered_code.append(number)
                self.speak_dialog("code_enter_number", {"number": number},
                                  expect_response=True)
                if len(self.entered_code) == len(self.correct_code):
                    self.check_code()
            else:
                self.speak_dialog("code_invalid", expect_response=True)
        elif self.layers.current_layer == 10:
            self.speak_dialog("colin_other")
            self.next_question()
        else:  # 9 11 12
            self.speak_dialog("invalid.command", expect_response=True)
        return True


def create_skill():
    return Apollo11GameSkill()