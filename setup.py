from pathlib import Path
import setuptools

if Path('./README.md').exists():
    with open ('README.md') as fh:
        long_description = fh.read()
else:
    long_description = ''
    
setuptools.setup(
    name='nea_ssoAuth',
    version='0.1.0',
    author='Jason M. Cherry',
    author_email='JCherry@gmail.com',
    description='New Eden Analytics Toolkit - SSO Authorizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Calvinxc1/NEA-SsoAuth',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask >= 1.1, < 2',
        'flask-restful >= 0.3, < 1',
        'gunicorn >= 20.0, < 21',
        'pandas >= 1.0, < 2',
        'pymongo >= 3.10, < 4',
        'python-jose >= 3.1, < 4',
        'requests >= 2.23, < 3',
        'tqdm >= 4.45, < 5',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
    ],
    python_requires='>= 3.6',
)