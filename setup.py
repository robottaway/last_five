from setuptools import setup, find_packages
setup(
    name = 'last five',
    version = '0.1.0',
    author = 'Rob Ottaway',
    author_email = 'robottaway@gmail.com',
    description = 'simple app for reading a Rack::CommonLogger log',
    packages = find_packages(exclude='tests'),
    test_suite = 'tests',
    entry_points = {
        'console_scripts': [
            'last_five=last_five.command:main',
            'tail_five=last_five.tail_command:main'
        ]
    }
)
