import numpy as np
from effects.template_voice import BaseVoiceEffect

class LoopVoiceEffect(BaseVoiceEffect):
    def process_audio(self, data):

        return

    def start(self):
        super().start()
        print("Effet Loop démarré.")

    def stop(self):
        super().stop()
        print("Effet Loop arrêté.")
