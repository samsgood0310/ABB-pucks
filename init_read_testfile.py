import configparser

"""Testing file for reading the *.ini file if needed. Same method can be used in the main functions/program"""

config = configparser.ConfigParser()
config.read('exposure.ini')

for key in config['EXPOSURE']:
    print(key)

print(config['EXPOSURE']['exposure'])
