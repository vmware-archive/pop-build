'''
Create and manage the venvs used for build environments
'''
# Import python libs
import venv
import os
import subprocess

OMIT = ('__pycache__', 'PyInstaller', 'pip', 'setuptools', 'pkg_resources', '__pycache__', 'dist-info', 'egg-info')


def bin(hub, bname):
    '''
    Ensure that the desired binary version is present and return the path to
    the python bin to call
    '''
    opts = hub.popbuild.BUILDS[bname]
    root = subprocess.run('pyenv root', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip().decode()
    avail = set()
    for line in subprocess.run('pyenv versions', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip().decode().split('\n'):
        avail.add(line.strip())
    if opts['pyenv'] not in avail:
        subprocess.run(f'env PYTHON_CONFIGURE_OPTS="--enable-shared --enable-ipv6" pyenv install {opts["pyenv"]}', shell=True)
    return os.path.join(root, 'versions', opts['pyenv'], 'bin', 'python')


def create(hub, bname):
    '''
    Make a virtual environment based on the version of python used to call this script
    '''
    opts = hub.popbuild.BUILDS[bname]
    if opts['pyenv'] == 'system':
        venv.create(opts['venv_dir'], clear=True, with_pip=True, system_site_packages=opts['sys_site'])
    else:
        env_bin = hub.popbuild.venv.bin(bname)
        cmd = f'{env_bin} -m venv {opts["venv_dir"]} --clear '
        if opts['sys_site']:
            cmd += '--system-site-packages'
        subprocess.run(cmd, shell=True)
    if opts['is_win']:
        py_bin = os.path.join(opts['venv_dir'], 'Scripts', 'python')
    else:
        py_bin = os.path.join(opts['venv_dir'], 'bin', 'python3')
    pip_cmd = f'{py_bin} -m pip '
    # I am hardcoding this in for now, it should be removed when Python 3.8 has been out longer
    subprocess.run(f'{pip_cmd} install distro', shell=True)
    subprocess.run(f'{pip_cmd} install -r {opts["req"]}', shell=True)
    if os.path.isfile(os.path.join(opts['dir'], 'setup.py')):
        subprocess.run(f'{pip_cmd} install {opts["dir"]}', shell=True)
    # Install old pycparser to fix: https://github.com/eliben/pycparser/issues/291 on Windows
    if opts['is_win']:
        subprocess.run(f'{pip_cmd} install pycparser==2.14', shell=True)
    if opts['dev_pyinst']:
        # Install development version of pyinstaller to run on python 3.8
        subprocess.run(f'{pip_cmd} install https://github.com/pyinstaller/pyinstaller/tarball/develop', shell=True)
    else:
        subprocess.run(f'{pip_cmd} install PyInstaller==3.6', shell=True)
    subprocess.run(f'{pip_cmd} uninstall -y -r {opts["exclude"]}', shell=True)


def _omit(test):
    for bad in OMIT:
        if bad in test:
            return True
    return False


def _to_import(path):
    ret = path[path.index('site-packages') + 14:].replace(os.sep, '.')
    if ret.endswith('.py'):
        ret = ret[:-3]
    return ret


def _to_data(path):
    dest = path[path.index('site-packages') + 14:]
    src = path
    if not dest.strip():
        return None
    ret = f'{src}{os.pathsep}{dest}'
    return ret


def scan(hub, bname):
    '''
    Scan the new venv for files and imports
    '''
    opts = hub.popbuild.BUILDS[bname]
    for root, dirs, files in os.walk(opts['vroot']):
        if _omit(root):
            continue
        for d in dirs:
            full = os.path.join(root, d)
            if _omit(full):
                continue
            opts['all_paths'].add(full)
        for f in files:
            full = os.path.join(root, f)
            if _omit(full):
                continue
            opts['all_paths'].add(full)


def mk_adds(hub, bname):
    '''
    Make the imports and datas for pyinstaller
    '''
    opts = hub.popbuild.BUILDS[bname]
    for path in opts['all_paths']:
        if not 'site-packages' in path:
            continue
        if os.path.isfile(path):
            if not path.endswith('.py'):
                continue
            if path.endswith('__init__.py'):
                # Skip it, we will get the dir
                continue
            imp = _to_import(path)
            if imp:
                opts['imports'].add(imp)
        if os.path.isdir(path):
            data = _to_data(path)
            imp = _to_import(path)
            if imp:
                opts['imports'].add(imp)
            if data:
                opts['datas'].add(data)
