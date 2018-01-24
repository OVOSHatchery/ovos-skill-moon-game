from mycroft.util.log import LOG
from mycroft.messagebus.message import Message

from time import time, sleep

__author__ = 'jarbas'


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
