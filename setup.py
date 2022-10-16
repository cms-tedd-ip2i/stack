from setuptools import setup, find_packages

setup(
    name="tracker_dcs_stack",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'influxdb-client',
    ],    
)
