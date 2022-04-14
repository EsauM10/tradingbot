from setuptools import setup, find_packages


setup(
    name="tradingbot",
    version="1.0",
    packages=find_packages(),
    description="A scalable bot where you can create custom trading strategies",
    long_description="A scalable bot where you can create custom trading strategies",
    keywords=["technical analysis", "ta", "trading", "bot", "iqoption"],
    url="https://github.com/EsauM10/tradingbot",
    author="Esaú Mascarenhas",
    author_email="esaumasc@gmail.com",
    packages=["trading"],
    install_requires=["numpy"],
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ]
)