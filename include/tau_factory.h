#ifndef TAU_FACTORY_H
#define TAU_FACTORY_H

#include <vector>
#include <string>
#include <iostream>
#include <cmath>
#include "TTree.h"
#include "TLorentzVector.h"

class tau_factory;

////////////////////////////////////////////////////
// Purpose: To hold a single composite tau lepton //
////////////////////////////////////////////////////
class tau {
  friend tau_factory;
private:
  std::string name = "tau";
  Int_t gen_match;
  Float_t pt, eta, phi, mass, charge, px, py, pz, l2_decayMode, dmf, dmf_new, iso;
  Bool_t AgainstTightElectron, AgainstVLooseElectron, AgainstTightMuon, AgainstLooseMuon;
  Float_t VLooseIsoMVA, LooseIsoMVA, MediumIsoMVA, TightIsoMVA, VTightIsoMVA, VVTightIsoMVA;
  TLorentzVector p4;

public:
  tau(Float_t, Float_t, Float_t, Float_t, Float_t);
  ~tau() {};

  // scale tau pT for embedded samples
  void scalePt(Float_t newPt) {
    pt *= newPt;
    p4.SetPtEtaPhiM(pt, eta, phi, mass);
  }

  // getters
  std::string getName()               { return name;                  };
  TLorentzVector getP4()              { return p4;                    };
  Float_t getPt()                     { return pt;                    };
  Float_t getEta()                    { return eta;                   };
  Float_t getPhi()                    { return phi;                   };
  Float_t getMass()                   { return mass;                  };
  Float_t getPx()                     { return px;                    };
  Float_t getPy()                     { return py;                    };
  Float_t getPz()                     { return pz;                    };
  Float_t getIso()                    { return iso;                   };
  Float_t getVLooseIsoMVA()           { return VLooseIsoMVA;          };
  Float_t getLooseIsoMVA()            { return LooseIsoMVA;           };
  Float_t getMediumIsoMVA()           { return MediumIsoMVA;          };
  Float_t getTightIsoMVA()            { return TightIsoMVA;           };
  Float_t getVTightIsoMVA()           { return VTightIsoMVA;          };
  Float_t getVVTightIsoMVA()          { return VVTightIsoMVA;         };
  Float_t getL2DecayMode()            { return l2_decayMode;          };
  Float_t getDecayModeFinding()       { return dmf;                   };
  Float_t  getDecayModeFindingNew()   { return dmf_new;               };
  Bool_t getAgainstTightElectron()    { return AgainstTightElectron;  };
  Bool_t getAgainstVLooseElectron()   { return AgainstVLooseElectron; };
  Bool_t getAgainstTightMuon()        { return AgainstTightMuon;      };
  Bool_t getAgainstLooseMuon()        { return AgainstLooseMuon;      };
  Int_t getGenMatch()                 { return gen_match;             };
  Int_t getCharge()                   { return charge;                };
};

// initialize member data and set TLorentzVector
tau::tau(Float_t Pt, Float_t Eta, Float_t Phi, Float_t M, Float_t Charge) :
  pt(Pt),
  eta(Eta),
  phi(Phi),
  mass(M),
  charge(Charge)
{
  p4.SetPtEtaPhiM(pt, eta, phi, mass);
}

/////////////////////////////////////////////////
// Purpose: To build a collection of taus      //
// from the ntuple                             //
/////////////////////////////////////////////////
class tau_factory {
private:
  Int_t gen_match_2;
  Float_t px_2, py_2, pz_2, pt_2, eta_2, phi_2, m_2, e_2, iso_2, q_2, mt_2;
  Float_t againstElectronTightMVA6_2, againstElectronVLooseMVA6_2, againstMuonTight3_2, againstMuonLoose3_2, l2_decayMode, dmf, dmf_new;
  Float_t byVLooseIsolationMVArun2v1DBoldDMwLT_2, byLooseIsolationMVArun2v1DBoldDMwLT_2, byMediumIsolationMVArun2v1DBoldDMwLT_2,
          byTightIsolationMVArun2v1DBoldDMwLT_2, byVTightIsolationMVArun2v1DBoldDMwLT_2, byVVTightIsolationMVArun2v1DBoldDMwLT_2;

public:
  tau_factory (TTree*, int);
  virtual ~tau_factory () {};
  tau run_factory();
};

// read data from tree Int_to member variables
tau_factory::tau_factory(TTree* input, int year=2017) {
  input -> SetBranchAddress( "px_2",                                    &px_2                                   );
  input -> SetBranchAddress( "py_2",                                    &py_2                                   );
  input -> SetBranchAddress( "pz_2",                                    &pz_2                                   );
  input -> SetBranchAddress( "pt_2",                                    &pt_2                                   );
  input -> SetBranchAddress( "eta_2",                                   &eta_2                                  );
  input -> SetBranchAddress( "phi_2",                                   &phi_2                                  );
  input -> SetBranchAddress( "m_2",                                     &m_2                                    );
  input -> SetBranchAddress( "e_2",                                     &e_2                                    );
  input -> SetBranchAddress( "q_2",                                     &q_2                                    );
  input -> SetBranchAddress( "gen_match_2",                             &gen_match_2                            );
  input -> SetBranchAddress( "againstElectronTightMVA6_2",              &againstElectronTightMVA6_2             );
  input -> SetBranchAddress( "againstElectronVLooseMVA6_2",             &againstElectronVLooseMVA6_2            );
  input -> SetBranchAddress( "againstMuonTight3_2",                     &againstMuonTight3_2                    );
  input -> SetBranchAddress( "againstMuonLoose3_2",                     &againstMuonLoose3_2                    );
  input -> SetBranchAddress( "l2_decayMode",                            &l2_decayMode                           );
  input -> SetBranchAddress( "decayModeFinding_2",                      &dmf                                    );
  input -> SetBranchAddress( "decayModeFindingNewDMs_2",                &dmf_new                                );

  if (year == 2017) {
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTraw",     &iso_2                                  );
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTVLoose",  &byVLooseIsolationMVArun2v1DBoldDMwLT_2 );
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTLoose",   &byLooseIsolationMVArun2v1DBoldDMwLT_2  );
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTMedium",  &byMediumIsolationMVArun2v1DBoldDMwLT_2 );
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTTight",   &byTightIsolationMVArun2v1DBoldDMwLT_2  );
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTVTight",  &byVTightIsolationMVArun2v1DBoldDMwLT_2 );
    input -> SetBranchAddress( "tRerunMVArun2v2DBoldDMwLTVVTight", &byVVTightIsolationMVArun2v1DBoldDMwLT_2);
  } else if (year == 2016) {
    input -> SetBranchAddress( "iso_2",                                   &iso_2                                  );
    input -> SetBranchAddress( "byVLooseIsolationMVArun2v1DBoldDMwLT_2",  &byVLooseIsolationMVArun2v1DBoldDMwLT_2 );
    input -> SetBranchAddress( "byLooseIsolationMVArun2v1DBoldDMwLT_2",   &byLooseIsolationMVArun2v1DBoldDMwLT_2  );
    input -> SetBranchAddress( "byMediumIsolationMVArun2v1DBoldDMwLT_2",  &byMediumIsolationMVArun2v1DBoldDMwLT_2 );
    input -> SetBranchAddress( "byTightIsolationMVArun2v1DBoldDMwLT_2",   &byTightIsolationMVArun2v1DBoldDMwLT_2  );
    input -> SetBranchAddress( "byVTightIsolationMVArun2v1DBoldDMwLT_2",  &byVTightIsolationMVArun2v1DBoldDMwLT_2 );
    input -> SetBranchAddress( "byVVTightIsolationMVArun2v1DBoldDMwLT_2", &byVVTightIsolationMVArun2v1DBoldDMwLT_2);
  } else {
    std::cerr << "Bad year given to tau_factory" << std::endl;
  }
 }

// create electron object and set member data
tau tau_factory::run_factory() {
  tau t(pt_2, eta_2, phi_2, m_2, q_2);
  t.px = px_2;
  t.py = py_2;
  t.pz = pz_2;
  t.iso = iso_2;
  t.gen_match = gen_match_2;
  t.AgainstTightElectron = againstElectronTightMVA6_2;
  t.AgainstVLooseElectron = againstElectronVLooseMVA6_2;
  t.AgainstTightMuon = againstMuonTight3_2;
  t.AgainstLooseMuon = againstMuonLoose3_2;
  t.l2_decayMode = l2_decayMode;
  t.VLooseIsoMVA = byVLooseIsolationMVArun2v1DBoldDMwLT_2;
  t.LooseIsoMVA = byLooseIsolationMVArun2v1DBoldDMwLT_2;
  t.MediumIsoMVA = byMediumIsolationMVArun2v1DBoldDMwLT_2;
  t.TightIsoMVA = byTightIsolationMVArun2v1DBoldDMwLT_2;
  t.VTightIsoMVA = byVTightIsolationMVArun2v1DBoldDMwLT_2;
  t.VVTightIsoMVA = byVVTightIsolationMVArun2v1DBoldDMwLT_2;
  t.dmf = dmf;
  t.dmf_new = dmf_new;

  return t;
}

#endif
