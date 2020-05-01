from distutils.core import setup

setup(
    name='CWiPy',
    packages=['CWiPy'],
    version='0.4',
    license='MIT',
    description='Computing with words library',
    author='Aisultan Kali',
    author_email='aisultan.kali@gmail.com',
    url='https://github.com/akali/fuzzy',
    download_url='https://github.com/akali/fuzzy/archive/0.4.tar.gz',
    keywords=['fuzzy', 'quantifier', 'very', 'expressive', 'CWiPy', 'modifier', 'hedge', 'query', 'database'],
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
