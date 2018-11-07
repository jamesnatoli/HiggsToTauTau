#!/usr/bin/env python

############################################################
## Script to automate running an analyzer on all files in ##
## a directory.                                           ##
############################################################

from os import popen
from subprocess import call
from optparse import OptionParser
import time
from glob import glob

parser = OptionParser()
parser.add_option('--data', '-d', action='store_true',
                  default=False, dest='isData',
                  help='run on data or MC'
                  )
parser.add_option('--exe', '-e', action='store',
                  default='Analyze', dest='exe',
                  help='name of executable'
                  )
parser.add_option('--syst', action='store_true',
                  default=False, dest='syst',
                  help='run systematics as well'
                  )
parser.add_option('--path', '-p', action='store',
                  default='root_files/', dest='path',
                  help='path to input file directory'
                  )
parser.add_option('--prefix', '-P', action='store',
                  default=None, dest='prefix',
                  help='prefix to strip'
)
(options, args) = parser.parse_args()
prefix = options.prefix
suffix = '.root'

start = time.time()
if options.isData:
    fileList = [ifile for ifile in glob(options.path+'/*') if '.root' in ifile and 'data' in ifile.lower()]
else:
    fileList = [ifile for ifile in glob(options.path+'/*') if '.root' in ifile]

systs = ['', 'met_UESUp', 'met_UESDown', 'met_JESUp', 'met_JESDown', 'metphi_UESUp', 'metphi_UESDown', 'metphi_JESUp', 'metphi_JESDown', 'mjj_JESUp', 'mjj_JESDown']

for ifile in fileList:
    sample = ifile.split('/')[-1].split(suffix)[0]
    if prefix:
      sample = sample.replace(prefix, '')
    tosample = ifile.replace(sample+suffix,'')
    print sample

    if 'DYJets' in sample:
        names = ['ZTT', 'ZL', 'ZJ']
    elif 'TT' in sample:
        names = ['TTT', 'TTJ']
    elif 'WJets' in sample or 'EWKW' in sample or 'WPlus' in sample or 'WMinus' in sample:
        names = ['W']
    elif 'EWKZ' in sample:
        names = ['EWKZ']
    elif 'data' in sample.lower():
        names = ['data_obs']
    elif 'ggHtoTauTau' in sample:
        mass = sample.split('ggHtoTauTau')[-1]
        names = ['ggH'+mass]
    elif 'ggH' in sample:
        mass = sample.split('ggH')[-1]
        names = ['ggH'+mass]
    elif 'VBFHtoTauTau' in sample:
        mass = sample.split('VBFHtoTauTau')[-1]
        names = ['VBF'+mass]
    elif 'VBF' in sample:
        mass = sample.split('VBF')[-1]
        names = ['VBF'+mass]
    elif 'WPlusH' in sample or 'WMinusH' in sample:
        mass = sample.split('HTauTau')[-1]
        names = ['WH'+mass]
    elif 'ZHTauTau' in sample:
        mass = sample.split('ZHTauTau')[-1]
        names = ['ZH'+mass]
    elif 'ZH' in sample:
        mass = sample.split('ZH')[-1]
        names = ['ZH'+mass]
    elif 'ttH' in sample:
        mass = sample.split('ttH')[-1]
        names = ['ttH'+mass]
    elif 'embed' in sample:
        names = ['embed']
    else: 
        names = ['VV', 'VVJ', 'VVT']

    callstring = './%s -p %s -s %s ' % (options.exe, tosample, sample)

    if options.syst:
        for isyst in systs:
            for name in names:
                tocall = callstring + ' -n %s -u %s' % (name, isyst)
                call(tocall, shell=True)
    else:
        for name in names:
            tocall = callstring + ' -n %s' % name 
            call(tocall, shell=True)

    print tocall

end = time.time()
print 'Processing completed in', end-start, 'seconds.'
