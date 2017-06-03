import configparser


config = configparser.ConfigParser()

config['POINTING EXPERIMENT'] = {'USER': 1,
                                 'WIDTHS': '30, 50, 60, 70',
                                 'DISTANCES': '100, 200, 300, 400'}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
