#!/usr/bin/python3
# vim: tabstop=4 shiftwidth=4 expandtab

from __future__ import print_function
import sys, getopt, argparse, os, glob, re, subprocess, collections, shutil, time
from subprocess import PIPE
from datetime import datetime


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run cluster jobs.")
    parser.add_argument("pgm", nargs=1, type=str, help="Program path")
    parser.add_argument("instfile", nargs=1, type=str, help="Instance file, text file with list of instances")
    parser.add_argument("configfile", nargs=1, type=str, help="Configuration file")
    parser.add_argument("destpath", nargs=1, type=str, help="Destionation path")
    #parser.add_argument("configfile", nargs=1, type=str, help="Configuration file")
    parser.add_argument("--max_array_size", type=int, default=1000, help="Maximum size of array job")
    parser.add_argument("--timestamp", choices=["date","datetime"], default="date", type=str, help="format of timestamp, used for result directory and files")
    parser.add_argument("--dry", help="Just output, no execution of runs", action='store_true')
    parser.add_argument("--rsync", type=str, help="Synchronize results from scratch directory with given directory")
    parser.add_argument("--summary", type=str, help="Summary script")
    args = parser.parse_args()

    # get list of instances from instance file
    instances = []
    with open(args.instfile[0], "r") as f:
        instances = f.readlines()

    # get paras from config file
    configs = []
    with open(args.configfile[0], "r") as f:
        configs = f.readlines()

    # time stamp
    dtobj = datetime.now()
    timestamp = dtobj.strftime("%Y%m%d")
    if args.timestamp == "datetime":
        timestamp = dtobj.strftime("%Y%m%d_%H%M%S")

    # create result directory
    abs_result_path = os.path.abspath(args.destpath[0])
    abs_result_timestamp_path = os.path.join(abs_result_path, timestamp)
    
    if os.path.exists(abs_result_timestamp_path):
        print("{} already exists!".format(abs_result_timestamp_path))
        exit(1)

    if not args.dry:
        os.mkdir(abs_result_timestamp_path)

    # create data directory (all out files will be stored there)
    abs_result_data_path = os.path.join(abs_result_timestamp_path, "data")
    if not args.dry:
        os.mkdir(abs_result_data_path)

    # copy program into result directory
    pgm_name = os.path.split(args.pgm[0])[1]
    pgm_timestamp_name = os.path.join(abs_result_timestamp_path, timestamp + "_" + pgm_name)
    if not args.dry:
        shutil.copy(args.pgm[0], pgm_timestamp_name)

    # copy instance file into result directory
    inst_name = os.path.split(args.instfile[0])[1]
    inst_timestamp_name = os.path.join(abs_result_timestamp_path, timestamp + "_" + inst_name)
    if not args.dry:
        shutil.copy(args.instfile[0], inst_timestamp_name)

    # copy config file into result directory
    config_name = os.path.split(args.configfile[0])[1]
    config_timestamp_name = os.path.join(abs_result_timestamp_path, timestamp + "_" + config_name)
    if not args.dry:
        shutil.copy(args.configfile[0], config_timestamp_name)

    runs = 0
    cmds = []
    for file in instances:
        file = file.strip()
        #print(file)
        for config in configs:
            runs = runs + 1

            #prepare command 
            config_str, dest_folder = config.split(';')
            dest_folder = dest_folder.strip()
            paras_str = 'ifile {} {}'.format(file, config_str)

            out_filename = os.path.splitext(os.path.basename(file))[0]
            abs_dest_path = os.path.join(abs_result_data_path, dest_folder)

            if not args.dry and not os.path.exists(abs_dest_path):
                os.mkdir(abs_dest_path)

            cmds.append('{} {} > {}/{}.out'.format(pgm_timestamp_name, paras_str, abs_dest_path, out_filename))

    cmd_name = os.path.join(abs_result_timestamp_path, "cmd.txt")
    if args.dry:
        print(*cmds, sep='\n')
        exit(0)
    else:
        with open(cmd_name, "w") as f:
            for cmd in cmds:
              f.write("{}\n".format(cmd))

    task_ids = []
    for chunk_start in range(0, runs, args.max_array_size):
        chunk_size = min(args.max_array_size, runs - chunk_start)
        sbatch_paras = ['sbatch']
        sbatch_paras.append( '--array={}-{}'.format(1, chunk_size) )
        sbatch_paras.append( 'run_array_job.sh' )
        sbatch_paras.append( cmd_name )
        sbatch_paras.append( str(chunk_start) )

        print(sbatch_paras)
        #taskid_text = subprocess.run(sbatch_paras, capture_output=True, text=True).stdout
        task_id_text = subprocess.run(sbatch_paras, stdout=PIPE, stderr=PIPE).stdout
        print(task_id_text)
        task_id = re.search(r'\d+', str(task_id_text)).group()
        task_ids.append(task_id)
        print(task_id)

    if args.summary is not None:
        summary_paras = ['sbatch']
        summary_paras.append( '--dependency=afterok:{}'.format(';'.join(task_ids)) )
        summary_paras.append( 'run_summary_job.sh' )
        summary_paras.append( args.summary )
        summary_paras.append( os.path.join(abs_result_data_path, '*') )
        summary_paras.append( os.path.join(abs_result_path, timestamp + '.sum') )
        summary_paras.append( os.path.join(abs_result_path, timestamp + '.err') )
        subprocess.run(summary_paras)

    # does not work yet...
    #if args.rsync is not None:
    #    rsync_paras = ['sbatch']
    #    rsync_paras.append( '--dependency=afterok:{}'.format(';'.join(task_ids)) )
    #    rsync_paras.append( '--partition=trans' )
    #    rsync_paras.append( '--time=00:10:00' )
    #    rsync_paras.append( '--ntasks=1' )
    #    rsync_paras.append( '--cpus-per-task=1' )
    #    rsync_paras.append( '--job-name="rsync"' )
    #    rsync_paras.append( '--wrap="rsync {} {}'.format(abs_result_timestamp_path, os.path.abspath(args.rsync)) )
    #    subprocess.run(rsync_paras)



