# -*- mode: python; coding: utf-8; -*-
import posixpath
import os
import re
import sys
import fabtools
from fabtools.files import is_dir
from fabtools.require import nginx, deb, python, files
from fabric.contrib.console import confirm as confirm_global
from fabric.api import *

__author__ = 'jbo'

# settings
from fabsettings import DEPLOY_USER, DEPLOY_PASSWORD, DEPLOY_HOSTS, DEPLOY_DEFAULT_DOMAIN, DEPLOY_DEFAULT_REPOSITORY, \
    BITBUCKET_PASSWORD, BITBUCKET_USER, VIRT_NAME, PROJECTS_ROOT, PROJECT_USER, VIRT_HOME
# end

env.user = DEPLOY_USER
env.project_user = PROJECT_USER
env.project_group = PROJECT_USER
env.password = DEPLOY_PASSWORD
env.hosts = DEPLOY_HOSTS
env.no_input_mode = False
env.virt = VIRT_NAME
env.project_dir_name = PROJECTS_ROOT

#env.v_format = '/usr/local/pythonbrew/venvs/Python-2.7.3/{0}'.format(env.virt)
env.virt_home = '.virtualenvs'
env.v_format = '{1}/{0}'.format(env.virt, VIRT_HOME)

project_virt = VIRT_NAME

env.domain_default = DEPLOY_DEFAULT_DOMAIN
env.repository_default = DEPLOY_DEFAULT_REPOSITORY

env.lcwd = os.path.abspath(os.path.dirname(__file__))
env.debug = True


def virt_comm(command):
    #local("/bin/bash -l -c 'source /usr/local/pythonbrew/venvs/Python-2.7.3/{0}/bin/activate && {1}'".format(env.virt, command))
    #local('source /usr/local/pythonbrew/venvs/Python-3.3.0/{0}/bin/activate && {1}'.format(env.virt, command))
    if sys.platform == 'darwin':
        local('source ~/.virtualenvs/{0}/bin/activate && {1}'.format(env.virt, command))
    else:
        local("/bin/bash -l -c '{0}/bin/activate && {1}'".format(env.v_format, command))


@task
def pip(r_file='prod'):
    virt_comm('pip install -r ./requirements/{0}.txt'.format(r_file))


@task
def c(c_param='local'):
    if c_param == 'local':
        if not is_dir('{0}/public/static'.format(env.lcwd)):
            #files.directory('{0}/public/static'.format(env.lcwd), mode='755')
            files.directory('public/static'.format(env.lcwd))
        virt_comm('python ./manage.py collectstatic -v 0 --clear --noinput'.replace('/', os.path.sep))
        virt_comm('python ./manage.py compress --force'.replace('/', os.path.sep))
        virt_comm('python ./manage.py syncdb --noinput --migrate'.replace('/', os.path.sep))
    else:
        with cd(env.project_dir_name):
            if not is_dir('{0}/public/static'.format(env.project_dir_name)):
                files.directory('{0}/public/static'.format(env.project_dir_name), use_sudo=True, owner=env.project_user,
                                group=env.project_group, mode='755')
                sudo(
                    'chown -R ' + env.project_user + ':' + env.project_group + ' db* log* public/static* public/media*')

            with fabtools.python.virtualenv(env.v_format):
                # django comands
                sudo('python ./manage.py collectstatic -v 0 --clear --noinput', user=env.project_user)
                sudo('python ./manage.py compress --force', user=env.project_user)
                sudo('python ./manage.py syncdb --noinput --migrate', user=env.project_user)
                #sudo('python src/manage.py loaddata fixtures.json', user=env.project_user)


@task
def t(t_param='prod'):
    env.debug = True
    with cd(env.project_dir_name):
        with fabtools.python.virtualenv('/usr/local/pythonbrew/venvs/Python-3.3.0/{0}'.format(t_param)):
            run('python -V')


@task
def libs(lookup_param='prod'):
    env.debug = True
    with cd(env.project_dir_name):
        with fabtools.python.virtualenv(env.v_format):
            #python.install_requirements('requirements/dev.txt', use_mirrors=False, use_sudo=True, user='jbo', download_cache=pip_cache_dir)
            python.install_requirements('requirements/{0}.txt'.format(lookup_param))


@task
def deploy(d_param='prod'):
    execute(libs, lookup_param=d_param)
    execute(compile, c_param=d_param)


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

    if not fabtools.user.exists('deploy'):
        fabtools.user.create('deploy', home=PROJECTS_ROOT, group='deploy', create_home=False, system=True,
                             shell='/bin/false', create_group=True)

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

            # proj dirs
            files.directory('log', use_sudo=True, owner='root', group='root', mode='755')
            files.directory('db', use_sudo=True, owner=env.project_user, group=env.project_group, mode='755')
            files.directory('media', use_sudo=True, owner=env.project_user, group=env.project_group, mode='755')
            files.directory('static', use_sudo=True, owner=env.project_user, group=env.project_group, mode='755')
            sudo('chown -R ' + env.project_user + ':' + env.project_group + ' db* static* media*')

            # django comands
            with fabtools.python.virtualenv('.virtualenvs'):
                sudo('python src/manage.py collectstatic --noinput', user=env.project_user)
                sudo('python src/manage.py syncdb --noinput', user=env.project_user)
                sudo('python src/manage.py migrate --noinput', user=env.project_user)
                #sudo('python src/manage.py loaddata fixtures.json', user=env.project_user)

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
