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


def check_return(result: subprocess.CompletedProcess, error_msg:str):
  #print(result)
  if (result.returncode < 0 or len(result.stderr)>0):
      print(error_msg)
      exit(-1)

def check_file_exist(file_path):
  if not Path(file_path).is_file():
      print("The file "+ file_path +" does not exist")
      exit(-1)

def msg_usage(name=None):                                                            
    return '''BowBin.py [options]* (-in_reads FASTQ | -dein_reads FASTQ1 FASTQ2 | -sraid SRAID)'''

# Gather our code in a main() function
def main(args):

  print (args)
  if args.dein_reads is not None:
    print(1)

  elif args.in_reads is not None:
    check_file_exist(args.in_reads)
    #fare check estensione (?)
    #fare check file output gia esistenti (?)

    #create output files
    create_reads_1_2 = "echo -n > "+OUTPUT_FOLDER+"reads-1.fq; echo -n > "+OUTPUT_FOLDER+"reads-2.fq"
    create_result = subprocess.run(create_reads_1_2, capture_output=True, shell=True)
    check_return(create_result, "error creation output file")

    #deinterleave reads
    deint_command = "paste - - - - - - - - < "+args.in_reads+" | tee >(cut -f 1-4 | tr \"\t\" \"\n\" > "+OUTPUT_FOLDER+"reads-1.fq) | cut -f 5-8 | tr \"\t\" \"\n\" > "+OUTPUT_FOLDER+"reads-2.fq"
    deint_result = subprocess.run(deint_command, capture_output=True, shell=True, executable="/bin/bash")
    check_return(deint_result, "error deinterleave reads")

  

  else:
    print(3)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline", usage=msg_usage())
  # TODO Specify your real parameters here.
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-in_reads', metavar="FASTQ", help="FASTQ = file .fastq containing interleaved paired-end reads")
  group.add_argument('-dein_reads', nargs=2,metavar=("FASTQ1","FASTQ2"), help="FASTQ1 and FASTQ2 = files .fastq containing deinterleaved paired-end reads")
  group.add_argument('-sraid', metavar="SRAID", help="SRA accession NCBI database")


  parser.add_argument('--verbose', help="Verbose mode. Defualt False", action='store_true')
  parser.add_argument('--version', action='version', version='%(prog)s 1.0')
  parser.add_argument('-o', help="Output folder")
  args = parser.parse_args()
    
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

  main(args)