import pytest
from Infra.clu import CLUTest
import logging


@pytest.fixture(scope='module')
def clu_test_instance():
    csv_file_path = 'utterances.csv'
    api_url = 'http://clu-api.example.com'
    result_file_path = 'clu_test_results.csv'

    clu_test = CLUTest(csv_file_path, api_url)
    clu_test.run_tests()
    clu_test.create_results_log(result_file_path)
    yield clu_test


def test_clu_test_result(clu_test_instance):
    intent_pass_criteria = 85
    entity_pass_criteria = 75
    assert clu_test_instance.check_pass_criteria(intent_pass_criteria, entity_pass_criteria)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pytest.main([__file__])
