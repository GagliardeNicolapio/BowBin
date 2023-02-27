#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, subprocess, os
from pathlib import Path




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
    print("DEBUG: "+msg)

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
  adapter_quality_trim_command = "trim_galore --paired "+file1+" "+file2+" -o "+OUTPUT_FOLDER
  polyA_command = "trim_galore --polyA --paired "+OUTPUT_FOLDER+file1+" "+OUTPUT_FOLDER+file2+" -o "+OUTPUT_FOLDER
  debug(adapter_quality_trim_command)
  debug(polyA_command)
  check_return_trim_galore(subprocess.run(adapter_quality_trim_command, capture_output=True, shell=True),"adapter removal or quality trimming error")
  check_return_trim_galore(subprocess.run(polyA_command, capture_output=True, shell=True),"polyA error")




# Gather our code in a main() function
def main(args):

  print (args)
  if args.dein_reads is not None:
    check_file_exist(args.dein_reads[0])
    check_file_exist(args.dein_reads[1])

    #adapter removale, quality trimming, polyA
    debug("start trim galore"+args.dein_reads[0]+"  "+args.dein_reads[1])
    trim_galore(args.dein_reads[0],args.dein_reads[1])

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