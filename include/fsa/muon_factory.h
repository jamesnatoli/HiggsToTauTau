// Copyright [2018] Tyler Mitchell

#ifndef INCLUDE_FSA_MUON_FACTORY_H_
#define INCLUDE_FSA_MUON_FACTORY_H_

#include <cmath>
#include <string>
#include <vector>
#include "TLorentzVector.h"
#include "TTree.h"
#include "../models/muon.h"

class muon_factory {
 private:
    Float_t px_1, py_1, pz_1, pt_1, eta_1, phi_1, m_1, e_1, q_1, mt_1, iso_1, mediumID, mGenPt, mGenEta, mGenPhi,
        mGenEnergy;
    Int_t gen_match_1;
    std::vector<muon> muons;

 public:
    explicit muon_factory(TTree*);
    virtual ~muon_factory() {}
    void set_process_all() { /* nothing to do */ }
    void run_factory();
    Int_t num_muons() { return muons.size(); }
    muon muon_at(unsigned i) { return muons.at(i); }
    muon good_muon() { return muons.at(0); }
    std::vector<muon> all_muons() { return muons; }
};

// read data from tree into member variabl
muon_factory::muon_factory(TTree* input) {
    input->SetBranchAddress("px_1", &px_1);
    input->SetBranchAddress("py_1", &py_1);
    input->SetBranchAddress("pz_1", &pz_1);
    input->SetBranchAddress("pt_1", &pt_1);
    input->SetBranchAddress("eta_1", &eta_1);
    input->SetBranchAddress("phi_1", &phi_1);
    input->SetBranchAddress("m_1", &m_1);
    input->SetBranchAddress("q_1", &q_1);
    input->SetBranchAddress("mRelPFIsoDBDefault", &iso_1);
    input->SetBranchAddress("gen_match_1", &gen_match_1);
    input->SetBranchAddress("mPFIDMedium", &mediumID);
    input->SetBranchAddress("mGenPt", &mGenPt);
    input->SetBranchAddress("mGenEta", &mGenEta);
    input->SetBranchAddress("mGenPhi", &mGenPhi);
    input->SetBranchAddress("mGenEnergy", &mGenEnergy);
}

// create muon object and set member data
void muon_factory::run_factory() {
    muon mu(pt_1, eta_1, phi_1, m_1, q_1);
    mu.setGenMatch(gen_match_1);
    mu.setIso(iso_1);
    mu.setMediumID(mediumID);
    mu.setGenPt(mGenPt);
    mu.setGenEta(mGenEta);
    mu.setGenPhi(mGenPhi);
    mu.setGenEnergy(mGenEnergy);

    muons = { mu };
}

#endif  // INCLUDE_FSA_MUON_FACTORY_H_
