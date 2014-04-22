from distutils.core import setup

setup(name='rumrunner',
    version='0.0.5',
    description='Client to send metrics to Speakeasy server',
    author='Eric Wong',
    py_modules=['rumrunner'],
    install_requires = [
        'pyzmq',
        'ujson',
    ]
    )
