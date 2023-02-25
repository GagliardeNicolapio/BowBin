#!/usr/bin/env python
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging

def print_header():
    print( "  ____                ____  _       ")
    print( " |  _ \              |  _ \(_)      ")
    print( " | |_) | _____      _| |_) |_ _ __  ")
    print( " |  _ < / _ \ \ /\ / /  _ <| | '_ \ ")
    print( " | |_) | (_) \ V  V /| |_) | | | | |")
    print( " |____/ \___/ \_/\_/ |____/|_|_| |_|\n\n")
print_header()


# Gather our code in a main() function
def main(args):
  # TODO Replace this with your actual code.
  print (args)
  if args.dein_reads is not None:
    print(1)
  elif args.in_reads is not None:
    print(2)
  else:
    print(3)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Does a thing to some stuff.",
                                    epilog = "As an alternative to the commandline")
  # TODO Specify your real parameters here.
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-in_reads', metavar="FASTQ", help="FASTQ = file .fastq containing interleaved paired-end reads")
  group.add_argument('-dein_reads', nargs=2,metavar=("FASTQ1","FASTQ2"), help="FASTQ1 and FASTQ2 = files .fastq containing deinterleaved paired-end reads")
  group.add_argument('-sraid', metavar="SRAID", help="SRA accession NCBI database")

  args = parser.parse_args()
    
  main(args)