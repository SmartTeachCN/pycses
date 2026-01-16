from setuptools import setup, find_packages

setup(
    name='pycses',
    version='0.1.3',
    author='SmartTeachCN',
    author_email='contact@smart-teach.cn',
    description='CSES access framework for Python',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SmartTeachCN/pycses',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyYAML>=5.4.1',
    ],
)
