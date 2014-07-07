# coding=utf-8
from fabric.api import env, settings, task, require, local, run, sudo, cd
from .util import path


@task
def push():
    """Push changes to the remote location."""
    require('hg_config', 'remote_django_sync')

    # If nothing to push, ignore return code
    with settings(warn_only=True):
        local('hg push -f --config {} {}'.format(env.hg_config, env.remote_django_sync))


@task
def pull():
    """Pull all the changes from the production server."""
    require('hg_config', 'remote_django_sync')

    #local('hg pull {}'.format(path.account('django')))
    local('hg pull --config {} {}'.format(env.hg_config, env.remote_django_sync))


@task
def update(force=False):
    """Update remote repository."""
    require('hg_config', 'tag')

    with cd(path.account('django')):
        run('hg update {1} {0}'.format(env.tag, '--clean' if force else ''))


@task
def touch(*args):
    """Touch uWSGI config to reload worker."""
    for _, remote in env.service_handlers['u'].generate(*args):
        sudo('touch ' + remote)


@task
def commit():
    """Commit all the changes on the production server."""
    require('django_user')

    with cd(path.account('django')):
        run('hg add')
        run('hg commit -m "Hosting changes save" -u {}'.format(env.django_user))


@task
def save():
    """Save all the changes on the production server.

    This will remotedly commit the repository, and pull changes from the remote location.
    """
    commit()
    pull()


@task
def migrate_app(site, app):
    """Do the South migration for an application."""
    require('settings')

    with cd(path.django_site(site)):
        run('python manage.py migrate {} --settings="{}.{}"'.format(app, site, env.settings))


@task
def migrate(*sites):
    """Do the South migration for an application."""
    require('settings')

    for site in get_sites_for_task("deploy", *sites):
        with cd(path.django_site(site)):
            run('python manage.py migrate --settings="{}.{}"'.format(site, env.settings))


@task
def clearstatic(*sites):
    """Clear static files for the web server."""
    for site in get_sites_for_task("deploy", *sites):
        with cd(path.django_site(site)):
            run('rm -rf ' + path.django_site(site, 'wwwroot', 'static', '*'))


@task
def collectstatic(*sites):
    """Collect static files for the web server."""

    for site in get_sites_for_task("deploy", *sites):
        with cd(path.django_site(site)):
            run('python manage.py collectstatic --noinput -l')

        # Copy mtime from file to symlink isn't necessary in case of offline compression.
        #run('find wwwroot -type l -exec readlink {} \; -print | xargs -n 2 touch -mhr')


@task
def createdirs(*sites):
    """Create necessary directories if absent.
    Those directories are excluded from the repository, thus are not copied on push."""
    for site in get_sites_for_task("deploy", *sites):
        with cd(path.django_site(site)):
            for dir_name in ['index', 'tmp']:
                run('mkdir -p {}'.format(dir_name))


@task
def loaddata(filename, *sites):
    """Load data from fixture."""
    require('settings')

    for site in get_sites_for_task("deploy", *sites):
        with cd(path.django_site(site)):
            run('python manage.py loaddata {} --settings="{}.{}"'.format(filename, site, env.settings))


@task
def cleanthumb(*sites):
    """Cleanup thumbnail cache database."""
    require('settings')

    for site in get_sites_for_task("thumbnail", *sites):
        with cd(path.django_site(site)):
            run('python manage.py thumbnail cleanup --settings="{}.{}"'.format(site, env.settings))


@task
def clearthumb(*sites):
    """Completely clear thumbnail cache database."""
    require('settings')

    for site in get_sites_for_task("thumbnail", *sites):
        with cd(path.django_site(site)):
            run('python manage.py thumbnail clear --settings="{}.{}"'.format(site, env.settings))


@task
def compress(*sites):
    """Execute compress task."""
    require('settings')

    for site in get_sites_for_task("compress", *sites):
        with cd(path.django_site(site)):
            run('python manage.py compress --settings="{}.{}"'.format(site, env.settings))


@task
def updateindex(*sites):
    """Completely clear thumbnail cache database."""
    require('settings')

    for site in get_sites_for_task("index", *sites):
        with cd(path.django_site(site)):
            run('python manage.py update_index --settings="{}.{}"'.format(site, env.settings))


@task
def clearindex(*sites):
    """Completely clear thumbnail cache database."""
    require('settings')

    for site in get_sites_for_task("index", *sites):
        with cd(path.django_site(site)):
            run('python manage.py clear_index --settings="{}.{}"'.format(site, env.settings))


@task
def cleanup(*sites):
    """Full static data prepare."""
    require('site_tasks')

    collectstatic(*sites)
    createdirs(*sites)
    cleanthumb(*sites)
    compress(*sites)
    updateindex(*sites)


@task
def upload(force=False):
    """Upload and update the sites."""
    push()
    update(force=force)


@task
def deploy(*sites):
    """Deploy the sites."""
    upload()
    cleanup(*sites)


@task
def uptouch(*args):
    """Upload and touch uWSGI config to reload worker."""
    upload()
    touch(*args)


@task
def uptouch(*args):
    """Upload and touch uWSGI config to reload worker."""
    upload()
    migrate(*args)
    touch(*args)


def get_sites_for_task(task_name, *sites):
    task_sites = set(env.site_tasks[task_name])
    selected_sites = set(sites)
    for cur in task_sites.intersection(selected_sites) if len(selected_sites) > 0 else task_sites:
        yield cur
