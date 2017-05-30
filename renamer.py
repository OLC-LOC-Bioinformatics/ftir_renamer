#!/usr/bin/env python
import time
import pandas
from accessoryfunctions.accessoryFunctions import *
__author__ = 'adamkoziol'


class Renamer(object):

    def excelparse(self):
        """
        Parses input excel file, and creates objects with headers as keys, and cell data as values for each row
        """
        # A dictionary to store the parsed excel file in a more readable format
        nesteddictionary = dict()
        # Use pandas to read in the excel file, and subsequently convert the pandas data frame to a dictionary
        # (.to_dict()). Only read the first fourteen columns (parse_cols=range(14)), as later columns are not
        # relevant to this script
        dictionary = pandas.read_excel(self.file, parse_cols=range(14)).to_dict()
        # Iterate through the dictionary - each header from the excel file
        for header in dictionary:
            # Sample is the primary key, and value is the value of the cell for that primary key + header combination
            for sample, value in dictionary[header].items():
                # Update the dictionary with the new data
                try:
                    nesteddictionary[sample].update({header: value})
                # Create the nested dictionary if it hasn't been created yet
                except KeyError:
                    nesteddictionary[sample] = dict()
                    nesteddictionary[sample].update({header: value})
        # Create objects for each of the samples, rather than using a nested dictionary. It may have been possible to
        # skip the creation of the nested dictionary, and create the objects from the original dictionary, but there
        # seemed to be too many possible places for something to go wrong
        for line in nesteddictionary:
            # Create an object for each sample
            metadata = MetadataObject()
            # Set the name of the metadata to be the primary key for the sample from the excel file
            metadata.name = line
            # Find the headers and values for every sample
            for header, value in nesteddictionary[line].items():
                # Try/except for value.encode() - some of the value are type int, so they cannot be encoded
                try:
                    # Create each attribute - use the header (in lowercase, and spaces removed) as the attribute name,
                    # and the value as the attribute value
                    setattr(metadata, header.replace(' ', '').encode().lower(), str(value).encode())
                except AttributeError:
                    setattr(metadata, header.replace(' ', '').encode().lower(), value)
            # Append the object to the list of objects
            self.metadata.append(metadata)
        # Run the filer method
        self.filer()

    def filer(self):
        """
        Match the files to the spreadsheet. Rename and copy the files as required.
        """
        from glob import glob
        import shutil
        # Create the output path as required
        make_path(self.outputpath)
        for sample in self.metadata:
            # Use the FTIR id and replicate from the spreadsheet as part of the pattern to match to find the
            # appropriate files e.g. FTIR0018 replicate 3 will match self.sequencepath/FTIR0018-3*
            try:
                sample.originalfile = glob(os.path.join(self.sequencepath,
                                                        ('{}-{}*'.format(sample.ftirid, sample.replicate))))[0]
                sample.datetime = os.path.basename(sample.originalfile).split('_')[1]
                # Rename the file using values from the spreadsheet
                # Original File Name: FTIR0182-1_2017-05-26T11-13-47.spc
                # New File Name: GN_Klebsiella_BHI_AN_CFIA_FTIR0182_C2_2017_May_26_CA01_OLC0027_2017-05-26T11-13-47.spc
                sample.renamedfile = '{}'.format('_'.join([sample.gramstain,
                                                           sample.genus,
                                                           sample.species,
                                                           sample.media,
                                                           sample.respiration,
                                                           sample.location,
                                                           sample.ftirid,
                                                           sample.machine,
                                                           sample.yyyy,
                                                           sample.mmm,
                                                           sample.dd,
                                                           '{}{:02d}'.format(sample.user, int(sample.replicate)),
                                                           sample.strainid,
                                                           sample.datetime
                                                           ]))
                # If the species is not provided, remove the 'nan' placeholder used e.g.
                # GP_Bacillus_nan_TSB_AE_CFIA_FTIR0010_C2_2017_April_20_01.spc becomes
                # GP_Bacillus_TSB_AE_CFIA_FTIR0010_C2_2017_April_20_01.spc
                if sample.species == 'nan':
                    sample.renamedfile = sample.renamedfile.replace('nan_', '')
                # The output file will be the the renamed file in the output path
                sample.outputfile = os.path.join(self.outputpath, sample.renamedfile)
                # Do not copy the file if it already exists
                if not os.path.isfile(sample.outputfile):
                    shutil.copyfile(sample.originalfile, sample.outputfile)
            # Print a message warning that certain files specified in the spreadsheet were not found in the file path
            except IndexError:
                printtime('Missing file for {}'.format(sample.ftirid), self.start, '\033[93m')

    def __init__(self, args):
        """
        :param args: object of arguments
        """
        # Define variables based on supplied arguments
        self.path = os.path.join(args.path, '')
        assert os.path.isdir(self.path), u'Supplied path is not a valid directory {0!r:s}'.format(self.path)
        self.sequencepath = os.path.join(args.sequencepath, '')
        assert os.path.isdir(self.sequencepath), u'Supplied sequence path is not a valid directory {0!r:s}'\
            .format(self.sequencepath)
        self.file = os.path.join(self.path, args.filename)
        self.start = args.start
        assert os.path.isfile(self.file), u'Cannot find the supplied Excel file ({0!r:s}) with the file information. ' \
                                          u'Please ensure that this file is in the path, and there\'s no spelling ' \
                                          u'mistakes'.format(self.file)
        # If the output path is not provided, use self.path/renamedfiles as the path
        try:
            self.outputpath = os.path.join(args.outputpath, '')

        except AttributeError:
            self.outputpath = os.path.join(self.path, 'renamedfiles', '')
        # Create class variable
        self.metadata = list()
        # Parse the excel sheet
        self.excelparse()

if __name__ == '__main__':
    # Argument parser for user-inputted values, and a nifty help menu
    from argparse import ArgumentParser
    # Parser for arguments
    parser = ArgumentParser(description='Rename files for FTIR experiments using strict naming scheme')
    parser.add_argument('path',
                        help='Specify input directory')
    parser.add_argument('-s', '--sequencepath',
                        required=True,
                        help='Path of .fastq(.gz) files to process.')
    parser.add_argument('-f', '--filename',
                        required=True,
                        help='Name of .xls(x) file with renaming information. Must conform to agreed upon format '
                             '(see README for additional information). This file must be in the path.')
    parser.add_argument('-o', '--outputpath',
                        help='Optionally specify the folder in which the renamed files are to be stored. Provide the'
                             'full path e.g. /path/to/output/files')
    # Get the arguments into an object
    arguments = parser.parse_args()
    # Define the start time
    arguments.start = time.time()

    # Run the script
    Renamer(arguments)

    # Print a bold, green exit statement
    print('\033[92m' + '\033[1m' + "\nElapsed Time: %0.2f seconds" % (time.time() - arguments.start) + '\033[0m')
