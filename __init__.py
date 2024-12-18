import os.path
from typing import List

from ovos_number_parser import extract_number
from ovos_workshop.decorators import layer_intent, enables_layer, disables_layer, resets_layers
from ovos_workshop.intents import IntentBuilder
from ovos_workshop.skills.game_skill import ConversationalGameSkill


class Apollo11GameSkill(ConversationalGameSkill):

    def __init__(self, *args, **kwargs):
        img = os.path.join(os.path.dirname(__file__), "res", "img.png")
        icon = os.path.join(os.path.dirname(__file__), "res", "img_small.png")
        super().__init__(skill_voc_filename="MoonGameKeyword",
                         skill_icon=icon, game_image=img,
                         *args, **kwargs)
        self.equipped = []
        self.entries = 0
        self.current_question = 0
        self.sanity = 0
        self.entered_code = []
        self.code = ["9", "0", "2", "1", "0"]

    def initialize(self):
        # start with all game states disabled
        self.intent_layers.disable()

    @property
    def items(self) -> List[str]:
        # it's a property to ensure language matches session
        # self.resources is lang aware
        return (self.resources.load_list_file("items") or
                ["gloves", "boots", "helmet", "body suit"])

    @property
    def questions(self) -> List[str]:
        # it's a property to ensure language matches session
        # self.resources is lang aware
        return self.resources.load_list_file("questions") or [
            "Do you like me?",
            "Do you think we'll survive?",
            "Do you trust the team?",
            "Does mission control have confidence in us?",
            "Do you think we aren't alone in the universe",
            "Am I going to die on this trip?"
        ]

    #####################################################################
    # abstract methods from base class that every game needs to implement
    def on_play_game(self):
        if not self.is_playing:
            self.speak_dialog("start.game")
            self.handle_intro()
        else:
            self.speak_dialog("already.started")

    def on_abandon_game(self):
        self.log.debug("game abandoned! skill kicked out of active skill list!!!")
        self.handle_game_over()

    def on_stop_game(self):
        self.handle_game_over()

    def on_game_command(self, utterance: str, lang: str):
        """pipe user input that wasnt caught by intents to the game
        do any intent matching or normalization here
        don't forget to self.speak the game output too!
        """
        self.log.debug("Skill intents wont trigger, handle game action in converse")

        # take corrective action when no intent matched
        if self.intent_layers.is_active("guard") or \
                self.intent_layers.is_active("guard2"):
            self.speak_dialog("guard_dead")
            self.handle_game_over()
        elif self.intent_layers.is_active("briefing"):
            self.speak_dialog("briefing_other")
            self.briefing_question2()
        elif self.intent_layers.is_active("briefing2"):
            self.suit_up()
        elif self.intent_layers.is_active("suit_up"):
            self.handle_board()
        elif self.intent_layers.is_active("boarding"):
            self.speak_dialog("boarding_dead")
            self.handle_game_over()
        elif self.intent_layers.is_active("evacuation"):
            self.speak_dialog("evacuate_dead")
            self.handle_game_over()
        elif self.intent_layers.is_active("launch_codes"):
            number = extract_number(utterance, lang=lang)
            if number is not False:
                number = str(int(number))
                if len(number) > 1:
                    self.speak_dialog("code_one_at_time",
                                      expect_response=True)
                elif number.isdigit():
                    self.entered_code.append(number)
                    self.speak_dialog("code_enter_number",
                                      {"number": number},
                                      expect_response=True)
                    if len(self.entered_code) == len(self.code):
                        if self.entered_code == self.code:
                            self.correct_code()
                        else:
                            self.wrong_code()
                else:
                    self.speak_dialog("code_invalid", expect_response=True)
            else:
                self.speak_dialog("code_invalid", expect_response=True)
        elif self.intent_layers.is_active("orbit"):
            self.speak_dialog("colin_other")
            self.next_question()
        else:
            self.speak_dialog("invalid.command", expect_response=True)

    ###############
    # This game is implemented via IntentLayers
    # when no intent matches self.on_game_command is called
    # IntentLayer handlers are defined below
    @enables_layer(layer_name="guard")
    @enables_layer(layer_name="stop_game")
    def handle_intro(self):
        self.speak_dialog("reach_gate")
        self.speak_dialog("guard")
        self.speak_dialog("present_id", expect_response=True)

    @resets_layers()
    def handle_game_over(self):
        self.speak_dialog("stop.game")
        self.equipped = []
        self.entries = 0
        self.sanity = 0
        self.current_question = 0
        self.entered_code = []

    # layer 1
    @layer_intent(IntentBuilder("Yes1Apollo11Intent").
                  require("yesKeyword"),
                  layer_name="guard")
    def handle_yes1(self, message=None):
        self.speak_dialog("guard_yes")
        self.briefing_question1()

    @layer_intent(IntentBuilder("No1Apollo11Intent").
                  require("noKeyword"),
                  layer_name="guard")
    @enables_layer(layer_name="guard2")
    @disables_layer(layer_name="guard")
    def handle_no1(self, message=None):
        self.speak_dialog("guard_no")
        self.speak_dialog("present_id", expect_response=True)

    # layer 2
    @layer_intent(IntentBuilder("Yes2Apollo11Intent").
                  require("yesKeyword"),
                  layer_name="guard2")
    def handle_yes2(self, message=None):
        self.speak_dialog("guard_yes_alternate")
        self.briefing_question1()

    @layer_intent(IntentBuilder("No2Apollo11Intent").
                  require("noKeyword"),
                  layer_name="guard2")
    def handle_no2(self, message=None):
        self.speak_dialog("guard_dead")
        self.handle_game_over()

    @enables_layer(layer_name="briefing")
    @disables_layer(layer_name="guard")
    @disables_layer(layer_name="guard2")
    def briefing_question1(self):
        self.speak_dialog("guard_next")
        self.speak_dialog("briefing")
        self.speak_dialog("briefing_question", expect_response=True)

    # briefing 1 - layer 3
    @layer_intent(IntentBuilder("WarmApollo11Intent").
                  require("warmKeyword"),
                  layer_name="briefing")
    def handle_warm(self, message=None):
        self.speak_dialog("briefing_warm")
        self.briefing_question2()

    @layer_intent(IntentBuilder("HarshApollo11Intent").
                  require("harshKeyword"),
                  layer_name="briefing")
    def handle_harsh(self, message=None):
        self.speak_dialog("briefing_harsh")
        self.briefing_question2()

    @layer_intent(
        IntentBuilder("NoAnswerApollo11Intent").
        require("silentKeyword"),
        layer_name="briefing")
    def handle_silence(self, message=None):
        self.speak_dialog("briefing_silence")
        self.briefing_question2()

    @enables_layer(layer_name="briefing2")
    @disables_layer(layer_name="briefing")
    def briefing_question2(self):
        self.speak_dialog("speech")
        self.speak_dialog("briefing_question2", expect_response=True)

    # briefing 2 - layer 4
    @layer_intent(
        IntentBuilder("SurvivalApollo11Intent").
        require("survivalKeyword"),
        layer_name="briefing2")
    def handle_percentage(self, message=None):
        self.speak_dialog("briefing_percentage")
        self.suit_up()

    @layer_intent(
        IntentBuilder("BadSpeechApollo11Intent").
        require("speechKeyword"),
        layer_name="briefing2")
    def handle_terrible(self, message=None):
        self.speak_dialog("briefing_terrible")
        self.suit_up()

    @layer_intent(
        IntentBuilder("LetsDoItApollo11Intent").
        require("dothisKeyword"),
        layer_name="briefing2")
    def handle_lets_do_this(self, message=None):
        self.speak_dialog("briefing_lets_do_this")
        self.suit_up()

    @enables_layer(layer_name="suit_up")
    @disables_layer(layer_name="briefing2")
    def suit_up(self):
        self.speak_dialog("briefing_end")
        self.speak_dialog("suit_up", expect_response=True)

    # space suit - layer 5
    @layer_intent(IntentBuilder("BoardApollo11Intent").
                  require("boardKeyword"),
                  layer_name="suit_up")
    def handle_board(self, message=None):
        if not self.can_board():
            self.speak_dialog("boarding_fail")
            return
        self.board()

    @layer_intent(
        IntentBuilder("HelmetApollo11Intent").
        require("helmetKeyword"),
        layer_name="suit_up")
    def handle_helmet(self, message=None):
        item = "helmet"
        if item in self.equipped:
            self.speak_dialog("already_equipped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equipped.append(item)
        if self.can_board():
            self.board()

    @layer_intent(IntentBuilder("BootsApollo11Intent").
                  require("bootsKeyword"),
                  layer_name="suit_up")
    def handle_boots(self, message=None):
        item = "boots"
        if item in self.equipped:
            self.speak_dialog("already_equiped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equipped.append(item)
        if self.can_board():
            self.board()

    @layer_intent(
        IntentBuilder("GlovesApollo11Intent").
        require("glovesKeyword"),
        layer_name="suit_up")
    def handle_gloves(self, message=None):
        item = "gloves"
        if item in self.equipped:
            self.speak_dialog("already_equiped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equipped.append(item)
        if self.can_board():
            self.board()

    @layer_intent(
        IntentBuilder("SuitApollo11Intent").
        require("spacesuitKeyword"),
        layer_name="suit_up")
    def handle_body_suit(self, message=None):
        item = "body suit"
        if item in self.equipped:
            self.speak_dialog("already_equiped", {"item": item})
        else:
            self.speak_dialog("equip", {"item": item})
            self.equipped.append(item)
        if self.can_board():
            self.board()

    @enables_layer(layer_name="boarding")
    @disables_layer(layer_name="suit_up")
    def board(self):
        self.speak_dialog("boarding", expect_response=True)

    def can_board(self) -> bool:
        return all(item in self.equipped for item in self.items)

    # board ship - layer 6
    @layer_intent(IntentBuilder("ExamineApollo11Intent").
                  require("examineKeyword"),
                  layer_name="boarding")
    @enables_layer(layer_name="launch_codes")
    @disables_layer(layer_name="boarding")
    def handle_examine(self, message=None):
        self.speak_dialog("examine")
        self.speak_dialog("codes", expect_response=True)

    @layer_intent(
        IntentBuilder("IgnoreApollo11Intent").
        require("ignoreKeyword"),
        layer_name="boarding")
    @enables_layer(layer_name="evacuation")
    @disables_layer(layer_name="boarding")
    def handle_ignore(self, message=None):
        self.speak_dialog("ignore", expect_response=True)

    # evacuation - layer 7
    @layer_intent(IntentBuilder("EvacuateApollo11Intent").
                  require("evacuateKeyword"),
                  layer_name="evacuation")
    def handle_evacuate(self, message=None):
        self.speak_dialog("evacuate_gameover")
        self.handle_game_over()

    @layer_intent(IntentBuilder("StayApollo11Intent").
                  require("stayKeyword"),
                  layer_name="evacuation")
    def handle_stay(self, message=None):
        self.speak_dialog("stay_dead")
        self.handle_game_over()

    # launch codes - layer 8
    @layer_intent(
        IntentBuilder("CodeResetApollo11Intent").
        require("CodeResetKeyword"),
        layer_name="launch_codes")
    def handle_reset_code(self, message=None):
        if self.entries > 3:
            self.speak_dialog("bad.code")
            self.handle_game_over()
        else:
            self.entries -= 1
            self.speak_dialog("code.reset", {"left": 3 - self.entries})
            self.entered_code = []

    @enables_layer("moon")
    @disables_layer("launch_codes")
    def correct_code(self):
        self.speak_dialog("launch")
        self.speak_dialog("moon_landing", expect_response=True)

    def wrong_code(self):
        self.speak_dialog("code_dead")
        self.handle_game_over()

    # moon landing - layer 9
    @layer_intent(IntentBuilder("LandApollo11Intent").
                  require("landKeyword"),
                  layer_name="moon")
    @enables_layer(layer_name="landing")
    @disables_layer(layer_name="moon")
    def handle_land(self, message=None):
        self.speak_dialog("moon_land", expect_response=True)

    @layer_intent(IntentBuilder("OrbitApollo11Intent").
                  require("orbitKeyword"),
                  layer_name="moon")
    @enables_layer(layer_name="orbit")
    @disables_layer(layer_name="moon")
    def handle_orbit(self, message=None):
        self.speak_dialog("moon_stay", expect_response=True)

    # stay on ship - layer 10
    @layer_intent(IntentBuilder("ColinYesApollo11Intent").
                  require("yesKeyword"),
                  layer_name="orbit")
    def handle_orbit_yes(self):
        self.sanity += 1
        self.speak_dialog("colin_yes")
        self.next_question()

    @layer_intent(IntentBuilder("ColinNoApollo11Intent").
                  require("noKeyword"),
                  layer_name="orbit")
    def handle_orbit_no(self):
        self.speak_dialog("colin_no")
        self.next_question()

    def next_question(self):
        if self.current_question == len(self.questions) - 1:
            if self.sanity > 2:
                self.speak_dialog("colin_calm")
                self.speak_dialog("go_home")
                self.handle_game_over()
            else:
                self.speak_dialog("colin_dead")
                self.handle_game_over()
        else:
            self.current_question += 1
            self.speak(self.questions[self.current_question],
                       expect_response=True)

    # land on moon - layer 11
    @layer_intent(IntentBuilder("AbortLandingApollo11Intent").
                  require("abortKeyword"),
                  layer_name="landing")
    @disables_layer(layer_name="landing")
    def handle_abort(self, message=None):
        self.speak_dialog("moon_land_abort", expect_response=True)
        self.handle_game_over()

    @layer_intent(IntentBuilder("IgnoreLandingApollo11Intent").
                  require("ignoreKeyword"),
                  layer_name="landing")
    @enables_layer(layer_name="pencil")
    @disables_layer(layer_name="landing")
    def handle_ignore_alarm(self, message=None):
        self.speak_dialog("moon_land_ignore")
        self.speak_dialog("moon_launch", expect_response=True)

    # moon launch - layer 12
    @layer_intent(
        IntentBuilder("PencilYesApollo11Intent").require("yesKeyword"),
        layer_name="pencil")
    @disables_layer(layer_name="pencil")
    def handle_pencil_yes(self, message=None):
        self.speak_dialog("pencil_yes")
        self.speak_dialog("go_home")
        self.handle_game_over()

    @layer_intent(IntentBuilder("PencilNoApollo11Intent").require("noKeyword"),
                  layer_name="pencil")
    @disables_layer(layer_name="pencil")
    def handle_pencil_no(self, message=None):
        self.speak_dialog("pencil_no")
        self.handle_game_over()
