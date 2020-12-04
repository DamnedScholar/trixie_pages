from sockpuppet.reflex import Reflex


class Trix_Or_TreatReflex(Reflex):
    def increment(self, step=1):
        self.count = int(self.element.dataset['count']) + step
