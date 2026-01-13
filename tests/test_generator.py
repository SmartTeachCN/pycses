import unittest
import os
import tempfile
from cses.generator import CSESGenerator

class TestCSESGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = CSESGenerator(version=1)

    def test_add_subject(self):
        self.generator.add_subject("Math", "M", "Mr. A", "101")
        self.assertEqual(len(self.generator.subjects), 1)
        self.assertEqual(self.generator.subjects[0]['name'], "Math")
        self.assertEqual(self.generator.subjects[0]['simplified_name'], "M")

    def test_add_schedule(self):
        classes = [{'subject': 'Math', 'start_time': '8:00', 'end_time': '9:00'}]
        self.generator.add_schedule("Monday", "mon", "all", classes)
        self.assertEqual(len(self.generator.schedules), 1)
        self.assertEqual(self.generator.schedules[0]['name'], "Monday")
        self.assertEqual(self.generator.schedules[0]['classes'][0]['subject'], 'Math')

    def test_generate_cses_data(self):
        self.generator.add_subject("Math")
        data = self.generator.generate_cses_data()
        self.assertIn('version', data)
        self.assertIn('subjects', data)
        self.assertIn('schedules', data)
        self.assertEqual(len(data['subjects']), 1)

    def test_save_to_file(self):
        self.generator.add_subject("Math")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.yaml') as tmp:
            tmp_path = tmp.name
        
        try:
            self.generator.save_to_file(tmp_path)
            self.assertTrue(os.path.exists(tmp_path))
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("Math", content)
        finally:
            os.remove(tmp_path)

    def test_to_string(self):
        self.generator.add_subject("Math")
        yaml_str = self.generator.to_string()
        self.assertIsInstance(yaml_str, str)
        self.assertIn("Math", yaml_str)
        self.assertIn("version: 1", yaml_str)

if __name__ == '__main__':
    unittest.main()
