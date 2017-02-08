import sys
sys.path.append('..')
from kiperserver import *
import time

def before_all(context):
    context.server = KiperServer()


def after_all(context):
    context.server.shutdown()
    time.sleep(10)
