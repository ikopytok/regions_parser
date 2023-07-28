import pandas as pd


class Periods:
    """Find on xlsx sheets what periods (years) are available."""
    def __init__(self, data: pd.DataFrame):
        """
        Initialize class to find available years.
        :param data: DataFrame with data from some xlsx file sheet.
        """
        self.periods = None # Here we save available periods in dictionary (year - column with data for this year format)
        self.data = data

    def check_periods(self):
        """
        Here find row with years and save all available years.
        :return:
        """

        year_column = self.data.iloc[:, 0].apply(lambda x: True if pd.isna(x) else False)
        index_of_row = year_column[year_column].index.tolist()

        if len(index_of_row) == 0:
            raise ValueError("Period string is not find.")
        elif len(index_of_row) >= 2:
            row = None
            for el in index_of_row:
                if not pd.isna(self.data.iloc[el, 2]):
                    if self.data.iloc[el, 2].startswith('2'):
                        row = el
                    else:
                        pass
                else:
                    pass
            if not row:
                raise ValueError("Period string is not find.")
            year_values = {int(i.strip()[0:4]): j for j, i in self.data.iloc[row][1:].items() if not pd.isna(i)}
            self.periods = year_values
            return year_values
        else:
            year_values = {int(i.strip()[0:4]): j for j, i in self.data.iloc[index_of_row[0]][1:].items() if not pd.isna(i)}
            self.periods = year_values
            return year_values


if __name__ == '__main__':
    pass
