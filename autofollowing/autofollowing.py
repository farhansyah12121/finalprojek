import getpass
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

def initial_checker():
    files = [hashtag_file, users_file, whitelist, blacklist, setting]
    try:
        for f in files:
            with open(f, 'r') as f:
                pass
    except BaseException:
        for f in files:
            with open(f, 'w') as f:
                pass
        print("""
        Welcome to instabot, it seems this is the first time you've used this bot.
        Before starting, let's setup the basics.
        So the bot functions the way you want.
        """)
        setting_input()
        print("""
        You can add hashtag database, competitor database,
        whitelists, blacklists and also add users in setting menu.
        Have fun with the bot!
        """)
        time.sleep(5)
        os.system('cls')

# setting function start here
def setting_input():
    inputs = [("How many follows do you want to do in a day? ", 350),
              ("How about unfollow? ", 350),
              (("Maximal followers of account you want to follow?\n"
                "We will skip media that have greater followers than this value "), 2000),
              (("Minimum followers a account should have before we follow?\n"
                "We will skip media that have lesser followers than this value "), 10),
              (("Maximum following of account you want to follow?\n"
                "We will skip media that have a greater following than this value "), 7500),
              (("Minimum following of account you want to follow?\n"
                "We will skip media that have lesser following from this value "), 10),
              ("Maximal followers to following_ratio ", 10),
              ("Maximal following to followers_ratio ", 2),
              ("Delay from one follow to another follow you will perform ", 30),
              ("Delay from one unfollow to another unfollow you will perform ", 30)]

    with open(setting, "w") as f:
        while True:
            for msg, n in inputs:
                read_input(f, msg, n)
            break
        print("Done with all settings!")

def parameter_setting():
    settings = ["Max follows per day: ",
                "Max unfollows per day: ",
                "Max followers to follow: ",
                "Min followers to follow: ",
                "Max following to follow: ",
                "Min following to follow: ",
                "Max followers to following_ratio: ",
                "Max following to followers_ratio: ",
                "Follow delay: ",
                "Unfollow delay: ",]


    with open(setting) as f:
        data = f.readlines()

    print("Current parameters\n")
    for s, d in zip(settings, data):
        print(s + d)
              

def username_adder():
    with open(SECRET_FILE, "a") as f:
        print("We will add your instagram account.")
        print("Don't worry. It will be stored locally.")
        while True:
            print("Enter your login: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            print("Enter your password: (it will not be shown due to security reasons - just start typing and press Enter)")
            f.write(getpass.getpass() + "\n")
            print("Do you want to add another account? (y/n)")
            if "y" not in sys.stdin.readline():
                break


def get_adder(name, fname):
    def _adder():
        print("Current Database:")
        print(bot.read_list_from_file(fname))
        with open(fname, "a") as f:
            print('Add {} to database'.format(name))
            while True:
                print("Enter {}: ".format(name))
                f.write(str(sys.stdin.readline().strip()) + "\n")
                print("Do you want to add another {}? (y/n)\n".format(name))
                if "y" not in sys.stdin.readline():
                    print('Done adding {}s to database'.format(name))
                    break
    return _adder()

def hashtag_adder():
    return get_adder('hashtag', fname=hashtag_file)


def competitor_adder():
    return get_adder('username', fname=users_file)


def blacklist_adder():
    return get_adder('username', fname=blacklist)


def whitelist_adder():
    return get_adder('username', fname=whitelist)


def userlist_maker():
    return get_adder('username', userlist)

def menu():
    ans = True
    while ans:
        print("""
        1. Follow from hashtag
        2. Follow followers
        3. Follow following
        4. Follow by likes on media
        5. Main menu
        """)
        ans = input("How do you want to follow?\n").strip()

        if ans == "1":
            print("""
            1.Insert hashtag
            2.Use hashtag database
            """)
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = input("Insert hashtags separated by spaces\nExample: cat dog\nwhat hashtags?\n").strip().split(' ')
            else:
                hashtags = bot.read_list_from_file(hashtag_file)
            for hashtag in hashtags:
                print("Begin following: " + hashtag)
                users = bot.get_hashtag_users(hashtag)
                bot.follow_users(users)
            menu()

        elif ans == "2":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_followers(user_id)
            menu()

        elif ans == "3":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_following(user_id)
            menu()

        elif ans == "4":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.follow(liker)

        elif ans == "5":
            menu()

        else:
            print("This number is not in the list?")
            menu()


def menu_unfollow():
    ans = True
    while ans:
        print("""
        1. Unfollow non followers
        2. Unfollow everyone
        3. Main menu
        """)
        ans = input("How do you want to unfollow?\n").strip()

        if ans == "1":
            bot.unfollow_non_followers()
            menu_unfollow()

        elif ans == "2":
            bot.unfollow_everyone()
            menu_unfollow()

        elif ans == "3":
            menu()

        else:
            print("This number is not in the list?")
            menu_unfollow()


def menu_setting():
    ans = True
    while ans:
        print("""
        1. Setting bot parameter
        2. Add user accounts
        3. Add competitor database
        4. Add hashtag database
        5. Add blacklist
        6. Add whitelist
        7. Clear all database
        8. Main menu
        """)
        ans = input("What setting do you need?\n").strip()

        if ans == "1":
            parameter_setting()
            change = input("Want to change it? y/n\n").strip()
            if change == 'y' or change == 'Y':
                setting_input()
            else:
                menu_setting()
        elif ans == "2":
            username_adder()
        elif ans == "3":
            competitor_adder()
        elif ans == "4":
            hashtag_adder()
        elif ans == "5":
            blacklist_adder()
        elif ans == "6":
            whitelist_adder()
        elif ans == "7":
            print(
                "Whis will clear all database except your user accounts and paramater settings")
            time.sleep(5)
            open(hashtag_file, 'w')
            open(users_file, 'w')
            open(whitelist, 'w')
            open(blacklist, 'w')
            print("Done, you can add new one!")
        elif ans == "8":
            menu()
        else:
            print("This number is not in the list?")
            menu_setting()


# for input compability
try:
    input = raw_input
except NameError:
    pass

# files location
hashtag_file = "hashtagsdb.txt"
users_file = "usersdb.txt"
whitelist = "whitelist.txt"
blacklist = "blacklist.txt"
userlist = "userlist.txt"
setting = "setting.txt"
SECRET_FILE = "secret.txt"

# check setting first
initial_checker()

if os.stat(setting).st_size == 0:
    print("Looks like setting are broken")
    print("Let's make new one")
    setting_input()

f = open(setting)
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())
setting_8 = int(lines[8].strip())
setting_9 = int(lines[9].strip())
setting_10 = int(lines[10].strip())

bot = Bot(
    max_follows_per_day=setting_0,
    max_unfollows_per_day=setting_1,
    max_followers_to_follow=setting_2,
    min_followers_to_follow=setting_3,
    max_following_to_follow=setting_4,
    min_following_to_follow=setting_5,
    max_followers_to_following_ratio=setting_6,
    max_following_to_followers_ratio=setting_7,
    follow_delay=setting_8,
    unfollow_delay=setting_9,
    whitelist_file=whitelist,
    blacklist_file=blacklist,
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'doodleartindonesia',
        'doodle art indonesia',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("error, read exception bellow")
        bot.logger.info(str(e))
    time.sleep(1)
