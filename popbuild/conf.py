CLI_CONFIG = {
        'config': {
            'options': ['-c'],
            'default': '',
            'help': 'Load extra options from a configuration file, this is useful when the project needs to use more advanced features like compiling c binaries into the environment.',
            },
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
        'onedir': {
            'default': False,
            'action': 'store_true',
            'help': 'Instead of producing a single binary produce a directory with all components',
            },
        'pyenv': {
            'default': 'system',
            'help': 'Set the python version to build with, if not present the system python will be used. Only use CPython versions, to see available versions run `pyenv install --list | grep " 3\.[6789]"`',
            },
        }
CONFIG = {
        'build': {
            'default': False,
            'help': '''Enter in commands to build a non-python binary into the deployed binary.
            The build options are set on a named project basis. This allows for multiple shared
            binaries to be embedded into the final build:
            
            build:
              libsodium:
                make:
                   - wget libsodium
                   - tar xvf libsodium*
                   - cd libsodium
                   - ./configure
                   - make
                src: libsodium/libsodium.so
                dest: lib64/
                '''
            },
        }
GLOBAL = {}
SUBS = {}
DYNE = {}
