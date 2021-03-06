from setuptools import setup, find_packages


with open('README.rst') as readme:
    next(readme)
    long_description = ''.join(readme).strip()

with open('requirements.txt') as requirements:
    install_requires = [line.strip() for line in requirements]


setup(
    name='NoahsArk',
    version='0.5.4',
    author="shonenada",
    author_email="shonenada@gmail.com",
    url="https://github.com/N402/NoahsArk",
    description="Something you should do right now or never",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points= {
        'console_scripts': 'ark-admin = ark.management:execute_command_line'
    },
    classifiers=[
        'Private :: Do Not Upload',
    ]
)
