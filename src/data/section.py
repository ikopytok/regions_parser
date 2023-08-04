import pandas as pd
from comment import Comment
from indicator import Indicator
from periods import Periods
from objects import ObjectInfo
import re


class Section:
    """Parse data for a give section (xml file)."""
    def __init__(self, source: str, regions_dict: str):
        """
        Initialize class.
        :param source: Path to source file with data about specific section.
        :param regions_dict: Path to reference regions dictionary.
        """
        self.source = source
        self.regions_dict = regions_dict
        self.sheets = self.sheet_names()
        self.data = None

    def sheet_names(self):
        """
        Return list of xlsx file sheets except first sheet.
        :return: List with sheets names.
        """
        return pd.ExcelFile(self.source).sheet_names[1:]

    def process_section(self):
        """
        Process xlsx file sheet by sheet. Save all date to one dataframe.
        :return:
        """
        df = pd.DataFrame()
        for sheet in self.sheets:
            print("Parse list ", sheet, ' of file ', self.source)
            data = self.process_sheet(sheet)
            df = pd.concat([df, pd.DataFrame(data)], axis=0)
        self.data = df
        return df

    @staticmethod
    def skip_value(val):
        if val in ('…', ' - ', '-', ' -', '- ', '...',  '–', '..',
                   '….', '−', '        …', '... ', '...  ', ' ...', '‐'):
            return True
        return False


    def process_sheet(self, sheet_name: str):
        """
        Parse all data from specific xlsx sheet.
        :param sheet_name: Name of sheet to parse.
        :return: Dictionary with indicator values from the sheet and other information.
        """
        result = {'section': [],
                  'indicator_name': [],
                  'indicator_unit': [],
                  'indicator_code': [],
                  'object_name': [],
                  'object_level': [],
                  'object_oktmo': [],
                  'object_okato': [],
                  'year': [],
                  'indicator_value': [],
                  'comment': []}

        df = pd.read_excel(self.source, sheet_name=sheet_name, dtype='string')

        indicator = Indicator(df)
        indicator.find_names()
        print("Section is: ", indicator.section, " Indicator is: ", indicator.name, " Unit is: ", indicator.unit)

        comment = Comment(df)
        comment.find_comment()

        periods = Periods(df)
        periods.check_periods()

        objects = ObjectInfo(df, self.regions_dict)
        objects.compare_etalon()

        for key, info in objects.objects.items():
            for year in range(2000, 2022):
                result['section'].append(indicator.section)
                result['indicator_name'].append(indicator.name)
                result['indicator_unit'].append(indicator.unit)
                result['indicator_code'].append(indicator.code)
                result['object_name'].append(key)
                result['object_level'].append(info[0])
                result['object_oktmo'].append(info[1])
                result['object_okato'].append(info[2])
                result['year'].append(year)
                result['comment'].append(comment.comment)

                #Handling some unsusual values which can't be save as floats.
                if year in periods.periods.keys():
                    value = df.loc[info[3], periods.periods[year]]
                    if pd.isna(value):
                        value = -99999999
                    elif self.skip_value(value):
                        value = -88888888
                    elif ' р.' in value:
                        value = round(float(value.replace('в ', '').replace(' р.', '').replace(',', '.').strip())*100, 4)
                    elif ')' in value:
                        value = re.sub(r'\d[)]', '', str(value.replace(',', '.')))
                        value = -88888888 if self.skip_value(value) else round(float(value), 4)
                    else:
                        try:
                            value = round(float(value), 4)
                        except ValueError:
                            value = re.sub(r'\s+', '', str(value).replace(',', '.'))
                            value = round(float(value), 4) if not self.skip_value(value) else -88888888

                else:
                    value = -99999999

                result['indicator_value'].append(value)
        return result


if __name__ == '__main__':
    PATH_TO_FILE = "D:/coding/regions_parser/data/raw/Pril_Region_Pokaz_2022/Раздел 5 - Здравоохранение.xlsx" # Write here path to xlsx file with data.
    PATH_TO_DICT = "D:/coding/regions_parser/src/data/regions_etalon.yaml" # Write here path to regions_etalon.yaml file with regions dictionary.

    section = Section(PATH_TO_FILE, PATH_TO_DICT)
    data = section.process_section()
    data.to_csv(f"""D:/coding/regions_parser/data/processed/data_5_healthcare.csv""", index=False, sep=";", encoding="utf8")

    print(data.head())






