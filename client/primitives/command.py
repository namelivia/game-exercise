from abc import ABC


class Command(ABC):

    def __init__(self, profile, description):
        self.description = description
        self.profile = profile

    def execute():
        pass
