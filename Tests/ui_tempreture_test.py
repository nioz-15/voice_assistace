import pytest
import logging
from Infra.ui import AndroidUITest


@pytest.fixture(scope='module')
def android_ui_test_instance():
    android_ui_test = AndroidUITest()
    yield android_ui_test
    android_ui_test.teardown()


@pytest.mark.parametrize('new_temperature', ['25', '30', '20'])
def test_temperature_change(android_ui_test_instance, new_temperature):
    new_temp_value = android_ui_test_instance.test_temperature_change(new_temperature)
    assert new_temp_value == new_temperature


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    pytest.main([__file__])