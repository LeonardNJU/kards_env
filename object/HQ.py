from utils.symbols import Nation
from object.object import Object

class HQ(Object):
    def __init__(self, host:Nation, HP: int=20):
        super().__init__(host.name, HP)