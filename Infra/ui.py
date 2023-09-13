import logging
from appium import webdriver


class AndroidUITest:
    def __init__(self):
        self.desired_caps = {
            'platformName': 'Android',
            'deviceName': 'emulator-5554',
            'appPackage': 'com.yourapp.package',
            'appActivity': '.MainActivity',
        }
        self.driver = None

    def setup(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)

    def teardown(self):
        if self.driver is not None:
            self.driver.quit()

    def test_temperature_change(self, new_temperature):
        try:
            self.setup()
            logging.info('Android UI test setup complete.')

            # Locate the temperature input field by its resource id
            temperature_input = self.driver.find_element_by_id('com.yourapp.package:id/temperature_input')

            # Clear any existing text and enter a new temperature value
            temperature_input.clear()
            temperature_input.send_keys(new_temperature)
            logging.info(f'Entered new temperature: {new_temperature}')

            # Locate and click the "Save" button to apply the temperature change
            save_button = self.driver.find_element_by_id('com.yourapp.package:id/save_button')
            save_button.click()
            logging.info('Clicked "Save" button.')

            # Verify that the temperature has changed as expected
            new_temperature_value = self.driver.find_element_by_id('com.yourapp.package:id/current_temperature').text
            logging.info(f'New Temperature Value: {new_temperature_value}')

            return new_temperature_value
        except Exception as e:
            logging.error(f'UI test failed with error: {str(e)}')
            raise
        finally:
            self.teardown()
            logging.info('Android UI test teardown complete.')
