from log import log
import time
import glob
import os
import globalstatic
import zipfile

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

def archive_maint():

    log.info('get all folders & sort by create datetime')
    archive_list = filter(os.path.isfile, glob.glob(globalstatic.archive_path + "\*"))
    archive_list.sort(key=lambda x: os.path.getctime(x),reverse=True)

    log.info('Starting cleanup')
    #delete files
    for file in archive_list[globalstatic.archives_to_keep -1 :]:
        os.remove(file)
    log.info(str(len(archive_list)) + ' archive snapshots removed')

def process():

    #check source path

    archive_maint()
    compress_archive(globalstatic.main_path)

def compress_archive(dir_compress):

    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    #modes = {zipfile.ZIP_DEFLATED: 'deflated', zipfile.ZIP_STORED: 'stored',}

    base_path = os.path.basename(os.path.normpath(globalstatic.main_path))
    gen_path = globalstatic.archive_path + base_path
    gen_path += '_' + time.strftime('%Y%m%d%H%M')

    zf = zipfile.ZipFile(gen_path + '.zip', "w")
    for dirname, subdirs, files in os.walk(dir_compress + '\\'):
        zf.write(dirname,os.path.basename(dirname))
        for filename in files:
            zf.write(os.path.join(dirname, filename),os.path.basename(os.path.join(dirname, filename)),compress_type=compression)

def sync_scheduler():

    process()

sync_scheduler()