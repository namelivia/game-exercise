from client.screen_manager import ScreenManager
from client.profile import Profile
import pickle


def get_new_name():
    profile = Profile(input('Enter your name:'))
    pickle.dump(profile, open("client_data/profile", "wb"))
    return profile


if __name__ == "__main__":
    try:
        profile = pickle.load(open("client_data/profile", "rb"))
    except FileNotFoundError:
        profile = get_new_name()
    screen_manager = ScreenManager(profile)
    while True:
        screen_manager.run()
