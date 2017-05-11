FTIR File Renamer
==============
### Introduction

Renames files from the FTIR based on strict naming scheme

### Installation

From the command line in the folder in which you would like to install the program:

`git clone https://github.com/adamkoziol/ftir_renamer.git --recursive`

`cd ftir_renamer`

`python setup.py install`

Note: this final command may need to be run with sudo 

Ideally add renamer.py to your path. If you don't know how, that's fine. Just run the merger.py script from within 
the ftir_renamer folder

### Requirements
- Unix-like environment
- Spreadsheet of FTIR-related metadata
- The .FTIR output files corresponding to the FTIR IDs in the spreadsheet

### Arguments

path
The path of the folder containing the the spreadsheet of FTIR metadata
-s
The path of the folder containing the FTIR output files
-f 
The name spreadsheet containing the FTIR metadata
-o
The absolute path of the folder to store the renamed files

### Running 

##### Example command to run the script

`renamer.py /nas0/bio_requests/8782 -f FTIR.xlsx -s /nas0/bio_requests/8782/files`
    
    - renamer.py is in $PATH
    - path argument: /nas0/bio_requests/8782
    - spreadsheet of FTIR metadata: FTIR.xlsx
    - output folder in which renamed files are stored: /nas0/bio_requests/8782/files
    
##### Usage

```
usage: renamer.py [-h] -s SEQUENCEPATH -f FILENAME [-o OUTPUTPATH] path

Rename files for FTIR experiments using strict naming scheme

positional arguments:
  path                  Specify input directory

optional arguments:
  -h, --help            show this help message and exit
  -s SEQUENCEPATH, --sequencepath SEQUENCEPATH
                        Path of .fastq(.gz) files to process.
  -f FILENAME, --filename FILENAME
                        Name of .xls(x) file with renaming information. Must
                        conform to agreed upon format (see README for
                        additional information). This file must be in the
                        path.
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Optionally specify the folder in which the renamed
                        files are to be stored. Provide thefull path e.g.
                        /path/to/output/files
```
