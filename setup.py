import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = map(str.strip, requirements_file.readlines())

setuptools.setup(
    name="emails-gdpr",
    version="1.0.3",
    author="Damian P.",
    author_email="an0o0nyme@gmail.com",
    description="",
    keywords="emails gdpr data protection",
    install_requires=list(requirements),
    license="MIT license",
    long_description=long_description + '\n\n' + history,
    long_description_content_type="text/markdown",
    url="https://github.com/an0o0nym/emails-gdpr",
    packages=setuptools.find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Natural Language :: English',
    ],
    entry_points = {
        'console_scripts': [
            'emails-gdpr=emails_gdpr.main:main',
        ],
    }
)