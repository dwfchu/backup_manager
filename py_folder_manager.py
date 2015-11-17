from log import log
import time

import glob
import os
import shutil
import globalstatic
import subprocess
import logging

def path_create_handler(dir,create=True):

    #create dir if it doesn't exist
    if (not os.path.exists(dir)) and (create==True) :
        os.makedirs(dir)
        return True
    else:
        return False


def check_paths():

    #check for required paths
    path_create_handler(globalstatic.src_path)
    path_create_handler(globalstatic.main_path)
    path_create_handler(globalstatic.archive_path)

def do_robocopy():

    log_file = globalstatic.main_path + '\\backup.log'
    log.info('Calling robocopy')
    subprocess.call(['robocopy',globalstatic.src_path,globalstatic.main_path, '/mir','/e','/np','/LOG+:' + log_file])
    log.info('Robocopy complete')

def archive_maint():

    log.info('get all folders & sort by create datetime')
    archive_list = filter(os.path.isdir, glob.glob(globalstatic.archive_path + "\*"))
    archive_list.sort(key=lambda x: os.path.getctime(x),reverse=True)

    log.info('Starting cleanup')
    #delete files
    for dir in archive_list[globalstatic.archives_to_keep -1 :]:

        shutil.rmtree(dir)
    log.info(str(len(archive_list)) + ' archive snapshots removed')

def move_to_archive():
    try:
        log.info('Starting snapshot archiving')
        base_path = os.path.basename(os.path.normpath(globalstatic.main_path))

        gen_path =  globalstatic.archive_path + base_path
        gen_path += '_' + time.strftime('%Y%m%d%H%M') + '\\'

        log.info('Check existing snapshot, and overwrite')
        #remove if exists
        if os.path.exists(gen_path):
            shutil.rmtree(gen_path)

        log.info('Start copy')
        shutil.copytree(globalstatic.main_path, gen_path)


    except shutil.Error as e:
        print('Error: %s' % e)
        log.info('Application error: ' + str(e))
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)
        log.info('System error: ' + str(e.strerror))

def process():

    #check source path
    if not path_create_handler(globalstatic.src_path,False):
        log.info('Source path is invalid')

        #setup/check for destination paths
        path_create_handler(globalstatic.main_path)
        path_create_handler(globalstatic.archive_path)

        #copy incremental
        log.info('Start backup update sync main process')
        do_robocopy()

        #remove older archives
        log.info('Start archive cleanup main process')
        archive_maint()

        #copy current to archive
        log.info('Start snapshot main process')
        move_to_archive()

def sync_scheduler():

    #need to find out how!
    process()



sync_scheduler()