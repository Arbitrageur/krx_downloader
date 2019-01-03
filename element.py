from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseElement:
    def __init__(self, driver, selector):
        self.driver = driver
        self.selector = selector

        self._wait = WebDriverWait(self.driver, 10)

        self.element = self._wait.until(
            EC.presence_of_element_located(self.selector)
        )


class InputElement(BaseElement):
    def __init__(self, driver, selector):
        super().__init__(driver, selector)

    def value(self, value):
        self.element.clear()
        self.element.send_keys(value)


class SelectElement(BaseElement):
    def __init__(self, driver, selector):
        super().__init__(driver, selector)
        self.element.click()


class ButtonElement(SelectElement):
    def __init__(self, driver, selector):
        _wait = WebDriverWait(driver, 10)

        _wait.until(
            EC.presence_of_element_located(selector)
        ).click()

