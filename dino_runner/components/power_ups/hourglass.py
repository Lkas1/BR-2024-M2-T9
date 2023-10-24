from dino_runner.utils.constants import HOURGLASS, HOURGLASS_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Hourglass(PowerUp):
    def __init__(self):
        self.image = HOURGLASS
        self.type = HOURGLASS_TYPE
        super().__init__(self.image, self.type)