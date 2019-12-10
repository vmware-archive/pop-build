# Import python libs
import os
import shutil


def report(hub, bname):
    opts = hub.popbuild.BUILDS[bname]
    art = os.path.join('dist', opts['name'])
    print(f'Executable created in {art}')


def clean(hub, bname):
    opts = hub.popbuild.BUILDS[bname]
    shutil.rmtree(opts['venv_dir'])
    os.remove(opts['spec'])
    os.remove(opts['req'])
