# -*- mode: python; coding: utf-8; -*-
import posixpath
import os
import re
import sys
import fabtools
from fabtools.files import is_dir, is_link, is_file
from fabtools.require import nginx, deb, python, files, git
from fabric.contrib.console import confirm as confirm_global
from fabric.contrib.files import exists
from fabric.api import *
import json

__author__ = 'jbo'

# settings
from fabsettings import DEPLOY_DEFAULT_DOMAIN, DEPLOY_DEFAULT_REPOSITORY, PROJECT_PASWD, BITBUCKET_PASSWORD, BITBUCKET_USER, VIRT_NAME, PROJECTS_ROOT, PROJECT_USER, VIRT_HOME
# end


env.lcwd = os.path.abspath(os.path.dirname(__file__))

#with open('./conf/environment.json') as f:

#env.project_group = PROJECT_USER
env.no_input_mode = False
env.virt = VIRT_NAME
env.project_dir_name = PROJECTS_ROOT
env.new_user_default = 'test'
env.new_passwd_default = 'test'
env.venv_default = 'prod'
env.pyver_default = '2.7.3'
#env.v_format = '/usr/local/pythonbrew/venvs/Python-2.7.3/{0}'.format(env.virt)
env.virt_home = '.virtualenvs'
env.python_dir = '/usr/local/pythonbrew/venvs/Python-'
env.v_format = '{1}/{0}'.format(env.virt, VIRT_HOME)
env.home_user = '/opt/www'
project_virt = VIRT_NAME
env.project_default = 'test'
env.domain_default = DEPLOY_DEFAULT_DOMAIN
env.repository_default = DEPLOY_DEFAULT_REPOSITORY


with open('./conf/environment.json') as f:
    conf = json.load(f)

env.debug = conf.get('debug', False)
env.pyver = '2.7.3'
try:
    env.config = json.load(open('./conf/deploy.json'))
    env.user = env.config['id']
    env.password = env.config['passwd']
    env.repository = env.config['www']['repository']
except Exception, e:
    env.user = conf.get('DEPLOY_USER', PROJECT_USER)
    env.password = conf.get('DEPLOY_PASSWORD', PROJECT_PASWD)
    #raise e

env.hosts = conf.get('DEPLOY_HOSTS')
try:
    env.home_dir = posixpath.join(env.home_user, env.config['passwd'])
    env.project_root = posixpath.join(env.home_user, env.config['id'], env.config['www']['approot'])
    env.root = posixpath.join(env.home_user, env.config['id'], env.config['www']['approot'], 'current')
    env.shared = posixpath.join(env.home_user, env.config['id'], env.config['www']['approot'], 'shared')
except Exception, e:
    pass


def virt_comm(command):
    #local("/bin/bash -l -c 'source /usr/local/pythonbrew/venvs/Python-2.7.3/{0}/bin/activate && {1}'".format(env.virt, command))
    #local('source /usr/local/pythonbrew/venvs/Python-3.3.0/{0}/bin/activate && {1}'.format(env.virt, command))
    if sys.platform == 'darwin':
        local('source ~/.virtualenvs/{0}/bin/activate && {1}'.format(env.virt, command))
    else:
        local("/bin/bash -l -c '{0}/bin/activate && {1}'".format(env.v_format, command))


@task
def m(dj_command='-h'):
    """
    Run django manage command EXAMPLE: fab m:show_urls
    """
    with lcd(env.lcwd):
        virt_comm('python ./manage.py {0}'.format(dj_command).replace('/', os.path.sep))


@task
def pi(r_file='prod'):
    """
    Run pip install ARG prod,dev EXAMPLE: fab pi:dev
    """
    with lcd(env.lcwd):
        virt_comm('pip install -r ./requirements/{0}.txt'.format(r_file))


@task
def pu(r_file='prod'):
    """
    Run pip install -U ARG prod,dev EXAMPLE: fab pi:dev
    """
    with lcd(env.lcwd):
        virt_comm('pip install -U -r ./requirements/{0}.txt'.format(r_file))


@task
def test(c_param='local'):
    if c_param == 'local':
        with lcd(env.lcwd):
            for mcom in conf.get('MANAGER_COMMAND_TEST'):
                virt_comm('python ./manage.py {0}'.format(mcom).replace('/', os.path.sep))


@task
def sh(lookup_param='python'):
    if lookup_param == 'python':
        run('pybrew list')
    elif lookup_param == 'pip':
        run('pip --version')


@task
def c():
    with lcd(env.lcwd):
        local('git add . && git commit')
        local('git push')


@task
def u(c_param='prod'):
    if c_param == 'local':
        with lcd(env.lcwd):
            if not is_dir('{0}/public/static'.format(env.lcwd)):
                #files.directory('{0}/public/static'.format(env.lcwd), mode='755')
                files.directory('public/static'.format(env.lcwd))

            for mcom in conf.get('MANAGER_COMMAND_RUN'):
                virt_comm('python ./manage.py {0}'.format(mcom).replace('/', os.path.sep))
    else:
        with cd(env.root):
            # if not is_dir('{0}/public/static'.format(env.project_dir_name)):
            #     files.directory('{0}/public/static'.format(env.project_dir_name), use_sudo=True, owner=env.project_user,
            #                     group=env.project_group, mode='755')
            #     sudo(
            #         'chown -R ' + env.project_user + ':' + env.project_group + ' db* log* public/static* public/media*')
            
            env.virt = posixpath.join(env.home_dir, env.virt_home, conf[lookup_param]['venv'])
            with prefix('pythonbrew use {0}'.format(env.pyver)):
                # django comands
                with fabtools.python.virtualenv(env.virt):
                    for mcom in conf.get('MANAGER_COMMAND_RUN'):
                        run('python ./manage.py {0}'.format(mcom))
                #sudo('python ./manage.py collectstatic -v 0 --clear --noinput', user=env.project_user)
                #sudo('python ./manage.py compress --force', user=env.project_user)
                #sudo('python ./manage.py syncdb --noinput --migrate', user=env.project_user)
                #sudo('python src/manage.py loaddata fixtures.json', user=env.project_user)


@task
def t(t_param='prod'):
    env.project_dir_name = conf[t_param]['PROJECTS_ROOT']
    with cd(env.project_dir_name):
        with fabtools.python.virtualenv('/usr/local/pythonbrew/venvs/Python-3.3.0/{0}'.format(t_param)):
            run('python -V')


@task
def libs(lookup_param='prod', pip='install'):
    with cd(env.home_dir):
        # pip cache
        pip_cache_dir = posixpath.join(env.shared, '.pip.cache')
        with cd(env.root):
            try:
                env.pyver = conf[lookup_param]['version']
            except:
                pass
            env.virt = posixpath.join(env.home_dir, env.virt_home, conf[lookup_param]['venv'])
            with prefix('pythonbrew use {0}'.format(env.pyver)):
                run('python -V')
                with fabtools.python.virtualenv(env.virt):
                    fabtools.python_distribute.install(conf[lookup_param]['distribute'])
                    python.install_requirements(conf[lookup_param]['requirement'], use_mirrors=False, download_cache=pip_cache_dir)


@task
def deploy(lookup_param='prod', pip='install'):
    with cd(env.home_dir):
        files.directory(env.project_root, mode='750')
        files.directory(env.shared, mode='750')
        with cd(env.shared):
            files.directory('.pip.cache', mode='750')
            files.directory('db', mode='750')
            files.directory('log', mode='750')
            files.directory('pids', mode='750')
            files.directory('system', mode='750')
            files.directory('media', mode='750')
    with cd(env.project_root):
        git.working_copy(env.repository, env.root, branch=env.config['www']['branch'])
        with cd(env.root):
            if not exists('db'):
                run('ln -s {0}/{1} {2}/'.format(env.shared, 'db', env.root))
            if not exists('log'):
                run('ln -s {0}/{1} {2}/'.format(env.shared, 'log', env.root))
            if not exists('public/media'):
                run('ln -s {0}/{1} {2}/public/'.format(env.shared, 'media', env.root))
            execute(libs, lookup_param=lookup_param, pip=pip)
    #execute(compile, c_param=d_param)


@task
def create(venv=None, pyver=None):
    deb.packages(['libjpeg8', 'libjpeg8-dev', 'libfreetype6', 'libfreetype6-dev', 'zlib1g-dev'])
    validate = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    if not env.get("new_user"):
        if env.no_input_mode:
            env.new_user = env.new_user_default
        else:
            prompt("User: ", "new_user", env.get('new_user_default', ''), validate=validate)

    if not fabtools.user.exists(env.new_user):
        prompt("Password for {0}: ".format(env.new_user), "new_passwd", '', validate=validate)
        env.home_dir = '{0}/{1}'.format(env.home_user, env.new_user)
        fabtools.user.create(env.new_user, home=env.home_dir, group=env.new_user, create_home=True, system=False,
                             shell='/bin/bash', create_group=True, password=env.new_passwd)

    if not env.get("project"):
        if env.no_input_mode:
            env.project = env.project_default
        else:
            prompt("Project name: ", "project", env.get('project_default', ''))

    if not env.get("repository"):
        if env.no_input_mode:
            env.repository = env.repository_default
        else:
            prompt("Deploy from: ", "repository", env.get('repository_default', ''))

    if not env.get("domain"):
        if env.no_input_mode:
            abort("Need set env.domain !")
        else:
            prompt("Project DNS url: ", "domain", env.get('domain_default', ''), validate=validate)
    else:
        if not re.findall(validate, env.domain):
            abort("Invalid env.domain !")

    require('repository', 'domain', 'project')
    if venv is not None:
        env.venv = venv
    else:
        prompt("Virtual ENV: ", "venv", env.get('venv_default', ''), validate=validate)
    if pyver is not None:
        env.pyver = pyver
    else:
        prompt("Python VERSION: ", "pyver", env.get('pyver_default', ''), validate=validate)
    env.virt = '{0}/{1}/{2}'.format(env.home_user, env.new_user, env.virt_home)
    pyver_dir = '{0}{1}/{2}-{3}'.format(env.python_dir, env.pyver, env.new_user, env.venv)
    files.directory(env.virt, mode='750', owner=env.new_user, group=env.new_user, use_sudo=True)
    if not is_dir(posixpath.join(env.virt, env.venv)):
        with prefix('pythonbrew use {0}'.format(env.pyver)):
            if not is_dir(pyver_dir):
                sudo('pythonbrew venv create {0}-{1}'.format(env.new_user, env.venv))
                sudo('ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so {0}/lib/'.format(pyver_dir))
                sudo('ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so {0}/lib/'.format(pyver_dir))
                sudo('ln -s /usr/lib/x86_64-linux-gnu/libz.so {0}/lib/'.format(pyver_dir))
            sudo("find {2}/venvs/ -type d -iname '{1}-{0}' -print0 | xargs -I{3} -0 chown -R --preserve-root --no-dereference {1}:pythonbrew '{3}'".format(env.venv, env.new_user, '${PYTHONBREW_ROOT}', '{}'))
            sudo('ln -s {0} {1}/'.format(pyver_dir, env.virt))
            sudo('chown -R {0}:{0} {1}'.format(env.new_user, env.virt))

    #with cd(env.home_dir):
    #    # pip cache
    #    files.directory('.pip.cache', use_sudo=True, owner='deploy', group='deploy', mode='755')
    #    #pip_cache_dir = posixpath.join(PROJECTS_ROOT, '.pip.cache')
    #execute(libs, lookup_param=d_param)
    #execute(compile, c_param=d_param)


def push():
    """
    This function for create django site project work flow on remote server.
    Django site source cloning from remote git repository.

    NOTE: This function may be used in other fab file.
    For this need setup global `env` dict.

    **`env` settings**
    env.user - deploy user name (use for ssh)
    env.password - deploy user password (use for ssh)
    env.hosts - list deploy hosts (use for ssh)

    env.domain - django site domain (DNS) use for:
        - nginx settings
        - uWSGI start user
        - project dir name

    env.repository - remote git repository url, use for git clone site source

    env.no_input_mode - in this variable True use no input deploy mode.
        If no_input_mode==True using follow strategy:
            Abort if env.domain (env.repository) value not set or invalid.
            And using default confirm() value if needed.

    """
    # cwd => ./deploy
    env.lcwd = os.path.abspath(os.path.dirname(__file__))

    require('no_input_mode')

    #env.no_input_mode = False
    if env.no_input_mode:
        def confirm_local(question, default=True):
            puts(question)
            puts("Use no_input_mode [default: {0}]".format("Y" if default else "N"))
            return default

        confirm = confirm_local
    else:
        confirm = confirm_global

    validate = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    if not env.get("domain"):
        if env.no_input_mode:
            abort("Need set env.domain !")
        else:
            prompt("Project DNS url: ", "domain", env.get('domain_default', ''), validate=validate)
    else:
        if not re.findall(validate, env.domain):
            abort("Invalid env.domain !")

    if not env.get("repository"):
        if env.no_input_mode:
            env.repository = env.repository_default
        else:
            prompt("Deploy from: ", "repository", env.get('repository_default', ''))

    require('repository', 'domain')

    puts("Deploy site: {0} \nFrom: {1}".format(env.domain, env.repository))
    DOMAIN_WITHOUT_DOT = env.domain.replace('.', '_')

    env.project_user = DOMAIN_WITHOUT_DOT
    env.project_group = DOMAIN_WITHOUT_DOT
    env.project_dir_name = DOMAIN_WITHOUT_DOT
    env.root = posixpath.join(PROJECTS_ROOT, env.project_dir_name)

    env.debug = True

    deb.packages(['git'])

    files.directory(PROJECTS_ROOT, use_sudo=True, owner='root', group='root', mode='755')
    with cd(PROJECTS_ROOT):
        # pip cache
        files.directory('.pip.cache', use_sudo=True, owner='deploy', group='deploy', mode='755')
        pip_cache_dir = posixpath.join(PROJECTS_ROOT, '.pip.cache')

        # proj dir create
        if is_dir(env.project_dir_name) and confirm("proj dir exist! abort ?", default=False):
            return

        files.directory(env.project_dir_name, use_sudo=True, owner='root', group='root', mode='755')

        # proj user create
        if not fabtools.user.exists(env.project_user):
            fabtools.user.create(env.project_user, home=env.root, group=env.project_group, create_home=False,
                                 system=True, shell='/bin/false', create_group=True)

        # proj infrastructure
        with cd(env.project_dir_name):
            # proj source
            if not is_dir('src') or confirm("proj src exist! [rm all and re clone / git pull]?", default=False):
                files.directory('src', use_sudo=True, owner='deploy', group='deploy', mode='755')
                with cd('src'):
                    sudo('rm -Rf .??* *')
                    sudo('git clone {repository:s} .'.format(env), user='deploy')
            else:
                with cd('src'):
                    sudo('git pull', user='deploy')

            # proj virtual env
            if not is_dir('.virtualenvs') or confirm("proj venv dir exist! [rm all and recreate / repeat install]?",
                                                     default=False):
                files.directory('.virtualenvs', use_sudo=True, owner='deploy', group='deploy', mode='755')
                with cd('.virtualenvs'):
                    sudo('rm -Rf .??* *')

            python.virtualenv('.virtualenvs', use_sudo=True, user='deploy', clear=True)
            with fabtools.python.virtualenv('.virtualenvs'):
                python.install_requirements('src/requirements.txt', use_mirrors=False, use_sudo=True, user='deploy',
                                            download_cache=pip_cache_dir)

            # ------------------- #
            # WEB SERVER SETTINGS #
            # ------------------- #

            # I`m use nginx <-> uWSGI <-> Django

            nginx.server()
            deb.packages(['uwsgi', 'uwsgi-plugin-python'])

            # proj conf!
            if not is_dir('conf') or confirm("proj conf dir exist! [backup and update? / skip]", default=False):
                files.directory('conf', use_sudo=True, owner='root', group='root', mode='755')
                with cd('conf'):
                    local_conf_templates = os.path.join(os.path.dirname(__file__), 'template', 'conf')
                    uwsgi_conf = os.path.join(local_conf_templates, 'uwsgi.ini')
                    nginx_conf = os.path.join(local_conf_templates, 'nginx.conf')

                    sudo("rm -Rf *.back")
                    sudo("ls -d *{.conf,.ini} | sed 's/.*$/mv -fu \"&\" \"\\0.back\"/' | sh")
                    files.template_file('uwsgi.ini', template_source=uwsgi_conf, context=env,
                                        use_sudo=True, owner='root', group='root', mode='644')
                    files.file('reload', use_sudo=True, owner='root', group='root')
                    sudo('ln -sf $(pwd)/uwsgi.ini /etc/uwsgi/apps-enabled/' + env.project_dir_name + '.ini')

                    files.template_file('nginx.conf', template_source=nginx_conf, context=env,
                                        use_sudo=True, owner='root', group='root', mode='644')
                    sudo('ln -sf $(pwd)/nginx.conf /etc/nginx/sites-enabled/' + env.project_dir_name)

            sudo('service nginx restart')
            sudo('service uwsgi restart')

#def is_git():
#    with settings(hide('running', 'warnings', 'stderr', 'stdout'), warn_only=True):
#        res = run('git status')
#    return res.succeeded


def local_template_render(local_template, dict, local_target):
    local_file_template = os.path.join(os.path.dirname(__file__), 'template', local_template)
    local_out = os.path.join(env.lcwd, local_target)
    with open(local_file_template, 'r') as f:
        rendered = f.read().format(**dict)
        with open(local_out, 'w') as out:
            out.write(rendered)


BITBUCKET_AUTH = (BITBUCKET_USER, BITBUCKET_PASSWORD)


@task
def r(h_run='local'):
    """
    Run Server
    """
    env.debug = True
    if h_run == 'local':
        virt_comm('python ./manage.py runserver_plus'.replace('/', os.path.sep))
    else:
        with cd(env.project_dir_name):
            r_k = 'python ./manage.py runserver_plus {0}:{1}'.format(env.host, env.run_port)
            with fabtools.python.virtualenv(env.v_format):
                # django comands
                sudo(r_k, user=env.project_user)


@task
def init():
    # cwd => ./deploy
    env.lcwd = os.path.abspath(os.path.dirname(__file__))

    env.debug = True
    prompt("project domain: ", "project",
           validate="^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
    puts("create project: {0}".format(env.project))

    with lcd('..'):
        #local('mkdir ' + env.project)
        #with lcd(env.project):
        puts("Dir: {0}".format(env.lcwd))
        #with lcd(env.lcwd):
        with lcd(env.project):
            local('mkdir db log')
            #with lcd('src'):
            #    # copy proj infrastructure
            #    local('cp -r ../../deploy/project/* .'.replace('/', os.path.sep))
            #    local_template_render('gitignore.txt', env, '.gitignore')

            #    # init git
            #local('git init')
            local('git add .')
            local('git commit -am "init"')

            ## init virtual env
            ##local('virtualenv --clear venv')
            #virt_comm('pip install --download-cache=../deploy/.pip.cache -r ./src/requirements.txt'.replace('/', os.path.sep))

            # init Django
            #virt_comm('python ./manage.py syncdb --noinput --migrate'.replace('/', os.path.sep))
            virt_comm('python ./manage.py syncdb && python ./manage.py migrate --noinput'.replace('/', os.path.sep))

        if BITBUCKET_USER and BITBUCKET_PASSWORD and confirm_global('create private bitbucket repository?'):
            env.bit_user = BITBUCKET_USER
            env.bit_password = BITBUCKET_PASSWORD

            import requests as r

            rez = r.post('https://api.bitbucket.org/1.0/repositories/', data=dict(name=env.project, is_private=True),
                         auth=BITBUCKET_AUTH, )
            puts('request status ok: {0}'.format(rez.ok))

            if rez.ok:
                with lcd(env.project):
                    #local_template_render('fabfile.txt', env, 'fabs.py')
                    #with lcd('src'):
                    local('git remote add origin https://{0}:{2}@bitbucket.org/{0}/{1}.git'.format(env.bit_user,
                                                                                                   env.project,
                                                                                                   env.bit_password))
                    local('git push -u origin --all')   # to push changes for the first time


if __name__ == '__main__':
    # hack for pycharm run configuration.
    import subprocess
    import sys

    subprocess.call(['fab', '-f', __file__] + sys.argv[1:])
    #FabricShell().run()
