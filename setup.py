from setuptools import setup, find_packages

setup(
    name='js-finding',
    version='1.002',
    description='A tool to extract JS files from given domains',
    author='pikpikcu',
    author_email='N/A',
    url='http://github.com/pikpikcu/js-finding',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyfiglet',
        'colorama',
        'PySocks',
    ],
    entry_points={
        'console_scripts': [
            'jsfind=core.main:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
