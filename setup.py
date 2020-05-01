from distutils.core import setup

setup(
    name='fuzzy_lib',
    packages=['fuzzy_lib'],
    version='0.3',
    license='MIT',
    description='Fuzzy logic library containing modifiers for making fuzzy_lib database queries',
    author='Aisultan Kali',
    author_email='aisultan.kali@gmail.com',
    url='https://github.com/akali/fuzzy',
    download_url='https://github.com/akali/fuzzy/archive/0.3.tar.gz',
    keywords=['fuzzy_lib', 'modifier', 'hedge', 'query', 'database'],
    install_requires=[
        "pandas==1.0.3",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
