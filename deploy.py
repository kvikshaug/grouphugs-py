#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import check_call, check_output
from os.path import dirname
import os
import logging as log

from config import DEPLOY_HOST, DEPLOY_PATH

def check_call_remote(command, **kwargs):
    return check_call(['ssh', DEPLOY_HOST, command], **kwargs)

if __name__ == '__main__':
    log.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=log.INFO)

    os.chdir(dirname(__file__))

    head = check_output(['git', 'rev-parse', '--short=8', 'HEAD']).decode('UTF-8').strip()
    log.info('Creating archive for {}'.format(head))
    release = 'grouphugs-py-{}'.format(head)
    archive = '{}.tar.gz'.format(release)
    check_call(['git', 'archive', '--output={}'.format(archive), head])

    log.info('Deploying {}'.format(archive))
    check_call(['scp', archive, "{0}:{1}/packages".format(DEPLOY_HOST, DEPLOY_PATH)])
    os.remove(archive)

    log.info('Extracting {}'.format(archive))
    check_call_remote('mkdir -p releases/{}'.format(release))
    check_call_remote(
        'tar  --directory=releases/{0} -xf packages/{1}'.format(release, archive))

    log.info('Bootstrapping python environment')
    check_call_remote('releases/{}/bootstrap.sh'.format(release))

    log.info('Running database migrations')
    check_call_remote('cd current && env/bin/alembic upgrade head')
