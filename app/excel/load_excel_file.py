import pandas


class LoadExcelFile:

    def load(self, path):
        try:
            return pandas.read_excel(path)
        except FileNotFoundError as e:
            raise FileNotFoundError('Excel file import error', e)
