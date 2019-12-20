'''
Test the build process and execute the resulting binary to ensure correct output
'''
# Import python libs
import os
import sys
import subprocess
import shutil
# Import pop libs
import pop.hub
# Import third party libs
import yaml


def test_build():
    hub = pop.hub.Hub()
    hub.pop.sub.add('popbuild.popbuild')
    cdir = os.path.dirname(__file__)
    build_dir = os.path.join(cdir, 'build')
    dist_dir = os.path.join(cdir, 'dist')
    pb_bin = os.path.join(dist_dir, 'pb')
    pdir = os.path.join(cdir, 'pb')
    conf = os.path.join(pdir, 'pb.yml')
    # we need the develop pyinstaller for python 3.8 right now
    if sys.version_info.minor > 7:
        dev_pyinst = True
    else:
        dev_pyinst = False
    with open(conf) as rfh:
        cdata = yaml.safe_load(rfh.read())
    hub.popbuild.init.builder(
            'pb',
            'requirements.txt',
            False,
            'exclude.txt',
            os.path.join(cdir, 'pb'),
            dev_pyinst,
            cdata['build'],
            )
    cp = subprocess.run(pb_bin, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert b'pb works!' in cp.stdout
    assert b'libsodium works!' in cp.stdout
    shutil.rmtree(dist_dir)
    shutil.rmtree(build_dir)
