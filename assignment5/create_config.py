import configparser
import random


config = configparser.ConfigParser()

number_participants = 4
number_repetitions = 4
distances = ['50', '150', '250', '350']
widths = ['15', '30']
widths.extend(widths)

for i in range(number_participants):

    config['POINTING EXPERIMENT'] = {'USER': 1,
                                 'WIDTHS': '30, 50, 60, 70',
                                 'DISTANCES': '100, 200, 300, 400',
                                 'WINDOW_WIDTH': 800,
                                 'WINDOW_HEIGHT': 800}

    config['POINTING EXPERIMENT']['USER'] = str(i)

    random.shuffle(distances)
    distances_string = ', '.join(distances)
    config['POINTING EXPERIMENT']['DISTANCES'] = str(distances_string)
    random.shuffle(widths)
    widths_string = ', '.join(widths)
    config['POINTING EXPERIMENT']['WIDTHS'] = str(widths_string)


    with open('config_' + str(i) + '.ini', 'w') as configfile:
        config.write(configfile)
