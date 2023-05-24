from app.connector_application import ConnectorApplication
from app.excel.load_excel_file import LoadExcelFile
from app.excel.parser_excel_file import ParserExcelFile
from app.import_invoice import ImportInvoice
from app.windows.invoice_data_entry_window import InvoiceDataEntryWindow
from app.windows.window_handle_finder import WindowHandleFinder


class ImportInvoices:
    def __getHandleWindowSage(self):
        windowHandleFinder = WindowHandleFinder()
        return windowHandleFinder.getHandleByContainsWindowName('A/P Invoice Data Entry')

    def importExcelFile(self, path):
        loadExcelFile = LoadExcelFile()
        return loadExcelFile.load(path)

    def parseExcelFile(self, excelFile):
        parser = ParserExcelFile()
        return parser.parse(excelFile)

    def connectToApplication(self, timeout=5):
        connector = ConnectorApplication()
        handleWindowSage = self.__getHandleWindowSage()

        return connector.connect(handleWindowSage, timeout)

    def importInvoices(self):
        try:
            excelFile = self.importExcelFile('test2.xlsx')
            invoices = self.parseExcelFile(excelFile)

            app = self.connectToApplication(timeout=5)

            invoiceDataEntryWindow = InvoiceDataEntryWindow(app)
            importInvoice = ImportInvoice(app)

            for invoice in invoices:
                try:
                    importInvoice.importInvoice(invoice)
                except Exception as e:
                    print(e)
                    invoiceDataEntryWindow.cancel()
                    pass

        except Exception as e:
            print(e)
            raise e
