from log import log
import time
import glob
import os
import globalstatic
import zipfile
import subprocess

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

def process():

    do_robocopy()

def sync_scheduler():

    process()

sync_scheduler()