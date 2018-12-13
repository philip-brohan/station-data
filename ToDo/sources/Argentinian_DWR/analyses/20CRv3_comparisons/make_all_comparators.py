#!/usr/bin/env python

# Extract data from 20CRv3 for each station at a range of timepoints

# Generates a set of jobs to be run in parallel on SPICE

import os
import sys
import subprocess
import datetime

max_jobs_in_queue=500
# Where to put the output files
opdir="%s/slurm_output" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this timepoint
def is_done(year,month,day,hour,var):
    op_file_name=("%s/sef_comparators/Argentinian_DWR/" +
                  "%04d/%02d/%02d/%02d/DWR_Zarate_%s.pkl") % (
                            os.getenv('SCRATCH'),
                            year,month,day,hour,var)
    if os.path.isfile(op_file_name):
        return True
    return False


start_day=datetime.datetime(1902, 2, 1, 0)
end_day  =datetime.datetime(1902,12,31,21)

f=open("run.txt","w+")
current_day=start_day
while current_day<=end_day:
    for hour in (0,3,6,9,12,15,18,21):
        for var in ('prmsl','air.2m'):
            if not is_done(current_day.year,current_day.month,
                           current_day.day,hour,var):
                cmd=("./get_comparators.py --year=%d --month=%d" +
                    " --day=%d --hour=%d --var=%s\n") % (
                       current_day.year,current_day.month,
                       current_day.day,hour,var)
                f.write(cmd)
    current_day=current_day+datetime.timedelta(days=1)
f.close()

