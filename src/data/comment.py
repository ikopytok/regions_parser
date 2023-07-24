import pandas as pd
import os
import re


class Comment:
    """Find special footnotes and comments in DataFrame prepared from xlsx sheet."""
    def __init__(self, data: pd.DataFrame):
        """
        Intialize class to find footnotes.
        :param data: DataFrame with data from some xlsx file sheet.
        """
        self.comment = '' # Save here processed text of all footnotes.
        self.data = data

    def find_comment(self):
        """
        Find all comments in dataframe (strings begining with '*)' chatacters, where * is digit.
        :return: All comments in one string.
        """

        substring_list = ["1)", "2)", "3)", "4)", "5)", "6)", "7)", "8)", "9)"]
        superscript_map = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁾', '0123456789)') # To correctly process superscript characters
        self.data = self.data.applymap(lambda cell: cell.translate(superscript_map) if not pd.isna(cell) else cell)
        comment = ''

        for comm in substring_list:
            text = ''
            matching_cells = self.data.applymap(lambda cell: self.check_substring(cell, comm))
            matching_cells = matching_cells.stack()
            matching_cells = matching_cells[matching_cells] #True if footnote in a cell

            if len(matching_cells) > 0:

                all_equal = all(sublist[1] == 'Unnamed: 0' for sublist in matching_cells.index)

                if all_equal:
                    """Если все сноски с этим номером в первой колонке, то перечисляем через запятую первые n-1 значений,
                    а дальше через двоеточие добавляем комментарий из под таблицы.
                    """
                    text = ', '.join([re.sub(r'^[\d.]+', '', self.data.loc[i[0], i[1]].replace(comm, '').strip()) for i in matching_cells.index[:-1]])\
                           + ': ' + self.data.loc[matching_cells.index[-1][0],
                                         matching_cells.index[-1][1]].replace(comm, '').strip()
                else:
                    """Если все сноски с этим номером из разных колонок, то перечисляем через запятую все значения,
                    которые есть не в первой колонке, а потом через двоеточие добавляем комментарий из под таблицы.
                    """
                    text = ', '.join([re.sub(r'^[\d.]+', '', self.data.loc[i[0], i[1]].replace(comm, '').strip())
                                      for i in matching_cells.index if i[1] == 'Unnamed: 0']) + \
                           ': ' + ', '.join([self.data.loc[i[0], i[1]].replace(comm, '').strip()
                                             for i in matching_cells.index if i[1] != 'Unnamed: 0'])
                text = ' '.join(text.split())

                if comment == '':
                    comment = comm + ' ' + text
                else:
                    if comment[-1] == '.':
                        comment = comment + ' ' + comm + ' ' + text
                    else:
                        comment = comment + '. ' + comm + ' ' + text

        self.comment = comment.replace(';', ',')
        return self.comment

    def check_substring(self, cell, number: str):
        """Checl is data in cell is string and substring with footnote number is in it."""
        if isinstance(cell, str) and number in cell:
            return True
        return False


if __name__ == '__main__':
    pass