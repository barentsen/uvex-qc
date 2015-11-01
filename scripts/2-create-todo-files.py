#!/usr/bin/env python
"""Creates UVEX todo files.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)                                           
import re
import os
import numpy as np
from astropy.io import fits
from astropy.io import ascii
from astropy import log

def read_fieldlist(filename):
    return [field.strip() for field in open(filename).readlines()]


FIELDS_DONE = []  # Use this list to ignore fields observed recently
FIELDS_DONE = read_fieldlist('../data/observing/fields-observed-in-2015.txt')
RA_BINS = [18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7]


##########
# CLASSES
##########

class UVEXToDo(object):

    def __init__(self):
        # Create data structure to hold todo lists, grouped by RA bin
        self.todo = {}
        for ra in RA_BINS:
            self.todo[ra] = []
        # Another dictionary to keep track of the bin a field has been put in
        self.track_assignments = {}
        # Load the definitions of fields
        fieldinfo = open('fields.txt', 'r').readlines()
        self.definitions = dict(zip(
                                    [m.split(' ')[0].split('_')[1] 
                                    for m in fieldinfo], 
                                    fieldinfo
                            ))

    def add_fields(self, fieldlist):
        """Add a list of field names to the todo list."""
        for field in fieldlist:
            self.add_field(field)

    def add_field(self, fieldname):
        """Add a single fieldname to the todo list."""
        fielddef = self.definitions[fieldname]
        # Make sure we put fieldpairs in the same bin
        if fieldname[0:4] in self.track_assignments:
            ra = self.track_assignments[fieldname[0:4]]
        else:
            ra = int(re.split("\W+", fielddef)[1])
            self.track_assignments[fieldname[0:4]] = ra
        # Avoid duplicates
        if (not (fieldname in FIELDS_DONE) and
                not (fielddef in self.todo[ra])):
            self.todo[ra].append(fielddef)

    def print_stats(self):
        n_total = len(np.concatenate([self.todo[ra] for ra in RA_BINS]))
        print('Total: {0} unique fields'.format(n_total))
        # Print number of fields per bin
        for ra in RA_BINS:
            print('{0:02d}h: {1}'.format(ra, len(self.todo[ra])))

    def write_todo_files(self, directory='output'):
        """Write the todo lists to disk."""
        for ra in RA_BINS:
            filename = os.path.join(directory,
                                    'fields.todo.{0:02d}h'.format(ra))
            with open(filename, 'w') as output:
                for myfield in self.todo[ra]:
                    output.write(myfield)

    def write_done_file(self, directory='output'):
        """Writes the fields.done file, listing all fields not to observe."""
        all_fields_todo = np.concatenate([self.todo[ra] for ra in RA_BINS])
        filename = os.path.join(directory, 'fields.done')
        with open(filename, 'w') as output:
            for fieldnumber in np.arange(1, 7635+0.1, 1, dtype=int):
                fieldnumber = '{0:04d}'.format(fieldnumber)
                for field in [fieldnumber, fieldnumber+'o']:
                    fielddef = self.definitions[field]
                    if fielddef not in all_fields_todo:
                        output.write(fielddef)

    def test_output(self, directory='output'):
        """Raises an exception if the output looks invalid."""
        # Count total number of fields todo
        n_todo = 0
        for ra in RA_BINS:
            filename = os.path.join(directory, 'fields.todo.{0:02d}h'.format(ra))
            n_todo += len(open(filename, 'r').readlines())
        # Count total number of fields done
        filename_done = os.path.join(directory, 'fields.done'.format(ra))
        n_done = len(open(filename_done, 'r').readlines())
        # Their sum should be the total number of fields
        assert((n_done+n_todo) == 15270)


########
# MAIN
########
if __name__ == "__main__":
    from matplotlib import pyplot as plt
    plt.figure()#figsize=(6, 5))

    todo = UVEXToDo()
    todo.add_fields(read_fieldlist('uvex-fields-never-attempted.txt'))
    for i, ra in enumerate(RA_BINS):
        n_fields = len(todo.todo[ra])
        bar1 = plt.bar(i-0.5, n_fields, width=0.9, facecolor='#e74c3c', edgecolor='none', zorder=20)

    todo.add_fields(read_fieldlist('uvex-fields-failed.txt'))
    for i, ra in enumerate(RA_BINS):
        n_fields = len(todo.todo[ra])
        bar2 = plt.bar(i-0.5, n_fields, width=0.9, facecolor='#3498db', edgecolor='none', zorder=10)

    todo.print_stats()
    todo.write_todo_files()
    todo.write_done_file()
    todo.test_output()

    plt.title('UVEX fields to be observed')
    plt.legend((bar1, bar2), ('First attempt', 'Repeat observation'), loc='upper left')#, fontsize=10)
    plt.xlabel('R.A. [h]')
    plt.ylabel('Fields')
    plt.xticks(range(len(RA_BINS)), RA_BINS)
    plt.xlim([-1, 14])
    plt.ylim([0,1200])
    plt.tight_layout()
    plt.savefig('uvex-todo.png', dpi=80)
