import yaml
from typing import List, Dict, Any, Optional, Union

class CSESParser:
    def __init__(self, file_path: str):
        """
        初始化 CSES 解析器
        
        Args:
            file_path (str): CSES 格式的 YAML 文件路径
        """
        self.file_path: str = file_path
        self.data: Optional[Dict[str, Any]] = None
        self.version: Optional[Union[int, str]] = None
        self.subjects: List[Dict[str, Any]] = []
        self.schedules: List[Dict[str, Any]] = []
        
        self._load_file()
        self._parse_data()
    
    def _load_file(self) -> None:
        """加载并解析 YAML 文件"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.file_path} Not Found")
        except yaml.YAMLError as e:
            raise ValueError(f"YAML Error: {e}")
    
    def _parse_data(self) -> None:
        """解析 YAML 数据"""
        if not self.data:
            return
        
        # 获取版本信息
        self.version = self.data.get('version', 1)
        
        # 解析科目信息
        subjects_data = self.data.get('subjects', [])
        for subject in subjects_data:
            subject_info = {
                'name': subject['name'],
                'simplified_name': subject.get('simplified_name'),
                'teacher': subject.get('teacher'),
                'room': subject.get('room')
            }
            self.subjects.append(subject_info)
        
        # 解析课程安排
        schedules_data = self.data.get('schedules', [])
        for schedule in schedules_data:
            schedule_info = {
                'name': schedule['name'],
                'enable_day': schedule['enable_day'],
                'weeks': schedule['weeks'],
                'classes': []
            }
            
            # 解析课程
            classes_data = schedule.get('classes', [])
            for cls in classes_data:
                class_info = {
                    'subject': cls['subject'],
                    'start_time': cls['start_time'],
                    'end_time': cls['end_time']
                }
                schedule_info['classes'].append(class_info)
            
            self.schedules.append(schedule_info)
    
    def get_subjects(self) -> List[Dict[str, Any]]:
        """获取所有科目信息"""
        return self.subjects
    
    def get_schedules(self) -> List[Dict[str, Any]]:
        """获取所有课程安排"""
        return self.schedules
    
    def get_schedule_by_day(self, day: str) -> List[Dict[str, Any]]:
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
    def is_cses_file(file_path: str) -> bool:
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
        except Exception:
            return False
