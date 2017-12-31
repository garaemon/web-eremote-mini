#!/usr/bin/env python
# script to deploy codes

import os
import subprocess

import fire

PYENV_INSTALLER_URL = 'https://raw.githubusercontent.com/' + \
    'pyenv/pyenv-installer/master/bin/pyenv-installer'

PYENV_SETUP_COMMANDS = [
    'export PATH="$HOME/.pyenv/bin:$PATH"', 'eval "$(pyenv init -)"',
    'eval "$(pyenv virtualenv-init -)"'
]

NVM_INSTALL_URL = 'https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh'

NVM_SETUP_COMMANDS = [
    'source ~/.nvm/nvm.sh',
]


def install_pyenv(hostname):
    'Install pyenv on remote host via ssh'
    print('> Installing pyenv')
    subprocess.check_call(['ssh', hostname, 'curl -L %s | bash' % PYENV_INSTALLER_URL])


def install_nvm(hostname):
    'Install nvm on remote host via ssh'
    print('> Installing nvm')
    subprocess.check_call(['ssh', hostname, 'curl -o- %s | bash' % NVM_INSTALL_URL])


def concatenate_shell_commands(commands, separator=';'):
    'Concatenate multiple shell command'
    return ''.join([c + separator for c in commands])


def install_python(hostname, version='3.5.2'):
    'Install python using pyenv on remote host'
    commands = PYENV_SETUP_COMMANDS + [
        'pyenv install %s -s' % version,
        'pyenv global %s' % version,
        'pip install -U virtualenv',
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def install_node(hostname, version='8.9.3'):
    'Install python using pyenv on remote host'
    commands = NVM_SETUP_COMMANDS + [
        'nvm install %s' % version,
        'nvm use %s' % version,
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def deploy_source_code(hostname, target_directory):
    'Copy source code to remote host'
    exclude_directories = [
        '.venv',
        '.idea',
        '.git',
        '__pycache__',
        '*.pyc',
        'node_modules',
        'bower_components',
        'ts_build',
    ]
    from_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    exclude_options = ['--exclude=%s' % d for d in exclude_directories]
    subprocess.check_call(
        ['rsync', '-avz'] + exclude_options +
        [from_directory + '/', '%s:%s/' % (hostname, target_directory)])


def build_python_code(hostname, target_directory):
    'Build python code using `python setup.py develop` on remote host'
    # install libleveldb-dev is required
    commands = PYENV_SETUP_COMMANDS + [
        'cd %s' % target_directory,
        'test -d .venv || virtualenv .venv',
        'source .venv/bin/activate',
        'python setup.py develop',
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def copy_environmental_variables(hostname, target_directory):
    envs = ['LOGGLY_TOKEN']
    content = ';'.join(['export %s=%s' % (env, os.environ[env]) for env in envs])
    commands = ['cd %s' % target_directory, 'echo "%s" > setup.sh' % content]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def setup_systemd(hostname, target_directory):
    'Prepare user-local systemd setting'
    service_file = 'tools/web-eremote-mini.service'
    sed_command = 'sed -e s+@PROJECT_DIR@+${PWD}+g -i %s' % (service_file)
    commands = [
        'cd %s' % target_directory,
        sed_command,
        'mkdir -p ${HOME}/.config/systemd/user/',
        # Be careful, symbolic link of .service file does not work.
        'cp ${PWD}/%s ${HOME}/.config/systemd/user/' % service_file,
        'systemctl --user daemon-reload',
        'systemctl --user enable web-eremote-mini',
        'systemctl --user restart web-eremote-mini',
    ]
    print(concatenate_shell_commands(commands))
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def install_npm_packages(hostname, target_directory):
    commands = NVM_SETUP_COMMANDS + [
        'cd %s' % target_directory,
        'npm install',
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def build_polymer(hostname, target_directory):
    commands = NVM_SETUP_COMMANDS + [
        'cd %s' % target_directory,
        'npm run bower install',
        'npm run gulp',
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def main_impl(hostname, target_directory):
    'Main function'
    print('> Start deploying to %s' % hostname)
    install_pyenv(hostname)
    install_python(hostname)
    install_nvm(hostname)
    install_node(hostname)
    install_npm_packages(hostname, target_directory)
    deploy_source_code(hostname, target_directory)
    build_python_code(hostname, target_directory)
    build_polymer(hostname, target_directory)
    copy_environmental_variables(hostname, target_directory)
    setup_systemd(hostname, target_directory)
    print('Please run `sudo loginctl enable-linger ${USER}` to enable auto start')


def main():
    'Entry point for command line usage'
    os.environ['LANG'] = 'C'
    os.environ['LC_ALL'] = 'C'
    fire.Fire(main_impl)


if __name__ == '__main__':
    main()
