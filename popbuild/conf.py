CLI_CONFIG = {
        'name': {
            'options': ['-n'],
            'default': None,
            'help': 'The name of the project to build',
            },
        'directory': {
            'options': ['-D', '--dir'],
            'default': '.',
            'help': 'The path to the directory to build from',
            },
        'requirements': {
            'options': ['-r'],
            'default': 'requirements.txt',
            'help': 'The name of the requirements.txt file to use',
            },
        'exclude': {
            'options': ['-e'],
            'default': 'exclude.txt',
            'help': 'The path to the exclude file, these python packages will be uninstalled',
            },
        'system_site': {
            'options': ['-S'],
            'default': False,
            'action': 'store_true',
            'help': 'Include the system site-packages when building. This is needed for builds from custom minstalls of Python',
            },
        'dev_pyinstaller': {
            'options': ['--dev-pyinst'],
            'default': False,
            'action': 'store_true',
            'help': 'Use the latest development build of PyInstaller. This can fix issues on newer versions of python not yet supported by mainline releases.',
            },
        }
CONFIG = {}
GLOBAL = {}
SUBS = {}
DYNE = {}
