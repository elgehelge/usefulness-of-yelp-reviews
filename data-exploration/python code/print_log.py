from time import gmtime, strftime

logging = False

def logging(boolean):
    logging = boolean

def log(text):
    if logging:
        print strftime("%H:%M:%S", gmtime()) + ' : ' + text
