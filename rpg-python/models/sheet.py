sheet_list = []


def get_last_id():
    if sheet_list:
        last_sheet = sheet_list[-1]
    else:
        return 1
    return last_sheet.id +1


class Sheet:

    def __init__(self, name, race, hp, statistics):
        self.id = get_last_id()
        self.name = name
        self.race = race
        self.hp = hp
        self.statistics = statistics
        self.is_publish = False


    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'race': self.race,
            'hp': self.hp,
            'statistics': self.statistics
        }