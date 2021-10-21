from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'smart-shell',
    version = '0.0.3',
    author = 'Joe McAllister',
    author_email = 'joseph.l.mcallister+smart-shell@gmail.com',
    license = 'GNU GENERAL PUBLIC LICENSE',
    description = 'AI command line tools',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/joseph-mcallister/smart-shell',
    py_modules = ['client'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        plz=client:main
        smart_shell=client:main
    '''
)