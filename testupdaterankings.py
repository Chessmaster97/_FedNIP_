import unittest
import json
import os

# Assuming your code is in a file named rankings.py
from updaterankings import update_rankings

class TestUpdateRankings(unittest.TestCase):
    def setUp(self):
        # Create temporary files for testing
        self.top_file = 'test_top.json'
        self.random_file = 'test_random.json'

        top_data = [
            {"clientID": 2, "accuracy": 0.3999}
        ]
        random_data = [
            {"clientID": 8, "accuracy": 0.20},
            {"clientID": 11, "accuracy": 0.4124},
            {"clientID": 14, "accuracy": 0.4172}
        ]

        with open(self.top_file, 'w') as file:
            json.dump(top_data, file)
        with open(self.random_file, 'w') as file:
            json.dump(random_data, file)

    def tearDown(self):
        # Clean up temporary files after testing
        os.remove(self.top_file)
        os.remove(self.random_file)
        os.remove("LogSwaps.json")

    def test_update_rankings(self):
        # Test with top_threshold=0.05 and random_threshold=0.05
        update_rankings(self.top_file, self.random_file, 0.05, 0.05)

        # Check if the files were updated correctly
        with open(self.top_file, 'r') as file:
            top_performers = json.load(file)
        with open(self.random_file, 'r') as file:
            random_performers = json.load(file)

        # Check if the performers are sorted correctly
        self.assertEqual(top_performers, [{"clientID": 14, "accuracy": 0.4172}])
        self.assertEqual(random_performers, [
            {"clientID": 11, "accuracy": 0.4124},
            {"clientID": 14, "accuracy": 0.4172},
            {"clientID": 8, "accuracy": 0.20}
        ])

        # Check if the LogSwaps.json file was created and contains correct data
        with open("LogSwaps.json", 'r') as log_file:
            log_data = [json.loads(line) for line in log_file]

        self.assertEqual(log_data, [
            {
                'top_client_id': 2,
                'random_client_id': 14,
                'top_accuracy': 0.3999,
                'random_accuracy': 0.4172,
                'random_threshold': 0.05,
                'tresholdmet': 'False'
            },
            {
                'top_client_id': 2,
                'random_client_id': 14,
                'top_accuracy': 0.3999,
                'random_accuracy': 0.4172,
                'random_threshold': 0.05
            }
        ])


if __name__ == '__main__':
    unittest.main()
