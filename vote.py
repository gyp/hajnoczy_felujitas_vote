#!/usr/bin/python3

import csv
import sys

from pyvotecore.schulze_npr import SchulzeNPR

class CSVVotes(object):
    def __init__(self, votesfilename):
        super(CSVVotes, self).__init__()
        self.ballots = self._parse_csvfile(votesfilename)

    def _parse_csvfile(self, votesfilename):
        ballots = []

        votesfile = open(votesfilename)
        votesfilereader = csv.reader(votesfile, delimiter=',')

        # skip the header
        next(votesfilereader)

        for row in votesfilereader:
            ballots.append(self._parse_row(row))

        return ballots

    def _parse_row(self, row):
        ballot = []
        equal_group = []
        for vote_or_delimiter in row[2:]:
            if vote_or_delimiter == '>':
                ballot.append(equal_group)
                equal_group = []
            elif vote_or_delimiter == '=':
                continue
            else:
                equal_group.append(vote_or_delimiter)
        ballot.append(equal_group)
        return {
            "count": int(row[1]),
            "ballot": ballot
        }

    def get_as_grouping(self):
        return self.ballots


voted_order = SchulzeNPR(
                CSVVotes(sys.argv[1]).get_as_grouping(),
                ballot_notation = "grouping").as_dict()['order']

print(voted_order)
 