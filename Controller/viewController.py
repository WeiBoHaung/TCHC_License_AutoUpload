import os,sys
import time
from datetime import date, datetime
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from View.noname import mainFrame as mf

class App:
    def __init__( self ):
        self.wd = os.getcwd()


if __name__ == '__main__':
    xxx=App()
    print(xxx.wd)