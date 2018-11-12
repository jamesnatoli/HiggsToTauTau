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
args = parser.parse_args()

from ROOT import TFile, TLegend, TH1F, TCanvas, THStack, kBlack, TColor, TLatex, kTRUE, TMath, TLine, gStyle
from glob import glob
gStyle.SetOptStat(0)


def applyStyle(name, hist, leg):
    overlay = 0
    print name, hist.Integral()
    if name == 'ZTT':
        hist.SetFillColor(TColor.GetColor("#f9cd66"))
        hist.SetName("ZTT")
    elif name == 'TTT':
        hist.SetFillColor(TColor.GetColor("#cfe87f"))
        hist.SetName('TTT')
    elif name == 'ZJ' or name == 'TTJ' or name == 'VV' or name == 'EWKZ' or name == 'W' or name == 'ZL':
        hist.SetFillColor(TColor.GetColor("#000000"))
        overlay = 4
    elif name == 'QCD':
        hist.SetFillColor(TColor.GetColor("#ffccff"))
        hist.SetName('QCD')
    elif name == 'Data':
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
    can = TCanvas('can', 'can', 600, 800)
    can.Divide(3, 1)
    pad1 = can.cd(1)
    pad1.cd()
    pad1.SetPad(0, .5, 1, 1)
    pad1.SetTopMargin(.1)
    pad1.SetBottomMargin(0.02)
    # pad1.SetLogy()
    pad1.SetTickx(1)
    pad1.SetTicky(1)

    pad2 = can.cd(2)
    pad2.SetPad(0, .3, 1, .5)
    pad2.SetTopMargin(0.06)
    pad2.SetBottomMargin(0.032)
    pad2.SetTickx(1)
    pad2.SetTicky(1)

    pad3 = can.cd(3)
    pad3.SetPad(0, 0, 1, .3)
    pad3.SetTopMargin(0.06)
    pad3.SetBottomMargin(0.35)
    pad3.SetTickx(1)
    pad3.SetTicky(1)

    can.cd(1)

    return can


def formatStat(stat):
    stat.SetMarkerStyle(0)
    stat.SetLineWidth(2)
    stat.SetLineColor(0)
    stat.SetFillStyle(3002)
    stat.SetFillColor(kBlack)
    return stat


titles = {
    'el_pt': 'Electron p_{T} [GeV]',
    't1_pt': 'Tau p_{T} [GeV]',
    'met': 'Missing E_{T} [GeV]',
    'pt_sv': 'SVFit p_{T} [GeV]',
    'm_sv': 'SVFit Mass [GeV]',
    'mjj': 'Dijet Mass [GeV]',
    'Dbkg_VBF': 'MELA VBF Disc',
    'Dbkg_ggH': 'MELA ggH Disc',
    'NN_disc': 'NN Disc.',
    'Q2V1': 'Q^2 V1',
    'Q2V2': 'Q^2 V2',
    'Phi': '#phi',
    'Phi1': '#phi_1',
    'costheta1': 'Cos(#theta_1)',
    'costheta2': 'Cos(#theta_2)',
    'costhetastar': 'Cos(#theta*)',
    'nbjets': 'N(b-jets)'
}

def formatStack(stack):
    stack.GetXaxis().SetLabelSize(0)
    stack.GetYaxis().SetTitle('Events / Bin')
    stack.GetYaxis().SetTitleFont(42)
    stack.GetYaxis().SetTitleSize(.05)
    stack.GetYaxis().SetTitleOffset(.92)
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
    holder = sorted(holder, key=lambda hist: hist.Integral())
    for hist in holder:
        stack.Add(hist)
    for hist in reversed(holder):
        leg.AddEntry(hist, hist.GetName(), 'f')
    return stack, leg

def createLegend():
    leg = TLegend(0.55, 0.45, 0.85, 0.85)
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
    pull.SetMarkerStyle(21)
    pull.GetXaxis().SetTitleSize(0.18)
    pull.GetXaxis().SetTitleOffset(0.8)
    pull.GetXaxis().SetTitleFont(42)
    pull.GetXaxis().SetLabelFont(42)
    pull.GetXaxis().SetLabelSize(.111)
    pull.GetXaxis().SetNdivisions(505)
    pull.GetXaxis().SetLabelSize(0)
    pull.GetXaxis().SetTitleSize(0)

    pull.GetYaxis().SetTitle('Data / MC')
    pull.GetYaxis().SetTitleSize(0.12)
    pull.GetYaxis().SetTitleFont(42)
    pull.GetYaxis().SetTitleOffset(.37)
    pull.GetYaxis().SetLabelSize(.12)
    pull.GetYaxis().SetNdivisions(204)
    return pull


def formatSigs(pull):
    pull.SetTitle('')
    pull.SetMaximum(2)
    pull.SetMinimum(0)
    pull.SetMarkerStyle(21)
    pull.SetMarkerColor(kBlack)
    pull.SetLineWidth(1)
    pull.SetLineColor(kBlack)
    pull.GetXaxis().SetTitle(titles[args.var])
    pull.GetXaxis().SetTitleSize(0.14)
    pull.GetXaxis().SetTitleOffset(0.92)
    pull.GetXaxis().SetTitleFont(42)
    pull.GetXaxis().SetLabelFont(42)
    pull.GetXaxis().SetLabelSize(.111)
    pull.GetXaxis().SetNdivisions(505)

    pull.GetYaxis().SetTitle('VBF / ggH')
    pull.GetYaxis().SetTitleSize(0.08)
    pull.GetYaxis().SetTitleFont(42)
    pull.GetYaxis().SetTitleOffset(.55)
    pull.GetYaxis().SetLabelSize(.08)
    pull.GetYaxis().SetNdivisions(204)
    return pull

def sigmaLines(data):
    low = data.GetBinLowEdge(1)
    high = data.GetBinLowEdge(data.GetNbinsX()) + \
        data.GetBinWidth(data.GetNbinsX())

    ## high line
    line1 = TLine(low, 0.5, high, 0.5)
    line1.SetLineStyle(3)
    line1.SetLineColor(kBlack)

    ## mid line
    line2 = TLine(low, 1., high, 1.)
    line2.SetLineStyle(3)
    line2.SetLineColor(kBlack)

    ## low line
    line3 = TLine(low, 1.5, high, 1.5)
    line3.SetLineStyle(3)
    line3.SetLineColor(kBlack)

    return line1, line2, line3

def main():
    fin = TFile('Output/templates/template_'+args.var+'.root', 'read')
    idir = fin.Get(args.cat)
    leg = createLegend()
    data = idir.Get('Data').Clone()
    vbf = data.Clone()
    vbf.Reset()
    ggh = vbf.Clone()
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
        elif overlay == 3:
            ggh = hist
        elif overlay == 4:
            other.Add(hist)
            stat.Add(hist)

    can = createCanvas()
    inStack = formatOther(other, inStack)
    stack, leg = fillStackAndLegend(data, vbf, ggh, inStack, leg)
    stat = formatStat(stat)
    leg.AddEntry(stat, 'Uncertainty', 'f')

    high = max(data.GetMaximum(), stat.GetMaximum()) * 1.6
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
    ll.DrawLatex(0.48, 0.92, "e#tau_{e} 2016, 35.9 fb^{-1} (13 TeV)")

    cms = TLatex()
    cms.SetNDC(kTRUE)
    cms.SetTextFont(61)
    cms.SetTextSize(0.09)
    cms.DrawLatex(0.14, 0.8, "CMS")

    prel = TLatex()
    prel.SetNDC(kTRUE)
    prel.SetTextFont(52)
    prel.SetTextSize(0.06)
    prel.DrawLatex(0.14, 0.74, "Preliminary")

    if args.cat == 'et_inclusive':
        catName = 'Inclusive'
    elif args.cat == 'et_vbf':
        catName = 'VBF enriched'

    lcat = TLatex()
    lcat.SetNDC(kTRUE)
    lcat.SetTextFont(42)
    lcat.SetTextSize(0.06)
    lcat.DrawLatex(0.14, 0.68, catName)

    can.cd(2)
    ###########################
    ## create pull histogram ##
    ###########################

    ratio = data.Clone()
    ratio.Divide(stat)
    ratio = formatPull(ratio)
    rat_unc = ratio.Clone()
    for ibin in range(rat_unc.GetNbinsX()+1):
        rat_unc.SetBinContent(ibin, 1)
        rat_unc.SetBinError(ibin, ratio.GetBinError(ibin))
    rat_unc.SetMarkerSize(0)
    rat_unc.SetMarkerStyle(8)
    from ROOT import kGray
    rat_unc.SetFillColor(kGray)
    rat_unc.Draw('same e2')
    ratio.Draw('same lep')

    line1, line2, line3 = sigmaLines(data)
    line1.Draw()
    line2.Draw()
    line3.Draw()

    can.cd(3)
    sig_rat = vbf.Clone()
    sig_rat.Divide(ggh)
    sig_rat = formatSigs(sig_rat)
    sig_rat.Draw('same lep')

    line1.Draw()
    line2.Draw()
    line3.Draw()


    can.SaveAs('Output/plots/'+args.var+'_'+args.cat+'.pdf')


if __name__ == "__main__":
    main()
