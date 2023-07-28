"""Class to process regions names."""
import pandas as pd
import yaml
import re


class ObjectInfo:
    """
    Find rows on xlsx sheet where data about specific region is available.
    """
    def __init__(self, data: pd.DataFrame, region_dict: str):
        """
        Itialize class to find rows with region.
        :param data: DataFrame with data from some xlsx file sheet.
        :param region_dict: Read special dictionary with regions and other info.
        """
        self.objects = None
        yaml_file = open(region_dict, 'r', encoding="utf8")
        self.full_description = yaml.load(yaml_file, Loader=yaml.FullLoader)
        self.data = data

    def compare_etalon(self):
        """
        Find start and end rows with information about regions (Российиская Федерация - Чукотский автономный округ).
        Compare name with etalon name, and parse if all is okay. If region with parsed named from xlsx can't be find
        it dictionary "Region was not found" error is raised. Name that can't be find is printed. You can check it and
        add some specific alternative names to region dictionary (alternative_name) attribute.
        :return:
        """
        first_column = self.data.iloc[:, 0].apply(lambda x: ' '.join(x.split()) if not pd.isna(x) else x)

        text_to_find = "Российская Федерация"
        matching_rows = first_column.str.contains(text_to_find).fillna(False)
        index_start = matching_rows[matching_rows].index.tolist()[0] # Нашли строку, в которой данные про РФ

        text_to_find = "Чукотский автономный округ"
        matching_rows = first_column.str.contains(text_to_find).fillna(False)
        index_end = matching_rows[matching_rows].index.tolist()[0] # Нашли строку, в которой данные про Чукотский АО

        object_indexes = {}

        for i in range(index_start, index_end):
            if 'в том числе:' in first_column[i]:
                pass
            else:
                if 'Российская Федерация' in first_column[i]:
                    object_indexes['Российская Федерация'] = ['страна', '00000000', '00000000', i]
                else:

                    reg_name = first_column[i].replace('p', 'р').replace('o', 'о').replace(';', '').strip()
                    reg_name = re.sub(r'\d+[)]', '', reg_name)
                    for j in self.full_description['dict']:
                        if (reg_name == self.full_description['dict'][j]['name_rus']) or \
                                reg_name in self.full_description['dict'][j]['alternative_name']:

                            object_indexes[self.full_description['dict'][j]['name_rus']] = [self.full_description['dict'][j]['level'],
                                                                                            self.full_description['dict'][j]['oktmo'],
                                                                                            self.full_description['dict'][j]['okato'], i]
                            if reg_name in self.full_description['dict'][j]['alternative_name']:
                                reg_name = self.full_description['dict'][j]['name_rus']

                    if reg_name not in object_indexes.keys():
                        print(reg_name)
                        raise ValueError("Region was not found")

        self.objects = object_indexes
        return self.objects


if __name__ == '__main__':
    pass
