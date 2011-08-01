#!/usr/bin/env python
# CPIP is a C/C++ Preprocessor implemented in Python.
# Copyright (C) 2008-2011 Paul Ross
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
# Paul Ross: cpipdev@googlemail.com

"""Base class for CPIP core test classes."""

__author__  = 'Paul Ross'
__date__    = '2011-07-10'
__version__ = '0.8.0'
__rights__  = 'Copyright (c) 2008-2011 Paul Ross'

#import logging
import difflib
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from cpip.core import PpToken
from cpip.core import PpTokeniser

######################
# Section: Unit tests.
######################
import unittest

class TestCpipBase(unittest.TestCase):
    """Base class for CPIP test classes."""

    def _printDiff(self, actual, expected):
        """Prints out the differences between two lists of PpTokens."""
        if actual != expected:
            print
            self.pprintReplacementList(actual)
            i = 0
            print 'Diff: actual -> expected'
            #m = map(None, actual, expected)
            for t, e in map(None, actual, expected):
                if t is not None and e is not None:
                    if t != e:
                        print '%d: %s, != %s' \
                                          % (i,
                                             self.__stringiseToken(t),
                                             self.__stringiseToken(e))
                else:
                    print '%d: %s, != %s' \
                                      % (i,
                                         self.__stringiseToken(t),
                                         self.__stringiseToken(e))
                i += 1

    def __stringiseToken(self, theTtt):
        return str(theTtt).replace('\n', '\\n')

    def pprintReplacementList(self, theList):
        """Pretty prints the replacement list."""
        #print
        i = 0
        for aTtt in theList:
            # PpTokeniser.NAME_ENUM['preprocessing-op-or-punc']),
            print '%2d: %s,' \
                % (i, self.__stringiseToken(aTtt))
            i += 1
        print 'As string:'
        print PpToken.tokensStr(theList)

    def stringToTokens(self, theString):
        """Returns a list of preprocessing tokens from a string. This can be
        used to test against expected values."""
        myCpp = PpTokeniser.PpTokeniser(
            theFileObj=StringIO.StringIO(theString)
            )
        return [t_tt for t_tt in myCpp.next()]

    def tokensToString(self, theTokens):
        """Returns a string from a list of preprocessing tokens. This can be
        used to test against expected values."""
        return ''.join([t_tt.t for t_tt in theTokens])

    def pprintTokensAsCtors(self, theList):
        """Pretty prints the list as PpToken constructors."""
        for aTtt in theList:
            # PpTokeniser.NAME_ENUM['preprocessing-op-or-punc']),
            print 'PpToken.PpToken(\'%s\', \'%s\'),' % (aTtt.t.replace('\n', '\\n'), aTtt.tt)

    def listStrDiff(self, a, b):
        retList = ['String diff using difflib:']
        s = difflib.SequenceMatcher(None, a, b)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            retList.append('%7s a[%d:%d] (%s) b[%d:%d] (%s)' \
                           % (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
        return retList
    
    def printStrDiff(self, a, b):
        """Prints the differences between two strings."""
        print ' Diff start '.center(75, '-')
        print '\n'.join(self.listStrDiff(a, b))
        print ' Diff end '.center(75, '-')
