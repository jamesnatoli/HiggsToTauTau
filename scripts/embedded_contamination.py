import pandas
import pprint
import uproot
from glob import glob
from subprocess import call


backgrounds = [
    'TTT', 'TTL', 'STT', 'STL',
    'VVT', 'VVL', 'ZL'
]


def parse_tree_name(keys):
    """Take list of keys in the file and search for our TTree"""
    if 'et_tree;1' in keys:
        return 'et_tree'
    elif 'mt_tree;1' in keys:
        return 'mt_tree'
    else:
        raise Exception('Can\'t find et_tree or mt_tree in keys: {}'.format(keys))


def main(args):
    files = [ifile for ifile in glob('{}/*.root'.format(args.input))]
    backgrounds = pandas.DataFrame()
    for ifile in files:
        open_file = uproot.open(ifile)
        tree_name = parse_tree_name(open_file.keys())
        events = open_file[tree_name].arrays(['*'], outputtype=pandas.DataFrame)
        signal_events = events[(events['is_signal'] > 0 & events['contamination'] == 1)]
        backgrounds = pandas.concat([backgrounds, signal_events], sort=False)

    shift_up = backgrounds.copy(deep=True)
    shift_dn = backgrounds.copy(deep=True)

    shift_up['evtwt'] *= 0.1
    shift_dn['evtwt'] *= -0.1

    open_file = uproot.open('{}/embed.root')
    tree_name = parse_tree_name(open_file.keys())
    oldtree = open_file[tree_name].arrays(['*'])
    treedict = {ikey: oldtree[ikey].dtype for ikey in oldtree.keys()}

    events = pandas.DataFrame(oldtree)
    signal_events = events[(events['is_signal'] > 0)]

    shift_up = pandas.concat([shift_up, signal_events])
    shift_dn = pandas.concat([shift_dn, signal_events])

    call('mkdir -p {}/../SYST_embed_contam_up'.format(args.input), shell=True)
    call('mkdir -p {}/../SYST_embed_contam_down'.format(args.input), shell=True)

    with uproot.recreate('{}/../SYST_embed_contam_up/embed.root'.format(args.input)) as f:
        f[tree_name] = uproot.newtree(treedict)
        f[tree_name].extend(shift_up.to_dict('list'))

    with uproot.recreate('{}/../SYST_embed_contam_down/embed.root'.format(args.input)) as f:
        f[tree_name] = uproot.newtree(treedict)
        f[tree_name].extend(shift_dn.to_dict('list'))


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='path to input files')
    main(parser.parse_args())