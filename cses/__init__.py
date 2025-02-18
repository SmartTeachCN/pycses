import yaml
from pathlib import Path
from collections import OrderedDict

# 解析器
class CSESParser:
    def __init__(self, file_path):
        """
        初始化 CSES 解析器
        
        Args:
            file_path (str): CSES 格式的 YAML 文件路径
        """
        self.file_path  = file_path
        self.data  = None
        self.version  = None
        self.subjects  = []
        self.schedules  = []
        
        self._load_file()
        self._parse_data()
    
    def _load_file(self):
        """加载并解析 YAML 文件"""
        try:
            with open(self.file_path,  'r', encoding='utf-8') as f:
                self.data  = yaml.load(f, Loader=yaml.BaseLoader) 
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.file_path} Not Found")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML Error: {e}")
    
    def _parse_data(self):
        """解析 YAML 数据"""
        if not self.data: 
            return
        
        # 获取版本信息
        self.version  = self.data.get('version',  1)
        
        # 解析科目信息
        subjects_data = self.data.get('subjects',  [])
        for subject in subjects_data:
            subject_info = {
                'name': subject['name'],
                'simplified_name': subject.get('simplified_name'), 
                'teacher': subject.get('teacher'), 
                'room': subject.get('room') 
            }
            self.subjects.append(subject_info) 
        
        # 解析课程安排
        schedules_data = self.data.get('schedules',  [])
        for schedule in schedules_data:
            schedule_info = {
                'name': schedule['name'],
                'enable_day': int(schedule['enable_day']),
                'weeks': schedule['weeks'],
                'classes': []
            }
            
            # 解析课程
            classes_data = schedule.get('classes',  [])
            for cls in classes_data:
                class_info = {
                    'subject': cls['subject'],
                    'start_time': cls['start_time'],
                    'end_time': cls['end_time']
                }
                schedule_info['classes'].append(class_info)
            
            self.schedules.append(schedule_info) 
    
    def get_subjects(self):
        """获取所有科目信息"""
        return self.subjects 
    
    def get_schedules(self):
        """获取所有课程安排"""
        return self.schedules 
    
    def get_schedule_by_day(self, day):
        """
        根据星期获取课程安排
        
        Args:
            day (str): 星期（如 'mon', 'tue' 等）
            
        Returns:
            list: 该星期的课程安排
        """
        for schedule in self.schedules: 
            if schedule['enable_day'] == day:
                return schedule['classes']  
        return []
    
    @staticmethod
    def is_cses_file(file_path):
        """
        判断是否为 CSES 格式的文件
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            bool: 是否为 CSES 文件
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) 
                return 'version' in data and 'subjects' in data and 'schedules' in data
        except:
            return False

# 生成器
class CSESGenerator:
    def __init__(self, version=1):
        """
        初始化 CSES 生成器 
        
        Args:
            version (int, optional): CSES 格式的版本号，默认为 1 
        """
        self.version  = version 
        self.subjects  = []
        self.schedules  = []

    def add_subject(self, name, simplified_name=None, teacher=None, room=None):
        """
        添加科目信息 
        
        Args:
            name (str): 科目名称 
            simplified_name (str, optional): 科目简称 
            teacher (str, optional): 教师姓名 
            room (str, optional): 教室名称 
        """
        subject = {
            'name': name,
            'simplified_name': simplified_name,
            'teacher': teacher,
            'room': room
        }
        self.subjects.append(subject) 
    
    def add_schedule(self, name, enable_day, weeks, classes):
        """
        添加课程安排 
        
        Args:
            name (str): 课程安排名称（如 "星期一"）
            enable_day (str): 课程安排的星期（如 'mon', 'tue' 等）
            weeks (str): 周次类型（如 'all', 'odd', 'even'）
            classes (list): 课程列表，每个课程包含以下键：
                - subject (str): 科目名称 
                - start_time (str): 开始时间（如 '8:00'）
                - end_time (str): 结束时间（如 '9:00'）
        """
        schedule = {
            'name': name,
            'enable_day': enable_day,
            'weeks': weeks,
            'classes': classes
        }
        self.schedules.append(schedule) 
    
    def generate_cses_data(self):
        """
        生成 CSES 格式的字典数据 
        
        Returns:
            dict: CSES 格式的字典数据 
        """
        cses_data = {
            'version': self.version,
            'subjects': self.subjects,
            'schedules': self.schedules
        }
        return cses_data 
    
    def save_to_file(self, file_path):
        """
        将 CSES 数据保存到 YAML 文件 
        
        Args:
            file_path (str): 输出文件路径 
        """
        cses_data = self.generate_cses_data() 
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(cses_data,  f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except IOError as e:
            raise IOError(f"Failed to write {file_path}: {e}")

# 示例用法
if __name__ == "__main__":
    import sys
    
    if len(sys.argv)  != 2:
        print("""Check CSES File
Usage: python -m cses <cses_file>""")
        sys.exit(1) 
    
    file_path = sys.argv[1] 
    
    if not CSESParser.is_cses_file(file_path): 
        print("Not a valid CSES file")
        sys.exit(1) 
    
    parser = CSESParser(file_path)
    
    print("All Subjects:")
    for subject in parser.get_subjects(): 
        print(f"{subject['name']} ({subject.get('simplified_name',  '')})")
        print(f"- Teacher: {subject.get('teacher',  '')}")
        print(f"- Room: {subject.get('room',  '')}")
    
    print("\nAll Schedules:")
    for schedule in parser.get_schedules():
        print(f"{schedule['name']} ({schedule['enable_day']} {schedule['weeks']}):")
        for cls in schedule['classes']:
            print(f"- {cls['subject']} ({cls['start_time']} - {cls['end_time']})")

