import unittest
import os
import tempfile
import yaml
from cses.parser import CSESParser

class TestCSESParser(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'version': 1,
            'subjects': [
                {'name': 'Math', 'simplified_name': 'M', 'teacher': 'Mr. A', 'room': '101'},
                {'name': 'English', 'simplified_name': 'E'}
            ],
            'schedules': [
                {
                    'name': 'Monday',
                    'enable_day': 'mon',
                    'weeks': 'all',
                    'classes': [
                        {'subject': 'Math', 'start_time': '8:00', 'end_time': '9:00'}
                    ]
                }
            ]
        }
        
        self.yaml_content = yaml.dump(self.test_data)
        
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', mode='w', encoding='utf-8')
        self.tmp_file.write(self.yaml_content)
        self.tmp_file.close()
        self.file_path = self.tmp_file.name

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_is_cses_file(self):
        self.assertTrue(CSESParser.is_cses_file(self.file_path))
        
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as bad_file:
            bad_file.write("invalid: yaml: content")
            bad_path = bad_file.name
        bad_file.close()
        
        try:
            self.assertFalse(CSESParser.is_cses_file(bad_path))
        finally:
            os.remove(bad_path)

    def test_parser_init_file(self):
        parser = CSESParser(file_path=self.file_path)
        self.assertEqual(parser.version, 1)
        self.assertEqual(len(parser.subjects), 2)
        self.assertEqual(len(parser.schedules), 1)

    def test_parser_init_content(self):
        parser = CSESParser(content=self.yaml_content)
        self.assertEqual(parser.version, 1)
        self.assertEqual(len(parser.subjects), 2)
        self.assertEqual(len(parser.schedules), 1)

    def test_parser_init_error(self):
        with self.assertRaises(ValueError):
            CSESParser()

    def test_get_subjects(self):
        parser = CSESParser(content=self.yaml_content)
        subjects = parser.get_subjects()
        self.assertEqual(subjects[0]['name'], 'Math')
        self.assertEqual(subjects[1]['name'], 'English')

    def test_get_schedules(self):
        parser = CSESParser(content=self.yaml_content)
        schedules = parser.get_schedules()
        self.assertEqual(schedules[0]['name'], 'Monday')

    def test_get_schedule_by_day(self):
        parser = CSESParser(content=self.yaml_content)
        classes = parser.get_schedule_by_day('mon')
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0]['subject'], 'Math')
        
        empty_classes = parser.get_schedule_by_day('tue')
        self.assertEqual(len(empty_classes), 0)

    def test_parser_validation(self):
        # Missing subject name
        malformed_data = {
            'version': 1,
            'subjects': [{'simplified_name': 'M'}],
            'schedules': []
        }
        with self.assertRaisesRegex(ValueError, "missing required field 'name'"):
            CSESParser(content=yaml.dump(malformed_data))

        # Missing schedule fields
        malformed_data = {
            'version': 1,
            'subjects': [],
            'schedules': [{'name': 'Monday'}] # Missing enable_day, weeks
        }
        with self.assertRaisesRegex(ValueError, "missing required field 'enable_day'"):
            CSESParser(content=yaml.dump(malformed_data))

        # Malformed structure (subjects not a list)
        malformed_data = {
            'version': 1,
            'subjects': "not a list",
            'schedules': []
        }
        with self.assertRaisesRegex(ValueError, "Field 'subjects' must be a list"):
            CSESParser(content=yaml.dump(malformed_data))

if __name__ == '__main__':
    unittest.main()
