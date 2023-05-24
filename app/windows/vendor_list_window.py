from app.exceptions.not_found_window_exception import NotFoundWindowException
from app.windows.base_window import BaseWindow


class VendorListWindow(BaseWindow):
    __windowName = 'Vendor List'

    def __init__(self, app):
        self.__app = app
        self.__window = self.__getWindowVendorList()

    def __getWindowVendorList(self):
        try:
            self.__app.window(title_re=f'{self.__windowName}').wait('visible', 10)
            return self.__app.window(title_re='Vendor List')
        except Exception as e:
            raise NotFoundWindowException(self.__windowName, e)

    def typeVendor(self, vendor):
        self.__window['Edit'].wait('visible', 10)
        self.__window['Edit'].click()
        self.__window['Edit'].set_text(vendor)
        self.enter()

    def filters(self, vendor):
        self.typeVendor(vendor)

    def __getVendorsSearchResult(self):
        self.__window['SysListView32'].wait('visible', 10)
        return self.__window['SysListView32'].texts()

    def vendorExists(self, vendor):
        try:
            self.filters(vendor)

            vendorsResult = self.__getVendorsSearchResult()

            self.cancel()

            for vendorResult in vendorsResult:
                if vendor in vendorResult:
                    return True
            return False

        except Exception as e:
            self.cancel()
            raise Exception('An error occurred while checking if the vendor exists', e)

    def cancel(self):
        def isEnabled():
            try:
                self.__window['&Cancel'].wait('enabled', 2)
                return True
            except Exception:
                return False

        if not isEnabled():
            return

        self.__window['&Cancel'].wait('visible', 10)
        self.__window['&Cancel'].click()
