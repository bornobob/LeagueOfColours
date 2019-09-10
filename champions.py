from json import loads
from os import path


class NameKey:
    def __init__(self, name, key):
        """
        Simple Name-Key class
        :param name: name of the instance
        :param key: key of the instance
        """
        self.name = name
        self.key = key


class Champion(NameKey):
    def __init__(self, name, key):
        """
        Champion class to save various champion data like name, key and skins
        :param name: name of the champion
        :param key: key of the champion
        """
        super().__init__(name, key)
        self.skins = []

    def add_skin(self, skin):
        """
        Adds a Skin instance to the champion's skins
        :param skin: the skin to add
        """
        self.skins.append(skin)

    def __str__(self):
        """
        Gives a full string representation of the champion
        """
        return '{0.name} ({0.key}):\n - {1}'.format(self, '\n - '.join(str(x) for x in self.skins))


class Skin(NameKey):
    def __init__(self, name, key, champion_id):
        """
        Skin class to save various skin data like name, key and the filename
        :param name: name of the skin
        :param key: key of the skin
        :param champion_id: champion id
        """
        super().__init__(name, key)
        self.filename = '{}_{}.jpg'.format(champion_id, key)

    def get_file_path(self, base_path, image_type='loading'):
        """
        Gets the file path used to retrieve images of a skin.
        Output will be in the form of '[base_path]/[image_type]/[champion_id]_[key].jpg'
        :param base_path: the base path of the location of the images
        :param image_type: image type is most likely either 'loading' or 'tiles' for loading screen image or tile image
        """
        return path.join(base_path, image_type, self.filename)

    def __str__(self):
        """
        String representation of name and key info
        """
        return '{0.name} ({0.key})'.format(self)


class ChampionList:
    def __init__(self, champion_data_file):
        """
        ChampionList is a class to ease the filtering process.
        :param champion_data_file: the path to the 'championFull.json' file
        """
        self.all_champions = self.get_champ_list(champion_data_file)
        self.filtered_champions = list(self.all_champions)

    @staticmethod
    def get_champ_data(champ_data_file):
        """
        Static method that reads the championFull.json file and parses the json.
        :param champ_data_file: the path to the 'championFull.json' file
        :return: dictionary of the champion data
        """
        with open(champ_data_file, 'r', encoding='utf8') as f:
            data = loads(f.read())
        return data

    @staticmethod
    def get_champ_list(champ_data_file):
        """
        Creates a list of Champion instances, also fills the Skin data.
        :param champ_data_file: the path to the 'championFull.json' file
        :return: a list of Champion instances
        """
        data = ChampionList.get_champ_data(champ_data_file)
        champ_list = []
        for champion_data in data['data'].values():
            champ = Champion(champion_data['name'], champion_data['key'])
            for skin_data in champion_data['skins']:
                champ.add_skin(Skin(skin_data['name'], skin_data['num'], champion_data['id']))
            champ_list.append(champ)
        return champ_list

    def get_filtered_skins(self):
        """
        Returns the skins in the filtered_champions
        """
        return sum([x.skins for x in self.filtered_champions], [])

    def add_skin_filter(self, filter_word, exact=False):
        """
        Adds a skin filter.
        Skin filters work by looking if the filter_word is in the skin name.
        Not case sensitive.
        :param filter_word: the filter word to filter by
        :param exact: if the name should be an exact (non case sensitive) match
        """
        for champ in self.filtered_champions:
            for skin in list(champ.skins):
                if (exact and skin.name.lower() != filter_word.lower()) or \
                   (not exact and filter_word.lower() not in skin.name.lower()):
                    champ.skins.remove(skin)

    def add_champion_filter(self, filter_word, exact=True):
        """
        Adds a champion filter.
        Champion filters work by looking if the name of the champion starts with the filter_word.
        Not case sensitive.
        :param filter_word: the filter word to filter by
        :param exact: if the name should be an exact (non case sensitive) match
        """
        for champ in list(self.filtered_champions):
            if (exact and not champ.name.lower() == filter_word.lower()) or \
               (not exact and not champ.name.lower().startswith(filter_word.lower())):
                self.filtered_champions.remove(champ)
