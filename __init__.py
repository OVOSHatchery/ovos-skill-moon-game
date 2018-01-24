# NO LICENSE

from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util.parse import extractnumber
from os.path import join
from time import time, sleep

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

        questions = join(self.vocab_dir, self.lang + '/questions.voc')
        with open(questions) as f:
            self.questions = list(filter(bool, f.read().split('\n')))

        # build intents
        intent = IntentBuilder("StartApollo11Intent"). \
            require("StartKeyword"). \
            require("GameKeyword").build()
        self.register_intent(intent, self.handle_start_intent)

        intent = IntentBuilder("StopApollo11Intent"). \
            require("StopKeyword"). \
            require("GameKeyword").build()
        self.register_intent(intent, self.handle_stop_intent)

        # 1
        intent = IntentBuilder("Yes1Apollo11Intent"). \
            require("yesKeyword").build()
        self.register_intent(intent, self.handle_yes1)

        intent = IntentBuilder("Yes2Apollo11Intent"). \
            require("yesKeyword").build()
        self.register_intent(intent, self.handle_yes2)

        # 2
        intent = IntentBuilder("No1Apollo11Intent"). \
            require("noKeyword").build()
        self.register_intent(intent, self.handle_no1)

        intent = IntentBuilder("No2Apollo11Intent"). \
            require("noKeyword").build()
        self.register_intent(intent, self.handle_no2)

        # 3
        intent = IntentBuilder("WarmApollo11Intent"). \
            require("warmKeyword").build()
        self.register_intent(intent, self.handle_warm)

        intent = IntentBuilder("HarshApollo11Intent"). \
            require("harshKeyword").build()
        self.register_intent(intent, self.handle_harsh)

        intent = IntentBuilder("NoAnswerApollo11Intent"). \
            require("silentKeyword").build()
        self.register_intent(intent, self.handle_silence)

        # 4
        intent = IntentBuilder("SurvivalApollo11Intent"). \
            require("survivalKeyword").build()
        self.register_intent(intent, self.handle_percentage)
        intent = IntentBuilder("BadSpeechApollo11Intent"). \
            require("speechKeyword").build()
        self.register_intent(intent, self.handle_terrible)
        intent = IntentBuilder("LetsDoItApollo11Intent"). \
            require("dothisKeyword").build()
        self.register_intent(intent, self.handle_lets_do_this)

        # 5
        intent = IntentBuilder("BoardApollo11Intent"). \
            require("boardKeyword").build()
        self.register_intent(intent, self.handle_board)

        intent = IntentBuilder("SuitApollo11Intent"). \
            require("spacesuitKeyword").build()
        self.register_intent(intent, self.handle_body_suit)

        intent = IntentBuilder("HelmetApollo11Intent"). \
            require("helmetKeyword").build()
        self.register_intent(intent, self.handle_helmet)

        intent = IntentBuilder("GlovesApollo11Intent"). \
            require("glovesKeyword").build()
        self.register_intent(intent, self.handle_gloves)

        intent = IntentBuilder("BootsApollo11Intent"). \
            require("bootsKeyword").build()
        self.register_intent(intent, self.handle_boots)

        # 6
        intent = IntentBuilder("ExamineApollo11Intent"). \
            require("examineKeyword").build()
        self.register_intent(intent, self.handle_examine)

        intent = IntentBuilder("IgnoreApollo11Intent"). \
            require("ignoreKeyword").build()
        self.register_intent(intent, self.handle_ignore)

        # 7
        intent = IntentBuilder("EvacuateApollo11Intent"). \
            require("evacuateKeyword").build()
        self.register_intent(intent, self.handle_evacuate)

        intent = IntentBuilder("StayApollo11Intent"). \
            require("stayKeyword").build()
        self.register_intent(intent, self.handle_stay)

        # 8
        intent = IntentBuilder("CodeResetApollo11Intent"). \
            require("CodeResetKeyword").build()
        self.register_intent(intent, self.handle_reset_code)

        # 9
        intent = IntentBuilder("LandApollo11Intent"). \
            require("landKeyword").build()
        self.register_intent(intent, self.handle_land)

        intent = IntentBuilder("OrbitApollo11Intent"). \
            require("orbitKeyword").build()
        self.register_intent(intent, self.handle_orbit)

        # 10
        intent = IntentBuilder("ColinYesApollo11Intent"). \
            require("yesKeyword").build()
        self.register_intent(intent, self.handle_orbit_yes)

        intent = IntentBuilder("ColinNoApollo11Intent"). \
            require("noKeyword").build()
        self.register_intent(intent, self.handle_orbit_no)

        # 11
        intent = IntentBuilder("AbortLandingApollo11Intent"). \
            require("abortKeyword").build()
        self.register_intent(intent, self.handle_abort)

        intent = IntentBuilder("IgnoreLandingApollo11Intent"). \
            require("ignoreKeyword").build()
        self.register_intent(intent, self.handle_ignore_alarm)

        # 12
        intent = IntentBuilder("PencilNoApollo11Intent"). \
            require("noKeyword").build()
        self.register_intent(intent, self.handle_pencil_yes)
        intent = IntentBuilder("PencilYesApollo11Intent"). \
            require("yesKeyword").build()
        self.register_intent(intent, self.handle_pencil_yes)

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
        self.speak_dialog("briefing_harsh")
        self.briefing_question2()

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
        self.speak_dialog("moon_stay", expect_response=True)
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


class IntentParser(object):
    def __init__(self, emitter, time_out=5):
        self.emitter = emitter
        self.time_out = time_out
        self.waiting = False
        self.skills_map = {}
        self.intent_map = {}
        self.intent_data = {}
        self.emitter.on("mycroft.intent.manifest.response",
                        self._handle_receive_intents)
        self.emitter.on("mycroft.skills.manifest.response",
                        self._handle_receive_skills)
        self.emitter.on("mycroft.intent.response",
                        self._handle_receive_intent)
        self.emitter.emit(Message("mycroft.skills.manifest"))
        self.emitter.emit(Message("mycroft.intent.manifest"))

    def get_skill_manifest(self):
        self.update_skill_manifest()
        return self.skills_map

    def get_intent_manifest(self):
        self.update_intent_manifest()
        return self.intent_map

    def determine_intent(self, utterance, lang="en-us"):
        self.waiting = True
        self.emitter.emit(Message("mycroft.intent.get", {"utterance": utterance, "lang": lang}))
        start_time = time()
        t = 0
        while self.waiting and t < self.time_out:
            t = time() - start_time
        if self.waiting:
            return None, None
        id, intent = self.intent_data["type"].split(":")
        return intent, id

    def update_intent_manifest(self):
        # update skill manifest
        self.waiting = True
        self.id = 0
        self.emitter.emit(Message("mycroft.intent.manifest"))
        start_time = time()
        t = 0
        while self.waiting and t < self.time_out:
            t = time() - start_time
        if self.waiting:
            self.waiting = False
            return False
        return True

    def update_skill_manifest(self):
        # update skill manifest
        self.waiting = True
        self.id = 0
        self.emitter.emit(Message("mycroft.skills.manifest"))
        start_time = time()
        t = 0
        while self.waiting and t < self.time_out:
            t = time() - start_time
        if self.waiting:
            self.waiting = False
            return False
        return True

    def get_skill_id(self, intent_name):
        self.update_intent_manifest()
        for skill_id in self.intent_map:
            intents = self.intent_map[skill_id]
            if intent_name in intents:
                return skill_id
        return None

    def _handle_receive_intent(self, message):
        self.intent_data = message.data.get("intent_data", {})
        self.waiting = False

    def _handle_receive_intents(self, message):
        self.intent_map = message.data
        self.waiting = False

    def _handle_receive_skills(self, message):
        self.skills_map = message.data
        self.waiting = False


class IntentLayers(object):
    def __init__(self, emitter, layers=None):
        layers = layers or []
        self.emitter = emitter
        # make intent levels for N layers
        self.layers = layers
        self.current_layer = 0
        self.activate_layer(0)

    def disable_intent(self, intent_name):
        """Disable a registered intent"""
        self.emitter.emit(Message("disable_intent", {"intent_name": intent_name}))

    def enable_intent(self, intent_name):
        """Reenable a registered self intent"""
        self.emitter.emit(Message("enable_intent", {"intent_name": intent_name}))

    def reset(self):
        LOG.info("Reseting Intent Layers")
        self.activate_layer(0)

    def next(self):
        LOG.info("Going to next Intent Layer")
        self.current_layer += 1
        if self.current_layer > len(self.layers):
            LOG.info("Already in last layer, going to layer 0")
            self.current_layer = 0
        self.activate_layer(self.current_layer)

    def previous(self):
        LOG.info("Going to previous Intent Layer")
        self.current_layer -= 1
        if self.current_layer < 0:
            self.current_layer = len(self.layers)
            LOG.info("Already in layer 0, going to last layer")
        self.activate_layer(self.current_layer)

    def add_layer(self, intent_list=None):
        intent_list = intent_list or []
        self.layers.append(intent_list)
        LOG.info("Adding intent layer: " + str(intent_list))

    def replace_layer(self, layer_num, intent_list=None):
        intent_list = intent_list or []
        self.layers[layer_num] = intent_list
        LOG.info("Adding layer" + str(intent_list) + " in position " + str(layer_num))

    def remove_layer(self, layer_num):
        if layer_num >= len(self.layers):
            return False
        self.layers.pop(layer_num)
        LOG.info("Removing layer number " + str(layer_num))
        return True

    def find_layer(self, intent_name):
        layer_list = []
        for i in range(0, len(self.layers)):
            if intent_name in self.layers[i]:
                layer_list.append(i)
        return layer_list

    def disable(self):
        LOG.info("Disabling layers")
        # disable all layers
        for i in range(0, len(self.layers)):
            self.deactivate_layer(i)

    def activate_layer(self, layer_num):
        # error check
        if layer_num < 0 or layer_num > len(self.layers):
            LOG.error("invalid layer number")
            return False

        self.current_layer = layer_num

        # disable other layers
        self.disable()

        # TODO in here we should wait for all intents to be detached
        # sometimes detach intent from this step comes after register from next
        sleep(0.3)

        # enable layer
        LOG.info("Activating Layer " + str(layer_num))
        for intent_name in self.layers[layer_num]:
            self.enable_intent(intent_name)
        return True

    def deactivate_layer(self, layer_num):
        # error check
        if layer_num < 0 or layer_num > len(self.layers):
            LOG.error("invalid layer number")
            return False
        LOG.info("Deactivating Layer " + str(layer_num))
        for intent_name in self.layers[layer_num]:
            self.disable_intent(intent_name)
        return True
