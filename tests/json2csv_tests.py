import io
import json
import unittest
from json2csv import extract_keys, load_json, dump_csv

class TestJsonToCsvConverter(unittest.TestCase):

    json_data = [
        {"name": "John", "age": 30},
        {"age": 25, "name": "Jane"},
        {"age": 35, "city": "Paris", "name": "Bob"}
    ]
    csv_data = 'name,age,city\r\nJohn,30,\r\nJane,25,\r\nBob,35,Paris\r\n'
    json_data_string = json.dumps(json_data)
    delimited_data = '\n'.join([json.dumps(record) for record in json_data])

    def test_extract_key(self):
        expected_keys = ["name", "age", "city"]
        self.assertEqual(extract_keys(self.json_data), expected_keys)

    def test_extract_keys_empty_data(self):
        json_data = []
        expected_keys = []
        self.assertEqual(extract_keys(json_data), expected_keys)

    def test_load_json_regular_format(self):
        file_obj = io.StringIO(self.json_data_string)
        loaded_data = load_json(file_obj)
        self.assertEqual(loaded_data, self.json_data)

    def test_load_json_line_delimited_format(self):
        file_obj = io.StringIO(self.delimited_data)
        loaded_data = load_json(file_obj, line_delimited=True)
        self.assertEqual(loaded_data, self.json_data)

    def test_load_json_invalid_format(self):
        file_content = "invalid json"
        file_obj = io.StringIO(file_content)
        with self.assertRaises(ValueError):
            load_json(file_obj)

    def test_load_json_valid_but_assertion_error(self):
        json_data = { 'data': [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]}
        file_content = json.dumps(json_data)
        file_obj = io.StringIO(file_content)
        with self.assertRaises(AssertionError):
            load_json(file_obj)

    def test_load_delimited_but_assertion_error(self):
        json_data_delimited = '[{"name": "Jaromir"}]'
        file_content = json.dumps(json_data_delimited)
        file_obj = io.StringIO(file_content)
        with self.assertRaises(AssertionError):
            load_json(file_obj, line_delimited=True)

    def test_dump_csv(self):
        file_obj = io.StringIO()
        dump_csv(self.json_data, file_obj)
        self.assertEqual(file_obj.getvalue(), self.csv_data)


if __name__ == '__main__':
    unittest.main()
