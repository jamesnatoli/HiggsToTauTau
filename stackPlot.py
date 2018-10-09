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
    if name == 'embed':
        hist.SetFillColor(TColor.GetColor("#ffcc66"))
        leg.AddEntry(hist, 'ZTT', 'f')
    elif name == 'ZL':
        hist.SetFillColor(TColor.GetColor("#4496c8"))
        leg.AddEntry(hist, 'ZL', 'f')
    elif name == 'ZJ':
        hist.SetFillColor(TColor.GetColor("#33ff11"))
        leg.AddEntry(hist, 'TTJ', 'f')
    elif name == 'TTT':
        hist.SetFillColor(TColor.GetColor("#9999cc"))
        leg.AddEntry(hist, 'TTT', 'f')
    elif name == 'TTJ':
        hist.SetFillColor(TColor.GetColor("#7799cc"))
        leg.AddEntry(hist, 'TTJ', 'f')
    elif name == 'VV':
        hist.SetFillColor(TColor.GetColor("#12cadd"))
        leg.AddEntry(hist, 'Diboson', 'f')
    elif name == 'W':
        hist.SetFillColor(TColor.GetColor("#de5a6a"))
        leg.AddEntry(hist, 'W+jets', 'f')
    elif name == 'QCD':
        hist.SetFillColor(TColor.GetColor("#ffccff"))
        leg.AddEntry(hist, 'QCD', 'f')
    elif name == 'Data':
        hist.SetLineColor(kBlack)
        overlay = 1
        leg.AddEntry(hist, 'Data', 'lep')
    elif name == 'VBF125':
        hist.SetFillColor(0)
        hist.SetLineWidth(3)
        hist.SetLineColor(TColor.GetColor('#000000'))
        hist.SetLineStyle(7)
        overlay = 2
        leg.AddEntry(hist, 'VBF M=125GeV', 'l')
    # elif name == 'ggH125':
    #     hist.SetFillColor(0)
    #     hist.SetLineWidth(3)
    #     hist.SetLineColor(TColor.GetColor('#000000'))
    #     hist.SetLineStyle(7)
    #     overlay = 2
    #     leg.AddEntry(hist, 'ggH M=125GeV', 'l')
    else:
        return None, -1, leg
    return hist, overlay, leg


def createCanvas():
    can = TCanvas()
    can.Divide(2, 1)
    pad1 = can.cd(1)
    pad1.cd()
    pad1.SetPad(0, .3, 1, 1)
    pad1.SetTopMargin(.1)
    pad1.SetBottomMargin(0.02)
    # pad1.SetLogy()
    pad1.SetTickx(1)
    pad1.SetTicky(1)

    pad2 = can.cd(2)
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
}


def formatStack(stack):
    stack.GetXaxis().SetLabelSize(0)
    stack.GetYaxis().SetTitle('Events / Bin')
    stack.GetYaxis().SetTitleFont(42)
    stack.GetYaxis().SetTitleSize(.05)
    stack.GetYaxis().SetTitleOffset(.92)
    stack.SetTitle('')


def createLegend():
    leg = TLegend(0.65, 0.45, 0.85, 0.85)
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextFont(61)
    leg.SetTextFont(42)
    leg.SetTextSize(0.045)
    return leg


def formatPull(pull):
    pull.SetTitle('')
    pull.SetMaximum(2.8)
    pull.SetMinimum(-2.8)
    pull.SetFillColor(TColor.GetColor('#bbbbbb'))
    pull.SetLineColor(TColor.GetColor('#bbbbbb'))
    pull.GetXaxis().SetTitle(titles[args.var])
    pull.GetXaxis().SetTitleSize(0.18)
    pull.GetXaxis().SetTitleOffset(0.8)
    pull.GetXaxis().SetTitleFont(42)
    pull.GetXaxis().SetLabelFont(42)
    pull.GetXaxis().SetLabelSize(.111)
    pull.GetXaxis().SetNdivisions(505)

    pull.GetYaxis().SetTitle('#frac{Data - Bkg}{Uncertainty}')
    pull.GetYaxis().SetTitleSize(0.16)
    pull.GetYaxis().SetTitleFont(42)
    pull.GetYaxis().SetTitleOffset(.251)
    pull.GetYaxis().SetLabelSize(.12)
    pull.GetYaxis().SetNdivisions(505)
    return pull


def sigmaLines(data):
    low = data.GetBinLowEdge(1)
    high = data.GetBinLowEdge(data.GetNbinsX()) + \
        data.GetBinWidth(data.GetNbinsX())

    ## high line
    line1 = TLine(low, 2., high, 2.)
    line1.SetLineWidth(1)
    line1.SetLineStyle(7)
    line1.SetLineColor(kBlack)

    ## low line
    line2 = TLine(low, -2., high, -2.)
    line2.SetLineWidth(1)
    line2.SetLineStyle(7)
    line2.SetLineColor(kBlack)

    return line1, line2

def main():
    fin = TFile('Templates/template_'+args.var+'.root', 'read')
    idir = fin.Get(args.cat)
    leg = createLegend()
    data = idir.Get('Data').Clone()
    sig = data.Clone()
    sig.Reset()
    stat = sig.Clone()
    stack = THStack()
    hists = [idir.Get(key.GetName()).Clone() for key in idir.GetListOfKeys()]
    hists = sorted(hists, key=lambda hist: hist.Integral())
    for ihist in hists:
        hist, overlay, leg = applyStyle(ihist.GetName(), ihist, leg)
        if overlay == 0:
            stack.Add(hist)
            stat.Add(hist)
        elif overlay == 1:
            data = hist
        elif overlay == 2:
            sig = hist

    can = createCanvas()
    stat = formatStat(stat)
    high = max(data.GetMaximum(), stat.GetMaximum()) * 1.2
    stack.SetMaximum(high)
    stack.Draw('hist')
    formatStack(stack)
    data.Draw('same lep')
    stat.Draw('same e2')
    sig.Scale(50)
    sig.Draw('same hist')
    leg.Draw()

    ll = TLatex()
    ll.SetNDC(kTRUE)
    ll.SetTextSize(0.06)
    ll.SetTextFont(42)
    ll.DrawLatex(0.69, 0.92, "35.9 fb^{-1} (13 TeV)")

    cms = TLatex()
    cms.SetNDC(kTRUE)
    cms.SetTextFont(61)
    cms.SetTextSize(0.09)
    cms.DrawLatex(0.14, 0.8, "CMS")

    prel = TLatex()
    prel.SetNDC(kTRUE)
    prel.SetTextFont(52)
    prel.SetTextSize(0.09)
    prel.DrawLatex(0.23, 0.8, "Preliminary")

    can.cd(2)
    ###########################
    ## create pull histogram ##
    ###########################
    pull = data.Clone()
    pull.Add(stat, -1)
    for ibin in range(pull.GetNbinsX()+1):
        pullContent = pull.GetBinContent(ibin)
        uncertainty = TMath.Sqrt(pow(stat.GetBinErrorUp(ibin), 2)+pow(data.GetBinErrorUp(ibin), 2))
        if uncertainty > 0:
            pull.SetBinContent(ibin, pullContent / uncertainty)
        else:
            pull.SetBinContent(ibin, 0)

    pull = formatPull(pull)
    pull.Draw('hist')

    line1, line2, = sigmaLines(data)
    line1.Draw()
    line2.Draw()

    can.SaveAs('Plots/'+args.var+'_'+args.cat+'.pdf')


if __name__ == "__main__":
    main()
