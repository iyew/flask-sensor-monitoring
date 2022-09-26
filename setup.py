from setuptools import find_packages, setup

setup(
    name='monitoring',
    version='1.0.0',
    description='Monitoring sensors',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pyserial',
        'pymysql'
    ],
)
