#!/usr/bin/env python
import os, re
import commands
import math, time
import sys

print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
NumberOfJobs= 100 # number of jobs to be submitted
#NumberOfJobs= 1 # number of jobs to be submitted
interval = 1 # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
OutputFileNames = "ntuple_jet" # base of the output file name, they will be saved in res directory
ScriptName = "scripts/runJets.py" # script to be used with cmsRun

#Single Gamma
#"SingleGammaPt25Eta1p6_2p8/crab_SingleGammaPt25_PU0-threshold/181031_145212/0000"
#"SingleGammaPt25Eta1p6_2p8/crab_SingleGammaPt25_PU0-stc/181031_145114/0000"
#VBF
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_threshold/181108_112741/0000"
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_stc/181108_104142/0000"
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_threshold-histoMax/181113_145731/0000"
#"VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_stc-histoMax/181113_145456/0000"

queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########

InputDirList = [ 
   "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_stc-histoMax/181113_145456/0000",
   "VBF_HToInvisible_M125_14TeV_powheg_pythia8/crab_stc-histoMax/181113_145456/0000"
   ]
OutputDirList = [
   "vbf_stc_histomax",
   "vbf_stc_histomax"
   ]

path = os.getcwd()

##### loop for creating and sending jobs #####
for indir, outdir in zip( InputDirList, OutputDirList ):

   print
   print 'do not worry about folder creation:'
   os.system("rm -r tmp/" + outdir)
   os.system("rm -r res/" + outdir)
   os.system("mkdir -p tmp/" + outdir)
   os.system("mkdir -p res/" + outdir)
   print

   for x in range(1, int(NumberOfJobs)+1):
      ##### creates directory and file list for job #######
      os.system("mkdir -p tmp/"+ outdir+"/"+str(x))
      os.chdir("tmp/"+ outdir+"/"+str(x))
      
      ##### creates jobs #######
      with open('job.sh', 'w') as fout:
         fout.write("#!/bin/sh\n")
         fout.write("echo\n")
         fout.write("echo\n")
         fout.write("echo 'START---------------'\n")
         fout.write("echo 'WORKDIR ' ${PWD}\n")
         fout.write("source /afs/cern.ch/work/s/sawebb/private/FastJet_HGC/HGCTPGPerformance/init_env_lxplus.sh\n")
         fout.write("export X509_USER_PROXY=/afs/cern.ch/user/s/sawebb/private/myVoms/x509up_u`id -u`\n")
         fout.write("cd "+str(path)+"\n")
         fout.write("python "+ScriptName+" --input='root://cms-xrd-global.cern.ch//store/user/sawebb/" + indir + "/ntuple_"+str(x)+".root' --output='res/"+outdir + "/" + OutputFileNames+"_"+str(x)+".root'\n")
         fout.write("echo 'STOP---------------'\n")
         fout.write("echo\n")
         fout.write("echo\n")
         os.system("chmod 755 job.sh")
         
         
   ##### creates submit file #######
      with open('condor.sub', 'w') as fout:
         fout.write("executable            = job.sh \n")
         fout.write("arguments             = $(ClusterID) $(ProcId) \n")
         fout.write("output                = $(ClusterId).out\n")
         fout.write("error                 = $(ClusterId).err\n")
         fout.write("log                   = $(ClusterId).log\n")
         fout.write("+JobFlavour           = \"workday\"\n") 
         fout.write("queue")
         
   ###### sends bjobs ######
   #   os.system("bsub -q "+queue+" -o logs job.sh")
      os.system("condor_submit condor.sub")
      print "job nr " + str(x) + " submitted"
   
      os.chdir("../../../")
   

   
print
print "your jobs:"
os.system("condor_q")
print
print 'END'
print
