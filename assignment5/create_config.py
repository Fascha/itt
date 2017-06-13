import configparser
import random


config = configparser.ConfigParser()

number_participants = 4
number_repetitions = 4
distances = ['50', '150', '250', '350']
widths = ['16', '32', '16', '32']

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
for i in range(number_participants):
    combinations = []
    for w in widths:
        for d in distances:
            combinations.append((w, d))
    random.shuffle(combinations)

    """

    COUNTER BALANCING


    """

    temp_widths = [w[0] for w in combinations]
    temp_distances = [d[1] for d in combinations]

    widths_string = ', '.join(temp_widths)
    distances_string = ', '.join(temp_distances)

    config['POINTING EXPERIMENT'] = {'USER': str(i),
                                     'WIDTHS': widths_string,
                                     'DISTANCES': distances_string,
                                     'CURSOR_START_X': int(WINDOW_WIDTH/2),
                                     'CURSOR_START_Y': int(WINDOW_HEIGHT/2),
                                     'WINDOW_WIDTH': int(WINDOW_WIDTH),
                                     'WINDOW_HEIGHT': int(WINDOW_HEIGHT)}

    """

    random.shuffle(distances)
    distances_string = ', '.join(distances)
    config['POINTING EXPERIMENT']['DISTANCES'] = str(distances_string)
    random.shuffle(widths)
    widths_string = ', '.join(widths)
    config['POINTING EXPERIMENT']['WIDTHS'] = str(widths_string)


    config['POINTING EXPERIMENT'] = {'USER': str(i),
                                 'WIDTHS': '30, 50, 60, 70',
                                 'DISTANCES': '100, 200, 300, 400',
                                 'WINDOW_WIDTH': 800,
                                 'WINDOW_HEIGHT': 800}


    """

    with open('config_' + str(i) + '.ini', 'w') as configfile:
        config.write(configfile)
