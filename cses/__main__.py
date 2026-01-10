import sys
from cses.parser import CSESParser

def main():
    if len(sys.argv) != 2:
        print("""Check CSES File
Usage: python -m cses <cses_file>""")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not CSESParser.is_cses_file(file_path):
        print("Not a valid CSES file")
        sys.exit(1)
    
    try:
        parser = CSESParser(file_path)
        
        print("All Subjects:")
        for subject in parser.get_subjects():
            print(f"{subject['name']} ({subject.get('simplified_name', '')})")
            print(f"- Teacher: {subject.get('teacher', '')}")
            print(f"- Room: {subject.get('room', '')}")
        
        print("\nAll Schedules:")
        for schedule in parser.get_schedules():
            print(f"{schedule['name']} ({schedule['enable_day']} {schedule['weeks']}):")
            for cls in schedule['classes']:
                print(f"- {cls['subject']} ({cls['start_time']} - {cls['end_time']})")
                
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
