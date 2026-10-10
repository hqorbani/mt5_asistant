from setuptools import setup, find_packages

setup(
    name="mt5_assistant",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ttkbootstrap>=1.0.0",
        "MetaTrader5",
    ],
    entry_points={
        'console_scripts': [
            'mt5_assistant = frontend.app:main',
        ],
    },
)