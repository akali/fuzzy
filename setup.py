from distutils.core import setup
setup(
    name = 'fuzzy_lib',         # How you named your package folder (MyLib)
    packages = ['fuzzy_lib'],   # Chose the same as "name"
    version = '0.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Fuzzy logic library containing hedges for making fuzzy_lib database queries',   # Give a short description about your library
    author = 'Aisultan Kali',                   # Type in your name
    author_email = 'aisultan.kali@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/akali/fuzzy',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/akali/fuzzy/archive/0.1.tar.gz',    # I explain this later on
    keywords = ['fuzzy_lib', 'hedge', 'query', 'database'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.8',
    ],
)
