from setuptools import setup

setup(name='rumrunner',
    version='0.0.9',
    description='Client to send metrics to Speakeasy server',
    author='Eric Wong',
    py_modules=['rumrunner'],
    install_requires=[
        'pyzmq',
        'simplejson',
    ],
    )
