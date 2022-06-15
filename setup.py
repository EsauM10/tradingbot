from setuptools import setup, find_packages


setup(
    name="tradingbot",
    version="1.2.2",
    packages=find_packages(),
    description="A scalable bot where you can create custom trading strategies",
    long_description="A scalable bot where you can create custom trading strategies",
    keywords=["technical analysis", "ta", "trading", "bot", "iqoption"],
    url="https://github.com/EsauM10/tradingbot",
    author="Esaú Mascarenhas",
    author_email="esaumasc@gmail.com",
    install_requires=[
        "numpy",
        "iqoptionapi @ https://github.com/iqoptionapi/iqoptionapi/tarball/master#egg=iqoptionapi"
    ],
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ]
)