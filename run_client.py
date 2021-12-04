from client.screen_manager import ScreenManager
from client.profile.profile import Profile
from client.persistence.persistence import Peristence
from client.profile.factory import Factory


def _get_new_profile() -> Profile:
    name = input('Enter your name:')
    profile = Factory.new_profile(name)
    Peristence.save(profile)
    return profile


def _initialize_status() -> Profile:
    try:
        return Peristence.load()
    except FileNotFoundError:
        return _get_new_profile()


if __name__ == "__main__":
    profile = _initialize_status()
    screen_manager = ScreenManager(profile)
    while True:
        screen_manager.run()
