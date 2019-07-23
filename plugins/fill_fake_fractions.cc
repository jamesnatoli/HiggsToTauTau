// Copyright 2019 Tyler Mitchell

#include "../include/fill_fake_fraction.h"

#include <iostream>
#include <vector>

#include "../include/CLParser.h"
#include "TFile.h"
#include "TTree.h"

using std::string;
using std::vector;

int main(int argc, char *argv[]) {
    // get CLI arguments
    CLParser parser(argc, argv);
    bool doSyst = parser.Flag("-s");
    string dir = parser.Option("-d");
    string year = parser.Option("-y");
    string suffix = parser.Option("--suf");
    string tree_name = parser.Option("-t");

    // get input file directory
    if (dir.empty()) {
        std::cerr << "You must give an input directory" << std::endl;
        return -1;
    }

    // get channel info
    string channel_prefix, lep_charge;
    if (tree_name.find("etau_tree") != string::npos) {
        channel_prefix = "et";
    } else if (tree_name.find("mutau_tree") != string::npos) {
        channel_prefix = "mt";
    } else if (tree_name.find("tautau_tree") != string::npos) {
        channel_prefix = "tt";
    } else {
        std::cerr << "Um. I don't know that tree. Sorry...";
        return -1;
    }

    // read all files from input directory
    vector<string> files;
    read_directory(dir, &files);
    auto fractions = new FakeFractions(channel_prefix, year, suffix);

    bool cat0(false), cat1(false), cat2(false);
    for (auto ifile : files) {
        auto fin = new TFile((dir + "/" + ifile).c_str(), "read");
        auto tree = reinterpret_cast<TTree *>(fin->Get(tree_name.c_str()));
        string name = ifile.substr(0, ifile.find(".")).c_str();

        // get variables from file
        Int_t is_antiTauIso, OS;
        Float_t vis_mass, mjj, njets, nbjets, MT, weight;
        Float_t higgs_pT, t1_pt;

        tree->SetBranchAddress("evtwt", &weight);
        tree->SetBranchAddress("vis_mass", &vis_mass);
        tree->SetBranchAddress("mjj", &mjj);
        tree->SetBranchAddress("njets", &njets);
        tree->SetBranchAddress("nbjets", &nbjets);
        tree->SetBranchAddress("is_antiTauIso", &is_antiTauIso);
        tree->SetBranchAddress("OS", &OS);
        tree->SetBranchAddress("mt", &MT);
        tree->SetBranchAddress("higgs_pT", &higgs_pT);
        tree->SetBranchAddress("t1_pt", &t1_pt);

        for (auto i = 0; i < tree->GetEntries(); i++) {
            tree->GetEntry(i);

            // only look at opposite-sign events
            if (OS == 0 || MT > 50 || nbjets > 0) {
                continue;
            }
            cat0 = (njets == 0);
            cat1 = (njets == 1 || (njets > 1 && (mjj < 300)));
            cat2 = (njets > 1 && mjj > 300);

            if (is_antiTauIso) {
                if (!(name == "W" || name == "ZJ" || name == "VVJ" || name == "TTJ" ||
                      //  name == "embedded" || name == "TTT" || name == "VVT" ||
                      name == "ZTT" || name == "TTT" || name == "VVT" || name == "Data")) {
                    continue;
                }

                fractions->fillFraction(inclusive, name, vis_mass, njets, weight);
                if (cat0) {
                    fractions->fillFraction(zeroJet, name, vis_mass, njets, weight);
                } else if (cat1) {
                    fractions->fillFraction(boosted, name, vis_mass, njets, weight);
                } else if (cat2) {
                    fractions->fillFraction(vbf, name, vis_mass, njets, weight);
                }
            }
        }
        std::cout << "finished file " << fin->GetName() << std::endl;
        fin->Close();
    }
    fractions->fillQCD();
    fractions->writeTemplates();
}
