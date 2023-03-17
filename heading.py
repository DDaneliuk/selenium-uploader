import os
import sys

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def heading():
    os.system("clear||cls")
    spaces = " " * 98
    sys.stdout.write(GREEN + spaces + """
    █ █       █ █   █ █ █ █ █ █   █ █ █ █ █ █
    █ █ █     █ █   █ █               █ █
    █ █  █    █ █   █ █               █ █
    █ █   █   █ █   █ █ █ █ █         █ █
    █ █     █ █ █   █ █               █ █
    █ █       █ █   █ █               █ █
    """ + END + BLUE +
    '\n' + '{}Upload your awesome nft collection faster{}'.format(BLUE, END).center(60) + '\n' + "")