import pip
import setuptools
import sunrice as target

with open('requirements.txt', 'r') as f:
    requirements = f.read()

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name=target.__name__,
    version=target.__version__,
    author='Pavel Hübner',
    author_email='pavel.hubner@gmail.com',
    description=target.__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hubpav/sunrice',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    keywords='lighting mqtt iot',
    platforms='any',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            '%s=%s:main' % (target.__name__, target.__name__)
        ]
    }
)
