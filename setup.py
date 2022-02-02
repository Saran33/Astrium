from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
	
setup(
    name='astrium',
    packages=find_packages(include=['astrium']),
    version='0.1',
	author='Saran Connolly',
    description='PWE Capital Astrium - market analysis dashboard.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/PWE-Capital/astrium",
    project_urls={
        "Bug Tracker": "https://github.com/PWE-Capital/astrium/issues",
    },
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires = [
        'Django==3.2.4', 'channels==3.0.3', 'celery==5.0.5', 'django-celery-beat==2.2.0',
        'django-celery-results==2.0.1', 'redis==3.5.3', 'channels-redis==3.2.0', 'asyncio==3.4.3',
        'simplejson==3.17.2',
        'django_plotly_dash @ git+https://github.com/Saran33/django-plotly-dash.git@1.6.6#egg=django_plotly_dash',
        'pwe @ git+https://github.com/Saran33/pwe_analysis', 'yahoo_fin', 'yfinance',
        # 'dash', 'dash-bootstrap-components',
],
	#package_dir={"": "src"},
    #packages=find_packages(where="astrium"),
    python_requires=">=3.8",
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)