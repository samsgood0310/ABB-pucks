import configparser

"""Testing file for updating the *.ini file if needed. Same method can be used in the main functions/program"""

config = configparser.ConfigParser()
config.read('exposure.ini')
cfgfile = open('exposure.ini', 'w')

# Updating the value for exposure
config.set('EXPOSURE', 'exposure', '40')

# Updating the value for focus
config.set('FOCUS', 'focus', '40')

config.write(cfgfile)
cfgfile.close()
