'''
The build plugin is used to execute the build routines for non-python components
'''
# Import python libs
import os
import shutil
import subprocess
import tempfile
import logging

log = logging.getLogger(__name__)


def make(hub, bname):

    opts = hub.popbuild.BUILDS[bname]
    build = opts['build']
    if not build:
        return
    hub.popbuild.BUILDS[bname]['binaries'] = []
    bdir = tempfile.mkdtemp()
    cur_dir = os.getcwd()
    os.chdir(bdir)
    for proj, conf in build.items():
        print(f'{proj}: {conf}')
        if 'make' in conf:
            for cmd in conf['make']:
                subprocess.call(cmd, shell=True)
        if 'src' in conf and 'dest' in conf:
            srcs = conf['src']
            dest = os.path.join(opts['venv_dir'], conf['dest'])
            print(f'Copying: {srcs}->{dest}')
            if not isinstance(srcs, list):
                srcs = [srcs]
            for src in srcs:
                if os.path.isfile(src):
                    shutil.copy(src, dest)
                    hub.popbuild.BUILDS[bname]['binaries'].append((os.path.join(dest, os.path.basename(src)), '.'))
                elif os.path.isdir(src):
                    shutil.copytree(src, dest)
    os.chdir(cur_dir)
