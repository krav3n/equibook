# coding=utf-8
"""
this fabfile automates certain tasks that are used often during development.
"""
import os
import sys
from os.path import abspath, dirname

import django
from fabric.api import local
from fabric.decorators import task

# TODO: BLOCK execution when running anywhere but in docker env

sys.path.append(dirname(abspath(__file__)))

# Set default settings before Django gets involved
settings_module = os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

django.setup()


def local_with_settings(cmd, capture=False):
    cmd = 'DJANGO_SETTINGS_MODULE={0} {1}'.format(settings_module, cmd)
    return local(cmd, capture=capture)


def manage(cmd):
    return local('python manage.py {0} --settings={1}'.format(cmd, settings_module), capture=False)


@task(alias='mdd')
def make_dummy_data():
    """
    Install dummydata
    """
    from horsebook.dummydata.dummydata import (
        create_trainer_dicipline_levels,
        mkbookings,
        mkusers,
    )

    create_trainer_dicipline_levels()
    mkusers()
    mkbookings()


@task(alias='mbdd')
def make_big_dummy_data():
    """
    Install alot of dummy stores, units and users
    """
    from horsebook.dummydata.dummydata import (
        create_trainer_dicipline_levels,
        mkbookings,
        mkusers,
    )

    create_trainer_dicipline_levels()
    mkusers(num=500)
    mkbookings(num=500, num_bookings=500)


@task(alias='rdb')
def resetdb():
    """
    configure MySQL databases, users and grants.

    - reset, or create, the development database.

    This command supports removing all tables in databases on other machines.
    In a docker setup with mysql on another machine all tables must be dropped instead
    of just dumping the database because giving grants to the admin account can only be done by root
    """
    for database in ["eqdev"]:
        local(r"""
            mysql -h hb-mysql.docker -u eq -BNe "show tables in %s" |
            tr '\n' ',' |
            sed -e 's/,$//' |
            awk '{print "SET FOREIGN_KEY_CHECKS = 0;DROP TABLE IF EXISTS " $1 ";SET FOREIGN_KEY_CHECKS = 1;"}' |
            mysql -h hb-mysql.docker -u eq %s""" % (database, database))


@task(alias='rel')
def clear_elasticsearch_index():
    """
    Clear elasticsearch index
    """
    manage('clear_index --noinput')


@task(alias='cs')
def collectstatics():
    """
    runs django-compressor to generate files
    """
    manage('collectstatic --noinput')


@task(alias='sdb')
def syncdb():
    """
    create database schemas
    """
    manage('syncdb --noinput --database=default')


@task(alias='pcq')
def purge_celery_queues():
    """
    Purge celery queues (alias: rcl)
    """
    local_with_settings('celery purge -A celeryd --force')


@task()
def pyclean():
    """
    Purge all .pyc files from the source code
    """
    return local("pyclean .")


@task()
def rebuild_search_data():
    """
    Rebuild elasticsearch core
    """
    # manage("update_index")
    manage("rebuild_index --noinput")


@task(alias='qr')
def reset():
    """
    Quickly reset the application data (alias: qr)
        (such as database, product images, etc.).
    """
    pyclean()
    purge_celery_queues()
    clear_elasticsearch_index()
    resetdb()
    syncdb()
    make_dummy_data()
    collectstatics()
    rebuild_search_data()


@task(alias='hlt')
def high_load_test():
    """
    Reset all components and load huge ammount of data into database.
    """
    pyclean()
    purge_celery_queues()
    clear_elasticsearch_index()
    resetdb()
    syncdb()
    make_big_dummy_data()
    collectstatics()
    rebuild_search_data()
