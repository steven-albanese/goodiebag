#!/bin/bash
#  Batch script for querying PDBs and fixing on cluster 
#
#
# walltime : maximum wall clock time (hh:mm:ss)
#PBS -l walltime=24:00:00
#
# join stdout and stderr
#PBS -j oe
#
# spool output immediately
#PBS -k oe
#
# specify queue
#PBS -q batch
#
# nodes: number of 8-core nodes
#   ppn: how many cores per node to use (1 through 8)
#       (you are always charged for the entire node)
#PBS -l nodes=1:ppn=1
#
#PBS -l mem=4GB
# export all my environment variables to the job
##PBS -V
#
# job name (default = name of scrfile)
#PBS -N query_pdb
#
#specifcy email for notifications 
#PBS -M steven.albanese@choderalab.org


cd $PBS_O_WORKDIR

python query_pdb.py -l Imatinib --mode LigAll --fix --apo --cwater

