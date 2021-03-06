from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, deltaPhi
import math
import ROOT

class SRAnalyzer( Analyzer ):
    '''Select Signal Region'''
    
    def beginLoop(self,setup):
        super(SRAnalyzer,self).beginLoop(setup)
        if "outputfile" in setup.services:
            setup.services["outputfile"].file.cd()
            self.inputCounter = ROOT.TH1F("SRCounter", "SRCounter", 10, 0, 10)
            self.inputCounter.GetXaxis().SetBinLabel(1, "All events")
            self.inputCounter.GetXaxis().SetBinLabel(2, "Trigger")
            self.inputCounter.GetXaxis().SetBinLabel(3, "#Jets > 1")
            self.inputCounter.GetXaxis().SetBinLabel(4, "Jet cuts")
            self.inputCounter.GetXaxis().SetBinLabel(5, "MEt cut")
            self.inputCounter.GetXaxis().SetBinLabel(6, "Muon veto")
            self.inputCounter.GetXaxis().SetBinLabel(7, "Electron veto")
            self.inputCounter.GetXaxis().SetBinLabel(8, "Tau veto")
            self.inputCounter.GetXaxis().SetBinLabel(9, "Photon veto")
    
    def vetoMuon(self, event):
        if len(event.selectedMuons) != 0:
            return False
        return True
    def vetoElectron(self, event):
        if len(event.selectedElectrons) != 0:
            return False
        return True
    def vetoTau(self, event):
        if len(event.selectedTaus) != 0:
            return False
        return True
    def vetoGamma(self, event):
        if len(event.selectedPhotons) != 0:
            return False
        return True

    def selectMet(self, event):
        if event.met.pt() < self.cfg_ana.met_pt:
            return False
#        if event.Category == 1 and deltaPhi(event.fatJets[0].phi(), event.met.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
#        if (event.Category == 2 or event.Category == 3) and deltaPhi(event.JetPostCuts[0].phi(), event.met.phi()) > self.cfg_ana.deltaPhi1met:
#            return True
        return True
        
    def process(self, event):
        event.isSR = False

        if not self.selectMet(event):
            return True
        self.inputCounter.Fill(4)
        # Muon veto
        if not self.vetoMuon(event):
            return True
        self.inputCounter.Fill(5)
        # Electron veto
        if not self.vetoElectron(event):
            return True
        self.inputCounter.Fill(6)
        # Tau veto
        if not self.vetoTau(event):
            return True
        self.inputCounter.Fill(7)
        # Photon veto
        if not self.vetoGamma(event):
            return True
        self.inputCounter.Fill(8)
        
        event.isSR = True
        return True
