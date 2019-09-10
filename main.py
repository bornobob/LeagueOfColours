from colorwheel import ColourWheel
from champions import ChampionList

CHAMPION_FILE = r'dragontail-9.17.1\9.17.1\data\en_GB\championFull.json'
SKIN_DIRECTORY = r'dragontail-9.17.1\img\champion'

if __name__ == '__main__':
    champ_list = ChampionList(CHAMPION_FILE)
    champ_list.add_champion_filter('a', exact=False)  # starting with 'a'
    champ_list.add_skin_filter('star', exact=False)  # containg 'star'

    colorwheel = ColourWheel(SKIN_DIRECTORY)
    # 'average' instead of 'common' for the average colour instead of the most frequent one
    colorwheel.add_data(champ_list.get_filtered_skins(), method='common')
    colorwheel.show_plot()
    # colorwheel.save_plot('a - star.jpg')
