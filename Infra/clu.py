import csv
import requests
import json
import logging


class CLUTest:
    def __init__(self, csv_file_path, api_url):
        self.csv_file_path = csv_file_path
        self.api_url = api_url
        self.results = []

    def send_utterance_to_api(self, utterance):
        try:
            payload = {
                'utterance': utterance
            }
            response = requests.post(self.api_url, json=payload)

            if response.status_code == 200:
                return response.text
            else:
                logging.error(f"API request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error sending utterance to API: {str(e)}")
            return None

    @staticmethod
    def parse_api_response(api_response):
        response_data = json.loads(api_response)
        return response_data['intent'], response_data['entity']

    def run_tests(self):
        with open(self.csv_file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                utterance = row['Utterance']
                expected_intent = row['Expected Intent']
                expected_entity = row['Expected Entity']

                api_response = self.send_utterance_to_api(utterance)
                if api_response is not None:
                    api_intent, api_entity = self.parse_api_response(api_response)

                    intent_similarity = 'Similar' if api_intent == expected_intent else 'Non-similar'
                    entity_similarity = 'Similar' if api_entity == expected_entity else 'Non-similar'

                    self.results.append({
                        'Utterance': utterance,
                        'API Intent': api_intent,
                        'Expected Intent': expected_intent,
                        'API Entity': api_entity,
                        'Expected Entity': expected_entity,
                        'Intent Similarity': intent_similarity,
                        'Entity Similarity': entity_similarity
                    })

    def calculate_similarity_percentage(self, similarity_type):
        total_utterances = len(self.results)
        similar_count = sum(1 for result in self.results if result[similarity_type] == 'Similar')
        similarity_percentage = (similar_count / total_utterances) * 100
        return similarity_percentage

    def check_pass_criteria(self, intent_pass_criteria, entity_pass_criteria):
        intent_similarity_percentage = self.calculate_similarity_percentage('Intent Similarity')
        entity_similarity_percentage = self.calculate_similarity_percentage('Entity Similarity')

        return intent_similarity_percentage >= intent_pass_criteria and \
            entity_similarity_percentage >= entity_pass_criteria

    def create_results_log(self, result_file_path):
        with open(result_file_path, mode='w') as result_file:
            fieldnames = ['Utterance', 'API Intent', 'Expected Intent', 'API Entity', 'Expected Entity',
                          'Intent Similarity', 'Entity Similarity']
            writer = csv.DictWriter(result_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

