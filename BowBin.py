#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, subprocess, os
from pathlib import Path


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    print( "  ____                ____  _       ")
    print( " |  _ \              |  _ \(_)      ")
    print( " | |_) | _____      _| |_) |_ _ __  ")
    print( " |  _ < / _ \ \ /\ / /  _ <| | '_ \ ")
    print( " | |_) | (_) \ V  V /| |_) | | | | |")
    print( " |____/ \___/ \_/\_/ |____/|_|_| |_|\n\n")
print_header()

def debug(msg:str):
  if 'DEBUG_FLAG' in globals():
    print(bcolors.WARNING+"DEBUG: "+msg+bcolors.ENDC)

def check_return(result: subprocess.CompletedProcess, error_msg:str):
  print(result)
  if (result.returncode != 0 or len(result.stderr)>0):
      print(error_msg)
      exit(-1)

#trim_galore uses stderr for print in shell
def check_return_trim_galore(result: subprocess.CompletedProcess, error_msg:str):
  print(result)
  if (result.returncode != 0):
      print(error_msg)
      exit(-1)

def check_file_exist(file_path:str):
  if not Path(file_path).is_file():
      print("The file "+ file_path +" does not exist")
      exit(-1)

def msg_usage(name=None):                                                            
  return '''BowBin.py [options]* (-in_reads FASTQ | -dein_reads FASTQ1 FASTQ2 | -sraid SRAID)'''

def trim_galore(file1:str, file2:str):
  debug("file1: "+file1)
  debug("file2: "+file2)
  adapter_quality_trim_command = "trim_galore --paired "+file1+" "+file2+" -o "+OUTPUT_FOLDER
 
  debug(adapter_quality_trim_command)
  check_return_trim_galore(subprocess.run(adapter_quality_trim_command, capture_output=True, shell=True),"adapter removal or quality trimming error")


def trim_galore_polya(file1:str, file2:str):
    debug("file1: "+file1)
    debug("file2: "+file2)
    #controllare virusseeker e genome detective dove fanno la polyA
    #provare senza polyA
    #polya e' sperimentale, il flag -o non funziona, quindi dopo polya faccio mv dei file
    polyA_command = "trim_galore --polyA --paired "+file1.replace(".fq","_val_1.fq")+" "+file2.replace(".fq","_val_2.fq")
    debug(polyA_command)
    check_return_trim_galore(subprocess.run(polyA_command, capture_output=True, shell=True),"polyA error")

    debug(file1.replace(".fq","_val_1_val_1.fq"))
    
    move_files = "mv ./"+file1.replace(".fq","_val_1_val_1.fq").replace(OUTPUT_FOLDER,"")+" ./"+file2.replace(".fq","_val_2_val_2.fq").replace(OUTPUT_FOLDER,"")+" "+OUTPUT_FOLDER
    debug(move_files)
    check_return(subprocess.run(move_files, capture_output=True, shell=True),"mv error")

def fastq_join(file1:str, file2:str):
  debug("file1: "+file1)
  debug("file2: "+file2)

  fastq_join_command = "fastq-join "+file1.replace(".fq","_val_1_val_1.fq")+" "+file2.replace(".fq","_val_2_val_2.fq")+" -o "+OUTPUT_FOLDER+"result-fq"
  debug(fastq_join_command)
  check_return(subprocess.run(fastq_join_command, capture_output=True, shell=True), "fastq-join error")


def cd_hit():#problema: ci mette un eternità di tempo
  cd_hit_command = "cd-hit -i "+OUTPUT_FOLDER+"result-fqjoin -o "+OUTPUT_FOLDER
  debug("cd_hit_command:"+cd_hit_command)
  check_return(subprocess.run(cd_hit_command, capture_output=True, shell=True), "cd-hit error")


# Gather our code in a main() function
def main(args):

  print (args)
  if args.dein_reads is not None:
    check_file_exist(args.dein_reads[0])
    check_file_exist(args.dein_reads[1])

    #adapter removale, quality trimming, polyA
    debug("start trim galore"+args.dein_reads[0]+"  "+args.dein_reads[1])
    trim_galore(args.dein_reads[0],args.dein_reads[1])


    #polyA
    trim_galore_polya(args.dein_reads[0],args.dein_reads[1])
    
    #join overlapping reads
    fastq_join(args.dein_reads[0],args.dein_reads[1])

    #cd-hit clustering reads
    cd_hit()

  elif args.in_reads is not None:
    check_file_exist(args.in_reads)
    #fare check estensione (?)
    #fare check file output gia esistenti (?)

    #create output files
    create_reads_1_2 = "echo -n > "+OUTPUT_FOLDER+"reads-1.fq; echo -n > "+OUTPUT_FOLDER+"reads-2.fq"
    debug(create_reads_1_2)
    check_return(subprocess.run(create_reads_1_2, capture_output=True, shell=True), "error creation output file")

    #deinterleave reads
    deint_command = "paste - - - - - - - - < "+args.in_reads+" | tee >(cut -f 1-4 | tr \"\t\" \"\n\" > "+OUTPUT_FOLDER+"reads-1.fq) | cut -f 5-8 | tr \"\t\" \"\n\" > "+OUTPUT_FOLDER+"reads-2.fq"
    debug(deint_command)
    check_return(subprocess.run(deint_command, capture_output=True, shell=True, executable="/bin/bash"), "error deinterleave reads")

    #adapter removale, quality trimming, polyA
    debug("start trim_galore "+OUTPUT_FOLDER+"reads-1.fq  "+OUTPUT_FOLDER+"reads-2.fq")
    trim_galore(OUTPUT_FOLDER+"reads-1.fq",OUTPUT_FOLDER+"reads-2.fq")
  

    #polya
    trim_galore_polya(OUTPUT_FOLDER+"reads-1.fq",OUTPUT_FOLDER+"reads-2.fq")

    #join overlapping reads
    fastq_join(OUTPUT_FOLDER+"reads-1.fq",OUTPUT_FOLDER+"reads-2.fq")

    #cd-hit clustering reads
    cd_hit()

  else:
    print(3)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline") # usage=msg_usage()
  # TODO Specify your real parameters here.
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-in_reads', metavar="FASTQ", help="FASTQ = file .fastq containing interleaved paired-end reads")
  group.add_argument('-dein_reads', nargs=2,metavar=("FASTQ1","FASTQ2"), help="FASTQ1 and FASTQ2 = files .fastq containing deinterleaved paired-end reads")
  group.add_argument('-sraid', metavar="SRAID", help="SRA accession NCBI database")


  verbose_group = parser.add_mutually_exclusive_group(required=False)
  verbose_group.add_argument('--verbose', help="Verbose mode", action='store_true')
  verbose_group.add_argument('--very-verbose', help="Very verbose mode", action='store_true')

  parser.add_argument('--version', action='version', version='%(prog)s 1.0')
  parser.add_argument('-o', help="Output folder")
  parser.add_argument('-debug',help="debug mode", action='store_true')
  args = parser.parse_args()
    
  #output folder  
  if args.o is not None:
    if os.path.exists(args.o):
      print("The folder "+args.o+" already exist")
      exit(-1)
    else:  
      os.makedirs(args.o)
      if args.o[-1] != "/":
        OUTPUT_FOLDER = args.o+"/"
      else:
        OUTPUT_FOLDER = args.o
  else:
    OUTPUT_FOLDER = "./"

  #debug
  if args.debug is True:
    DEBUG_FLAG = True

  main(args)