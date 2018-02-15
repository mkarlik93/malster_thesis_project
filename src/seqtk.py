#!/usr/bin/env python

###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = 'Michal Karlicki'
__copyright__ = 'Copyright 2018'
__credits__ = ['Michal Karlicki']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Michal Karlicki'
__email__ = 'michal.karlicki@gmail.com'
__status__ = 'Development'




def parse_labels(path):
    reads = {}
    with open(path,"r") as f:
        for line in f:
            splited = line.split(" ")
            splited_1 = line.split(";")
            try:
                reads[splited[0].strip("\troot;cellular")] = splited_1[3].strip("\n")
            except IndexError:
                try:
                    reads[splited[0].strip("\troot;cellular")] = splited_1[2].strip("\n")
                except IndexError:
                    try:
                        reads[splited[0].strip("\troot;cellular")] = splited_1[1].strip("\n")
                    except IndexError:
                        pass
    return reads

def parse_unique(path):
    unique = set()

    with open(path,"r") as f:
        for line in f:
            splited = line.split(" ")
            splited_1 = line.split(";")
            try:
                unique.add(splited_1[3].strip("\n"))
            except IndexError:
                try:
                    unique.add(splited_1[2].strip("\n"))
                except IndexError:
                    try:
                        unique.add(splited_1[1].strip("\n"))
                    except IndexError:
                        pass
    return unique


def segregate(path):
    segregated = {}
    unique = parse_unique(path)
    reads = parse_labels(path)
    for i in unique:
        segregated[i] = []
    for key in reads:
        segregated[reads[key]].append(key)
    return segregated


def file_preparation(path):
    dictionary = segregate(path)
    to_save = dictionary.items()
    for i in to_save:
        with open(str(i[0]+".1"),"w") as f:
            for id in i[1]:
                f.write(id+"\n")
        print str(i[0])+" has been written! (R)"

        with open(str(i[0]+".2"),"w") as f:
            for id in i[1]:
                new_id = id[:-2]
                f.write(new_id+".2"+"\n")
        print str(i[0])+" has been written! (F)"


def seqtq_handler(reads_1,reads_2,path,ext):

    dictionary = segregate(path)
    to_save = dictionary.items()
    for i in to_save:
        command_1 = "seqtk subseq %s %s > %s" % (reads_1, i[0]+".1", "reads_"+i[0]+"_1."+ext)
        os.system(command_1)
        command_2 = "seqtk subseq %s %s > %s" % (reads_2, i[0]+".2", "reads_"+i[0]+"_2."+ext)
        os.system(command_2)

if __name__ == "__main__":

    import os
    from time import gmtime, strftime
    import sys
    import argparse

    description = """

Version 1.01

This script is designed for taxonomic-wise reads extraction.

If you have any questions, please do not hesitate to contact me
email address: michal.karlicki@gmail.com
"""

    epilog = """

"""


    parser = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=epilog)




    parser.add_argument('read_1', metavar='read_1', type=str)
    parser.add_argument('read_2', metavar='read_2', type=str)
    parser.add_argument('labels', metavar='labels', type=str)
    parser.add_argument('ext', metavar='ext', type=str)


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    file_preparation(args.labels)
    seqtq_handler(args.read_1,args.read_2,args.labels,args.ext)
    end = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "Starting time: "+start
    print "Ending time: "+end