from setuptools import setup

setup(
    name='pyvault',
    version='0.1',
    py_modules=['pyvault'],
    install_requires=[
        'Click',
        'pyyaml',
        'hvac',
    ],
    entry_points='''
        [console_scripts]
        pyvault=pyvault:cli
    ''',
)

