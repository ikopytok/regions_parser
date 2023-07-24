"""Class to proccess specific indicators."""
import pandas as pd
import re


class Indicator:
    """Parse indicator characteristics (section, name, unit, code) from xlsx sheet."""

    def __init__(self, data: pd.DataFrame):
        """
        Initialize class to parse data
        :param data: DataFrame with data from some xlsx file sheet.
        """
        """Initialize class to parse data"""
        self.section = None
        self.name = None
        self.unit = None
        self.code = None
        self.data = data

    def find_names(self):
        """Search indicator name, section, unit and code in dataframe (first column)."""

        # Ищем все в первой колонке датафрема, который получили из листа файла xlsx
        first_column = self.data.iloc[:, 0].apply(lambda x: ' '.join(x.split()) if not pd.isna(x) else x)
        # Нужная нам инфа до строки, в которой указано Российская Федерация
        text_to_find = "Российская Федерация"
        matching_rows = first_column.str.contains(text_to_find).fillna(False)
        index_of_row = matching_rows[matching_rows].index.tolist()

        if len(index_of_row) == 0:
            raise ValueError("Name is not find. Russia Federation is not in dataframe.")
        elif len(index_of_row) == 2:
            raise ValueError("Several rows with Russian Federation.")
        else:
            special_for_russia = ''
            if len(first_column[index_of_row[0]]) > 22:
                special_for_russia = ', ' + first_column[index_of_row[0]][20:] + ' для значений в целом по России'

            """
            Тут под разные варианты xlsx листа разбор. Иногда нужные данные об индикаторе хранятся в разных строках.
            Позиции можно вычислить относительно строки, в которой есть Российская Федерация.
            Внутри if просто аккуратно обрабатываем строки и собираем нужную информацию.
            """
            if index_of_row[0] == 7:
                self.section = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[1]).strip()).replace('1)', '')

                self.name = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[3]).strip().replace('1)', '')) + ': ' + \
                            self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[4]).strip().replace('1)', ''))

                self.unit = first_column[5].strip("()").replace(';', ',') + special_for_russia
                self.code = ''.join([part.zfill(2) for part in re.match(r'^[\d.]+',
                                                                        first_column[4]).group().split('.')]).ljust(8,
                                                                                                                    '0')
            elif index_of_row[0] == 6:
                self.section = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[1]).strip()).replace('1)', '')

                self.name = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[2]).strip().replace('1)', '')) + ': ' + \
                            self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[3]).strip().replace('1)', ''))

                self.unit = first_column[4].strip("()").replace(';', ',') + special_for_russia
                self.code = ''.join([part.zfill(2) for part in re.match(r'^[\d.]+',
                                                                        first_column[3]).group().split('.')]).ljust(8,
                                                                                                                    '0')
            elif index_of_row[0] == 5:
                self.section = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[1]).strip()).replace('1)', '')

                self.name = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[2]).strip()).replace('1)', '')

                self.unit = first_column[3].strip("()").replace(';', ',') + special_for_russia
                self.code = ''.join([part.zfill(2) for part in re.match(r'^[\d.]+',
                                                                        first_column[2]).group().split('.')]).ljust(8,
                                                                                                                    '0')
            elif index_of_row[0] == 4:
                self.section = self.lower_sentence(re.sub(r'^[\d.]+', '', first_column[1]).strip()).replace('1)', '')
                self.name = self.lower_sentence(
                    re.sub(r'^[\d.]+', '', first_column[2][:first_column[2].index(' на 10')].strip().replace('1)', '')))
                self.unit = first_column[2][first_column[2].index(' на 10'):].strip().replace('1)', '') + special_for_russia
                self.code = ''.join([part.zfill(2) for part in re.match(r'^[\d.]+',
                                                                        first_column[2]).group().split('.')]).ljust(8,
                                                                                                                    '0')
            else:
                raise ValueError("Row index for Russian Federation is not rigth.")

        return self.section, self.name, self.unit, self.code

    def lower_sentence(self, sentence: str):
        """
        Strip string and change all characters except first to lowecase.
        :param sentence:
        :return:
        """
        sentence = sentence.strip()
        return sentence[0] + sentence[1:].lower()


if __name__ == '__main__':
    pass
