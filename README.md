<div align="center">

<image src="http://m.qpic.cn/psc?/V51UyG6T2hLdbN0oEgHl3fEkH73KqJt7/TmEUgtj9EK6.7V8ajmQrEEsEylM*52lTktZHLze*PTbMCd2wg4o5kkEyKNVsVL9UM5xK4GLClF.TOL*ty*FnqAuxBQmobbAoJ.gYMo62EQY!/mnull&bo=wADAAAAAAAADByI!&rf=photolist&t=5" height="64"/>

# PyCSES

CSES Access Framework for Python

#### [Main Repo](https://github.com/CSES-org/CSES)

</div>

## Introduction

PyCSES is a Python library that provides access to the CSES format. It is designed to be simple and easy to use.

> [!Warning]
> 由于上游 PyYaml 解析的不完善，`start_time` 和 `end_time` 可能会变为 `int` 类型，需要手动检测类型并用 `f'{int(time/60/60)}:{int(time/60%60)}:{time%60}'` 之类的方式转换回来。

## Functions

```python
import cses

# Read a CSES file
parser = cses.CSESParser("path/to/file.cses.yaml")

# Check if the file is valid
if not cses.CSESParser.is_cses_file("path/to/file.cses.yaml"):
    print("Not a valid CSES file")

# Get subjects
for subject in parser.get_subjects():
    print("Name:", subject["name"])
    print("Simplified Name:", subject["simplified_name"])
    print("Teacher:", subject["teacher"])
    print("Room:", subject["room"])
    print("")

# Get schedules
for schedule in parser.get_schedules():
    print("Name:", schedule["name"])
    print("Enable Day:", schedule["enable_day"])
    print("Weeks:", schedule["weeks"])
    print("Classes:")
    for class_ in schedule["classes"]:
        print("  Subject:", class_["subject"])
        print("  Start Time:", class_["start_time"])
        print("  End Time:", class_["end_time"])
    print("")


# Generate a CSES file
generator = cses.CSESGenerator(version=1)

# Add a subject
generator.add_subject(name="Math", simplified_name="M", teacher="Mr. Wang", room="101")

# Add a schedule
generator.add_schedule(name="Monday", enable_day="mon", weeks=all, classes=[
    {
        "subject": "Math",
        "start_time": "08:00:00",
        "end_time": "09:00:00"
    },
    {
        "subject": "Biology",
        "start_time": "09:00:00",
        "end_time": "10:00:00"
    }
])

# Save the file
generator.save_to_file("path/to/file.cses.yaml")
```


