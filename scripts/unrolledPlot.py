#!/usr/bin/env python
from argparse import ArgumentParser

parser = ArgumentParser(description='script to produce stacked plots')
parser.add_argument('--var', '-v', action='store',
                    dest='var', default='el_pt',
                    help='name of variable to plot'
                    )
parser.add_argument('--cat', '-c', action='store',
                    dest='cat', default='et_vbf',
                    help='name of category to pull from'
                    )
parser.add_argument('--channel', '-l', action='store',
                    dest='channel', default='et',
                    help='name of channel'   
                    )
parser.add_argument('--year', '-y', action='store',
                    dest='year', default='2016',
                    help='year to plot'   
                    )
parser.add_argument('--dir', '-d', action='store',
                    dest='in_dir', default='',
                    help='input directory'
                    )
parser.add_argument('--prefix', '-p', action='store',
                    dest='prefix', default='test',
                    help='prefix to add to plot name'
                    )
parser.add_argument('--scale', '-s', action='store', type=float,
                    dest='scale', default=1.,
                    help='scale top of hist by x'
                    )
args = parser.parse_args()

from ROOT import TFile, TLegend, TH1F, TCanvas, THStack, kBlack, TColor, TLatex, kTRUE, TMath, TLine, gStyle
from glob import glob
gStyle.SetOptStat(0)

from ROOT import gROOT, kTRUE
gROOT.SetBatch(kTRUE)

def applyStyle(name, hist, leg):
    overlay = 0
    print name, hist.Integral()
    if name == 'embedded':
        hist.SetFillColor(TColor.GetColor("#f9cd66"))
        hist.SetName("embedded")
    elif name == 'TTT':
        hist.SetFillColor(TColor.GetColor("#cfe87f"))
        hist.SetName('TTT')
    elif name == 'VVT' or name == 'EWKZ':
        hist.SetFillColor(TColor.GetColor("#9feff2"))
        overlay = 4
    elif name == 'ZL':
        hist.SetFillColor(TColor.GetColor("#de5a6a"))
        hist.SetName('ZL')
    elif name == 'QCD':
        hist.SetFillColor(TColor.GetColor("#ffccff"))
        hist.SetName('QCD')
    elif name == 'jetFakes':
        hist.SetFillColor(TColor.GetColor("#ffccff"))
        hist.SetName('jet fakes')
    elif name == 'data_obs':
        hist.SetLineColor(kBlack)
        hist.SetMarkerStyle(8)
        overlay = 1
    elif name == 'VBF125':
        hist.SetFillColor(0)
        hist.SetLineWidth(3)
        hist.SetLineColor(TColor.GetColor('#FF0000'))
        overlay = 2
    elif name == 'ggH125':
        hist.SetFillColor(0)
        hist.SetLineWidth(3)
        hist.SetLineColor(TColor.GetColor('#0000FF'))
        overlay = 3
    else:
        return None, -1, leg
    return hist, overlay, leg


def createCanvas():
    can = TCanvas('can', 'can', 432, 451)
    can.Divide(2, 1)

    pad1 = can.cd(1)
    pad1.SetLeftMargin(.12)
    pad1.cd()
    pad1.SetPad(0, .3, 1, 1)
    pad1.SetTopMargin(.1)
    pad1.SetBottomMargin(0.02)
    #pad1.SetLogy()
    pad1.SetTickx(1)
    pad1.SetTicky(1)

    pad2 = can.cd(2)
    pad2.SetLeftMargin(.12)
    pad2.SetPad(0, 0, 1, .3)
    pad2.SetTopMargin(0.06)
    pad2.SetBottomMargin(0.35)
    pad2.SetTickx(1)
    pad2.SetTicky(1)

    can.cd(1)

    return can


def formatStat(stat):
    stat.SetMarkerStyle(0)
    stat.SetLineWidth(2)
    stat.SetLineColor(0)
    stat.SetFillStyle(3004)
    stat.SetFillColor(kBlack)
    return stat


def formatStack(stack):
    stack.GetXaxis().SetLabelSize(0)
    stack.GetYaxis().SetTitle('Events / Bin')
    stack.GetYaxis().SetTitleFont(42)
    stack.GetYaxis().SetTitleSize(.05)
    stack.GetYaxis().SetTitleOffset(1.2)
    stack.SetTitle('')

def formatOther(other, holder):
    other.SetFillColor(TColor.GetColor("#9feff2"))
    other.SetName('Other')
    holder.append(other.Clone())
    return holder


def fillStackAndLegend(data, vbf, ggh, holder, leg):
    stack = THStack()
    leg.AddEntry(data, 'Data', 'lep')
    leg.AddEntry(vbf, 'VBF Higgs(125)x50', 'l')
    leg.AddEntry(ggh, 'ggH Higgs(125)x50', 'l')
    leg.AddEntry(filter(lambda x: x.GetName() == 'embedded', holder)[0], 'ZTT', 'f')
    leg.AddEntry(filter(lambda x: x.GetName() == 'ZL', holder)[0], 'ZL', 'f')
    leg.AddEntry(filter(lambda x: x.GetName() == 'jet fakes', holder)[0], 'jetFakes', 'f')
    leg.AddEntry(filter(lambda x: x.GetName() == 'TTT', holder)[0], 'TTT', 'f')
    leg.AddEntry(filter(lambda x: x.GetName() == 'Other', holder)[0], 'Others', 'f')

    holder = sorted(holder, key=lambda hist: hist.Integral())
    for hist in holder:
        stack.Add(hist)
    return stack, leg

def createLegend():
    leg = TLegend(0.5, 0.45, 0.85, 0.85)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextFont(61)
    leg.SetTextFont(42)
    leg.SetTextSize(0.045)
    return leg


def formatPull(pull):
    pull.SetTitle('')
    pull.SetMaximum(2)
    pull.SetMinimum(0)
    pull.GetXaxis().SetTitle('Unrolled')
    pull.SetMarkerStyle(21)
    pull.GetXaxis().SetTitleSize(0.18)
    pull.GetXaxis().SetTitleOffset(0.8)
    pull.GetXaxis().SetTitleFont(42)
    pull.GetXaxis().SetLabelFont(42)
    pull.GetXaxis().SetLabelSize(.111)
    pull.GetXaxis().SetNdivisions(505)
    # pull.GetXaxis().SetLabelSize(0)
    # pull.GetXaxis().SetTitleSize(0)

    pull.GetYaxis().SetTitle('Data / MC')
    pull.GetYaxis().SetTitleSize(0.12)
    pull.GetYaxis().SetTitleFont(42)
    pull.GetYaxis().SetTitleOffset(.475)
    pull.GetYaxis().SetLabelSize(.12)
    pull.GetYaxis().SetNdivisions(204)
    return pull

# def formatPull(pull):
#     pull.SetTitle('')
#     pull.SetMaximum(2.8)
#     pull.SetMinimum(-2.8)
#     pull.SetFillColor(TColor.GetColor('#bbbbbb'))
#     pull.SetLineColor(TColor.GetColor('#bbbbbb'))
#     pull.GetXaxis().SetTitle(titles[args.var])
#     pull.GetXaxis().SetTitleSize(0.18)
#     pull.GetXaxis().SetTitleOffset(0.8)
#     pull.GetXaxis().SetTitleFont(42)
#     pull.GetXaxis().SetLabelFont(42)
#     pull.GetXaxis().SetLabelSize(.111)
#     pull.GetXaxis().SetNdivisions(505)

#     pull.GetYaxis().SetTitle('#frac{Data - Bkg}{Uncertainty}')
#     pull.GetYaxis().SetTitleSize(0.16)
#     pull.GetYaxis().SetTitleFont(42)
#     pull.GetYaxis().SetTitleOffset(.251)
#     pull.GetYaxis().SetLabelSize(.12)
#     pull.GetYaxis().SetNdivisions(505)
#     return pull


def sigmaLines(data):
    low = data.GetBinLowEdge(1)
    high = data.GetBinLowEdge(data.GetNbinsX()) + \
        data.GetBinWidth(data.GetNbinsX())

    ## high line
    line1 = TLine(low, 1.5, high, 1.5)
    line1.SetLineWidth(1)
    line1.SetLineStyle(3)
    line1.SetLineColor(kBlack)

    ## low line
    line2 = TLine(low, 0.5, high, 0.5)
    line2.SetLineWidth(1)
    line2.SetLineStyle(3)
    line2.SetLineColor(kBlack)

    return line1, line2


def blindData(data, signal, background):
#    for ibin in range(data.GetNbinsX()+1):
#        sig = signal.GetBinContent(ibin)
#        bkg = background.GetBinContent(ibin)
#        if bkg > 0 and sig / TMath.Sqrt(bkg + pow(0.09*bkg, 2)) > 0.5:
#            data.SetBinContent(ibin, 0)
#
#    if args.var == 'NN_disc':
#        middleBin = data.FindBin(0.5)
#        for ibin in range(middleBin, data.GetNbinsX()+1):
#            data.SetBinContent(ibin, 0)

    return data

def main():
    fin = TFile(args.in_dir, 'read')
    idir = fin.Get(args.cat)
    leg = createLegend()
    data = idir.Get('data_obs').Clone()
    vbf = data.Clone()
    vbf.Reset()
    ggh = vbf.Clone()
    allSig = vbf.Clone()
    stat = vbf.Clone()
    other = stat.Clone()
    inStack = []
    hists = [idir.Get(key.GetName()).Clone() for key in idir.GetListOfKeys()]
    for ihist in hists:
        hist, overlay, leg = applyStyle(ihist.GetName(), ihist, leg)
        if overlay == 0:
            inStack.append(hist)
            stat.Add(hist)
        elif overlay == 1:
            data = hist
        elif overlay == 2:
            vbf = hist
            allSig.Add(hist)
        elif overlay == 3:
            ggh = hist
            allSig.Add(hist)
        elif overlay == 4:
            other.Add(hist)
            stat.Add(hist)
        elif overlay == 5:
            allSig.Add(hist)

    can = createCanvas()
    inStack = formatOther(other, inStack)
    stack, leg = fillStackAndLegend(data, vbf, ggh, inStack, leg)
    stat = formatStat(stat)
    leg.AddEntry(stat, 'Uncertainty', 'f')

    data = blindData(data, allSig, stat)

    high = max(data.GetMaximum(), stat.GetMaximum()) * args.scale
    stack.SetMaximum(high)
    stack.Draw('hist')
    formatStack(stack)
    data.Draw('same lep')
    stat.Draw('same e2')
    vbf.Scale(50)
    vbf.Draw('same hist e')
    ggh.Scale(50)
    ggh.Draw('same hist e')
    leg.Draw()

    ll = TLatex()
    ll.SetNDC(kTRUE)
    ll.SetTextSize(0.06)
    ll.SetTextFont(42)
    if 'et_' in args.cat:
        lepLabel = "e#tau_{e}"
    elif 'mt_' in args.cat:
        lepLabel = "#mu#tau_{#mu}"
    if args.year == '2016':
        lumi = "35.9 fb^{-1}"
    elif args.year == '2017':
        lumi = "41.5 fb^{-1}"
    
    ll.DrawLatex(0.42, 0.92, "{} {}, {} (13 TeV)".format(lepLabel, args.year, lumi))

    cms = TLatex()
    cms.SetNDC(kTRUE)
    cms.SetTextFont(61)
    cms.SetTextSize(0.09)
    cms.DrawLatex(0.16, 0.8, "CMS")

    prel = TLatex()
    prel.SetNDC(kTRUE)
    prel.SetTextFont(52)
    prel.SetTextSize(0.06)
    prel.DrawLatex(0.16, 0.74, "Preliminary")

    if args.cat == 'et_inclusive' or args.cat == 'mt_inclusive':
        catName = 'Inclusive'
    elif args.cat == 'et_0jet' or args.cat == 'mt_0jet':
        catName = '0-Jet'
    elif args.cat == 'et_boosted' or args.cat == 'mt_boosted':
        catName = 'Boosted'
    elif args.cat == 'et_vbf' or args.cat == 'mt_vbf':
        catName = 'VBF enriched'
    else:
      catName = ''

    lcat = TLatex()
    lcat.SetNDC(kTRUE)
    lcat.SetTextFont(42)
    lcat.SetTextSize(0.06)
    lcat.DrawLatex(0.16, 0.68, catName)

    can.cd(2)
    ###########################
    ## create pull histogram ##
    ###########################
    # pull = data.Clone()
    # pull.Add(stat, -1)
    # for ibin in range(pull.GetNbinsX()+1):
    #     pullContent = pull.GetBinContent(ibin)
    #     uncertainty = TMath.Sqrt(pow(stat.GetBinErrorUp(ibin), 2)+pow(data.GetBinErrorUp(ibin), 2))
    #     if uncertainty > 0:
    #         pull.SetBinContent(ibin, pullContent / uncertainty)
    #     else:
    #         pull.SetBinContent(ibin, 0)
    ratio = data.Clone()
    ratio.Divide(stat)
    ratio = formatPull(ratio)
    rat_unc = ratio.Clone()
    for ibin in range(1, rat_unc.GetNbinsX()+1):
        rat_unc.SetBinContent(ibin, 1)
        rat_unc.SetBinError(ibin, ratio.GetBinError(ibin))
    rat_unc.SetMarkerSize(0)
    rat_unc.SetMarkerStyle(8)
    from ROOT import kGray
    rat_unc.SetFillColor(kGray)
    rat_unc.Draw('same e2')
    ratio.Draw('same lep')

    line1, line2 = sigmaLines(data)
    line1.Draw()
    line2.Draw()

    can.SaveAs('Output/plots/{}_{}_{}.pdf'.format(args.prefix, args.cat, args.year))


if __name__ == "__main__":
    main()