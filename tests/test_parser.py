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
        
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml', mode='w', encoding='utf-8')
        yaml.dump(self.test_data, self.tmp_file)
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

    def test_parser_init(self):
        parser = CSESParser(self.file_path)
        self.assertEqual(parser.version, 1)
        self.assertEqual(len(parser.subjects), 2)
        self.assertEqual(len(parser.schedules), 1)

    def test_get_subjects(self):
        parser = CSESParser(self.file_path)
        subjects = parser.get_subjects()
        self.assertEqual(subjects[0]['name'], 'Math')
        self.assertEqual(subjects[1]['name'], 'English')

    def test_get_schedules(self):
        parser = CSESParser(self.file_path)
        schedules = parser.get_schedules()
        self.assertEqual(schedules[0]['name'], 'Monday')

    def test_get_schedule_by_day(self):
        parser = CSESParser(self.file_path)
        classes = parser.get_schedule_by_day('mon')
        self.assertEqual(len(classes), 1)
        self.assertEqual(classes[0]['subject'], 'Math')
        
        empty_classes = parser.get_schedule_by_day('tue')
        self.assertEqual(len(empty_classes), 0)

if __name__ == '__main__':
    unittest.main()
