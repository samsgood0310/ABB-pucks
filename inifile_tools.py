import configparser

"""Testing file for reading the *.ini file if needed. Same method can be used in the main functions/program"""

config = configparser.ConfigParser()
config.read('cam_adjustments.ini')

for key in config['EXPOSURE']:
    print(key)

print(config['EXPOSURE']['exposure'])


import configparser

"""Testing file for updating the *.ini file if needed. Same method can be used in the main functions/program"""

config = configparser.ConfigParser()
config.read('cam_adjustments.ini')
cfgfile = open('cam_adjustments.ini', 'w')

# Updating the value for exposure
config.set('EXPOSURE', 'exposure', '40')

# Updating the value for focus
config.set('FOCUS', 'focus', '40')

config.write(cfgfile)
cfgfile.close()




import configparser

"""Testing file for initializing values for the *.ini files. Method can be used in other configuration files to save
values to """

configfile_name = "cam_adjustments.ini"

# Create the configuration file as it doesn't exist yet
cfgfile = open(configfile_name, 'w')

# Add content to the file
Config = configparser.ConfigParser()
Config.add_section('EXPOSURE')
Config.set('EXPOSURE', 'exposure', '35')
Config.add_section('FOCUS')
Config.set('FOCUS', 'focus', '36')
Config.add_section('SLOPEX')
Config.set('SLOPEX', 'slopex', '100')
Config.add_section('SLOPEY')
Config.set('SLOPEY', 'slopey', '500')

Config.write(cfgfile)
cfgfile.close()