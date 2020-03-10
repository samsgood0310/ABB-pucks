import configparser

"""Testing file for initializing values for the *.ini files. Method can be used in other configuration files to save
values to """

configfile_name = "exposure.ini"

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
