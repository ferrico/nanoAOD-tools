from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import os
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import MuonScaRe
import numpy as np
from math import pi

def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg
               for arg in e.args):
            print(
                'WARNING: catching exception and returning -1. Exception arguments: %s'
                % e.args)
            return -1.
        else:
            raise e


class muonScaleResProducer(Module):
    def __init__(self, rc_corrections, dataYear):
        #p_postproc = '%s/src/PhysicsTools/NanoAODTools/python/postprocessing' % os.environ[
        #        p_postproc = '%s/src/PhysicsTools/NanoAODTools/src/' % os.environ[
        #                'CMSSW_BASE']
        #        p_roccor = p_postproc + '/data'
        #        p_roccor = p_postproc
        #        if "/MuonScaRe_cc.so" not in ROOT.gSystem.GetLibraries():
        #            p_helper = '%s/MuonScaRe.cc' % p_roccor
        #            print('Loading C++ helper from ' + p_helper)
        #            ROOT.gROOT.ProcessLine('.L ' + p_helper)
        #        self._roccor = MuonScaRe(rc_corrections)
        json = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_skim/corrections/%s" % (os.environ['CMSSW_BASE'], rc_corrections) 
        print (json)
        self.corrModule = MuonScaRe(json)

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Muon_pt", "F", lenVar="nMuon")
        self.out.branch("Muon_uncorrected_pt", "F", lenVar="nMuon")
        self.out.branch("Muon_pt_scaleUP", "F", lenVar="nMuon")
        self.out.branch("Muon_pt_scaleDOWN", "F", lenVar="nMuon")
        self.out.branch("Muon_pt_resUP", "F", lenVar="nMuon")
        self.out.branch("Muon_pt_resDOWN", "F", lenVar="nMuon")

        self.is_mc = bool(inputTree.GetBranch("GenJet_pt"))

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getPtCorr(self, muon) :
        
        if muon.pt < 26 or muon.pt > 200:
            return muon.pt
        
        isData = int(not self.is_mc)
        
        scale_corr = self.corrModule.pt_scale(isData, muon.pt, muon.eta, muon.phi, muon.charge)
        pt_corr = scale_corr

        if self.is_mc:
            smear_corr = self.corrModule.pt_resol(scale_corr, muon.eta, muon.nTrackerLayers)
            pt_corr = smear_corr

        return pt_corr

    def getPtCorrScaleVar(self, muon, updn) :
        
        if muon.pt < 26 or muon.pt > 200:
            return muon.pt
        
        scale_corr = self.corrModule.pt_scale_var(muon.pt, muon.eta, muon.phi, muon.charge, updn)
        pt_corr = scale_corr

        return pt_corr

    def getPtCorrResVar(self, muon, pt_corrected, updn) :

        if muon.pt < 26 or muon.pt > 200:
            return muon.pt

        scale_corr = self.corrModule.pt_resol_var(muon.pt, pt_corrected, muon.eta, updn)
        pt_corr = scale_corr

        return pt_corr

    def analyze(self, event):
        muons = Collection(event, "Muon")

        pt_corr = [0.]*len(muons)
        pt_resolUP = [0.]*len(muons)
        pt_resolDOWN = [0.]*len(muons)
        pt_scaleUP = [0.]*len(muons)
        pt_scaleDOWN = [0.]*len(muons)

        isData = int(not self.is_mc)

        for imu, muon in enumerate(muons):
            seedSeq = np.random.SeedSequence([event.luminosityBlock, event.event, int(abs((muon.phi/pi*100.)%1)*1e10), 351740215])
            self.corrModule.setSeed(int(seedSeq.generate_state(1,np.uint64)[0]))

            pt_corr[imu] = self.getPtCorr(muon)
            pt_resolUP[imu] = self.getPtCorrResVar(muon, pt_corr[imu], "up")
            pt_resolDOWN[imu] = self.getPtCorrResVar(muon, pt_corr[imu], "dn")
            pt_scaleUP[imu] = self.getPtCorrScaleVar(muon, "up")
            pt_scaleDOWN[imu] = self.getPtCorrScaleVar(muon, "dn")

            pt_uncorr = list(mu.pt for mu in muons)
            self.out.fillBranch("Muon_uncorrected_pt", pt_uncorr)
            self.out.fillBranch("Muon_pt", pt_corr)
            self.out.fillBranch("Muon_pt_scaleUP", pt_scaleUP)
            self.out.fillBranch("Muon_pt_scaleDOWN", pt_scaleDOWN)
            self.out.fillBranch("Muon_pt_resUP", pt_resolUP)
            self.out.fillBranch("Muon_pt_resDOWN", pt_resolDOWN)

        return True


muonScaleRes2016 = lambda: muonScaleResProducer('2022_schemaV2.json', 2016)
muonScaleRes2017 = lambda: muonScaleResProducer('2022_schemaV2.json', 2017)
muonScaleRes2018 = lambda: muonScaleResProducer("2022_schemaV2.json", 2022)
muonScaleRes2022 = lambda: muonScaleResProducer("2022_Summer22.json", 2022)
muonScaleRes2022EE = lambda: muonScaleResProducer("2022_Summer22EE.json", 2022)
muonScaleRes2023 = lambda: muonScaleResProducer("2023_Summer23.json", 2023)
muonScaleRes2023BPix = lambda: muonScaleResProducer("2023_Summer23BPix.json", 2023)
