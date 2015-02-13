from setuptools import setup

setup(
    name='rumrunner',
    version='0.5.2',
    description='Client to send metrics to Speakeasy server',
    author='Eric Wong',
    py_modules=['rumrunner'],
    install_requires=[
        'pyzmq',
        'simplejson',
    ],
    url='https://github.com/etdub/rumrunner',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
)
