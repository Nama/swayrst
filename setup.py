from setuptools import setup

setup(
    name='swayrst',
    version='1.3',
    packages=['swayrst'],
    scripts=['swayrst/swayrst.py'],
    url='https://github.com/Nama/swayrst',
    license='MIT',
    author='Yama',
    author_email='',
    description='Restore workspaces in sway to displays and move applications to saved workspaces.',
    entry_points={
        'console_scripts': [
            'swayrst = swayrst:main',
        ]
    }
)
