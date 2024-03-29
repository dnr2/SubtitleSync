#################################################
# srt.py
#
# A Python script to manipulate .srt subtitles
#
# Version:          0.1
# Author:           Riobard - me@riobard.com
# Modifications:    Danilo - dnr2@cin.ufpe.br
#################################################

import re
from sys import argv
from itertools import count

#################################################
# srt_parser class with Timecode object and friends
#################################################

class srt_parser():

    def tc2ms(self, tc):
        ''' convert timecode to millisecond '''

        sign    = 1
        if tc[0] in "+-":
            sign    = -1 if tc[0] == "-" else 1
            tc  = tc[1:]

        TIMECODE_RE     = re.compile('(?:(?:(?:(\d?\d):)?(\d?\d):)?(\d?\d))?(?:[,.](\d?\d?\d))?')
        # NOTE the above regex matches all following cases
        # 12:34:56,789
        # 01:02:03,004
        # 1:2:3,4   => 01:02:03,004
        # ,4        => 00:00:00,004
        # 3         => 00:00:03,000
        # 3,4       => 00:00:03,004
        # 1:2       => 00:01:02,000
        # 1:2,3     => 00:01:03,003
        # 1:2:3     => 01:02:03
        # also accept "." instead of "," as millsecond separator
        match   = TIMECODE_RE.match(tc)
        try: 
            assert match is not None
        except AssertionError:
            print tc
        hh,mm,ss,ms = map(lambda x: 0 if x==None else int(x), match.groups())
        return ((hh*3600 + mm*60 + ss) * 1000 + ms) * sign

    def ms2tc(self, ms):
        ''' convert millisecond to timecode ''' 
        sign    = '-' if ms < 0 else ''
        ms      = abs(ms)
        ss, ms  = divmod(ms, 1000)
        hh, ss  = divmod(ss, 3600)
        mm, ss  = divmod(ss, 60)
        TIMECODE_FORMAT = '%s%02d:%02d:%02d,%03d'
        return TIMECODE_FORMAT % (sign, hh, mm, ss, ms)


    class Timecode(object):
        def __init__(self, t):
            '''
            Construct a Timecode object from string representation or milliseconds
            '''

            if type(t) == int:  # millisec.
                self.ms = t
            elif type(t) == str:    # string format
                self.ms = srt_parser().tc2ms(t)
            else:
                raise Exception("Type mismatch")

        def __str__(self):
            return srt_parser().ms2tc(self.ms)

        def __repr__(self):
            return 'Timecode("%s")' % self.__str__()

        def __cmp__(self, other):
            return self.ms - other.ms

        def __add__(self, other):
            return srt_parser().Timecode(self.ms + other.ms)

        def __sub__(self, other):
            return srt_parser().Timecode(self.ms - other.ms)

        def __neg__(self):
            return srt_parser().Timecode(- self.ms)

    TC = Timecode  # short alias for Timecode

    #################################################
    # .srt parsing and serialization
    #################################################

    def parse(self, file):
        def parse_block(block):
            lines   = block.split('\n')
            TIMECODE_SEP    = re.compile('[ \->]*')
            tc1, tc2= map(self.TC, TIMECODE_SEP.split(lines[1]))
            txt     = '\n'.join(lines[2:])
            return (tc1, tc2, txt)

        return map(parse_block, 
                   open(file).read().strip().replace('\r', '').split('\n\n'))
    
    def parse_ms(self, file):
        def parse_block(block):
            lines   = block.split('\n')
            TIMECODE_SEP    = re.compile('[ \->]*')
            tc1, tc2= map(self.TC, TIMECODE_SEP.split(lines[1]))
            txt     = '\n'.join(lines[2:])
            return (tc1.ms, tc2.ms, txt)

        return map(parse_block, 
                   open(file).read().strip().replace('\r', '').split('\n\n'))

    def format(self, ls):
        def format_block(no, block):
            tc1, tc2, txt   = block
            return '\n'.join(['%d' % no, '%s --> %s' % (tc1, tc2), txt])

        return '\n\n'.join(map(format_block, range(1, len(ls)+1), ls))
    
    def format_ms(self, ls):
        def format_block(no, block):
            ms1, ms2, txt   = block
            return '\n'.join(['%d' % no, '%s --> %s' % (self.TC(ms1), self.TC(ms2)), txt])

        return '\n\n'.join(map(format_block, range(1, len(ls)+1), ls))


    #################################################
    # parsed .srt manipulation
    #################################################
        
    def shift(self, stream, delta):
        '''
        all timecode +delta
        '''
        return [(tc1+delta, tc2+delta, txt) for (tc1,tc2,txt) in stream]
    
    def concatenate(self, head, tail, tail_shift):
        '''
        Concatnate two srts by shifting the second and append to the first
        '''
        return head + shift(tail, tail_shift)

    def split(self, stream, *ts):
        '''
        Split stream into multiple substreams with given lengths

        NOTE: this is NOT splitting AT the time points!!!
        '''
        
        def split_at(stream, t):
            '''
            Split a subtitle stream at a given time point t
            '''
            head    = [(tc1, tc2, txt) for (tc1, tc2, txt) in stream if tc1 <= t]
            tail    = [(tc1, tc2, txt) for (tc1, tc2, txt) in stream if tc1 > t]

            return head, shift(tail, -t)

        for t in ts:
            head, tail  = split_at(stream, t)
            yield head
            stream  = tail

        yield tail

    #################################################
    # Command system
    #################################################    
    def split_cmd(self, *args):
        '''
        Usage: split input_file.srt 00:12:33,999 00:25:12,500

        Split a subtitle stream into multiple substreams with given length
        A trailing substream is assumed if it is not empty
        '''
        if len(args) < 2:
            print 'Usage: split input_file.srt 00:12:33,999 00:25:12,500'
        else:
            infile  = args[0]
            tcs     = args[1:]
            segs= split(parse(infile), *map(TC, tcs))
            print 'Splitting at %s' % ', '.join(map(str, map(TC, tcs)))
            for (no, seg) in zip(count(), segs):
                open('%s.%03d'%(infile, no), 'wb').write(format(seg))

    def shift_cmd(self, *args):
        if len(args) != 2:
            print 'Usage: shift input_file.srt delta'
        else:
            infile  = args[0]
            delta   = args[1]
            print(self.format(self.shift(self.parse(infile), self.TC(delta))))


    def command_run(self, argv):
        cmds    = {'split': self.split_cmd, 
                   'shift': self.shift_cmd}
        if len(argv) > 1 and argv[1] in cmds:
            cmds[argv[1]](*argv[2:])
        else:
            print 'Usage: %s [ %s ]' % (argv[0], ' | '.join(cmds))

#################################################
# Main program
#################################################
            
if __name__ == '__main__':
    srt_parser().command_run(argv)
