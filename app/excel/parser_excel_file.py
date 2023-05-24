import locale


class ParserExcelFile:
    __headers = ['vendor', 'invoice_date', 'invoice_number', 'comment', 'invoice_due_date',
                 'invoice_amount', 'job_number_1', 'cost_code_1', 'type_1', 'amount_1', 'comment_1', 'gl_1',
                 'job_number_2', 'cost_code_2', 'type_2', 'amount_2', 'comment_2', 'gl_2']

    def parse(self, dataframe):
        try:
            dataframe.columns = dataframe.iloc[0]
            dataframe.columns = dataframe.iloc[1]

            dataframe.columns = self.__headers

            df = dataframe[2:]

            parsedData = []

            for i in range(2, len(df)):
                data = {
                    'vendor': str(df.loc[i, 'vendor']),
                    'invoice_date': self.__parseDate(df.loc[i, 'invoice_date']),
                    'invoice_number': str(df.loc[i, 'invoice_number']),
                    'comment': str(df.loc[i, 'comment']),
                    "invoice_due_date": self.__parseDate(df.loc[i, 'invoice_due_date']),
                    "invoice_amount": self.__parseAmount(df.loc[i, 'invoice_amount']),
                    "lines": [{
                        'job_number': str(df.loc[i, 'job_number_1']),
                        'cost_code': str(df.loc[i, 'cost_code_1']),
                        'type': str(df.loc[i, 'type_1']),
                        'amount': self.__parseAmount(df.loc[i, 'amount_1']),
                        'comment': str(df.loc[i, 'comment_1']),
                        'gl': str(df.loc[i, 'gl_1']),
                    },
                        {
                            'job_number': str(df.loc[i, 'job_number_2']),
                            'cost_code': str(df.loc[i, 'cost_code_2']),
                            'type': str(df.loc[i, 'type_2']),
                            'amount': self.__parseAmount(df.loc[i, 'amount_2']),
                            'comment': str(df.loc[i, 'comment_2']),
                            'gl': str(df.loc[i, 'gl_2']),
                        }]
                }

                parsedData.append(data)

            return parsedData
        except Exception as e:
            raise Exception("Error parse excel file to Sage data", e)

    def __parseDate(self, datetime):
        return datetime.strftime('%m/%d/%Y')

    def __parseAmount(self, amount):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        return locale.atof(str(locale.format('%.2f', amount)))
