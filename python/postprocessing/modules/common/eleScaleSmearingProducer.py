from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
import ROOT
import os
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import EleScaSmear
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


class eleScaleSmearingProducer(Module):
    def __init__(self, rc_corrections, dataYear, var):
        #p_postproc = '%s/src/PhysicsTools/NanoAODTools/src/' % os.environ[
        #                'CMSSW_BASE']
        #p_roccor = p_postproc
        #if "/EleScaSmear_cc.so" not in ROOT.gSystem.GetLibraries():
        #    p_helper = '%s/EleScaSmear.cc' % p_roccor
        #    print('Loading C++ helper from ' + p_helper)
        #    ROOT.gROOT.ProcessLine('.L ' + p_helper)
        #        self._roccor = EleScaSmear(rc_corrections)
        json = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_skim/corrections/%s" % (os.environ['CMSSW_BASE'], rc_corrections) 
        print (json)
        self.corrModule = EleScaSmear(json)
        self.var = var

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Electron_pt", "F", lenVar="nElectron")
        self.out.branch("Electron_uncorrected_pt", "F", lenVar="nElectron")
        self.out.branch("Electron_pt_UP", "F", lenVar="nElectron")
        self.out.branch("Electron_pt_DOWN", "F", lenVar="nElectron")

        self.is_mc = bool(inputTree.GetBranch("GenJet_pt"))

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getPtCorr(self, ele, run) :
        
        if ele.pt < 209999 or ele.pt > 0.200:
#        if ele.pt < 20 or ele.pt > 200:
            return ele.pt
        
        isData = int(not self.is_mc)

        if self.is_mc:
#            print("Uncorr = " + str(ele.pt))
            pt_corr = self.corrModule.pt_smearing(self.var, ele.eta, ele.r9, ele.pt)
#            print("Corr = " + str(pt_corr))
        else:
            pt_corr = self.corrModule.pt_scale(self.var, ele.seedGain, run, ele.eta, ele.r9, ele.pt)

        return pt_corr


    def getPtCorr_UP(self, ele, run) :

        if ele.pt < 209999 or ele.pt > 0.200:
            return ele.pt

        isData = int(not self.is_mc)

        if self.is_mc:
            pt_corr_UP = self.corrModule.pt_smearing_UP(self.var, ele.eta, ele.r9, ele.pt)
        else:
            pt_corr_UP = self.corrModule.pt_scale_UP(self.var, ele.seedGain, run, ele.eta, ele.r9, ele.pt)

#        print("Corr UP = " + str(pt_corr_UP))

        return pt_corr_UP



    def getPtCorr_DOWN(self, ele, run) :

        if ele.pt < 209999 or ele.pt > 0.200:
            return ele.pt

        isData = int(not self.is_mc)

        if self.is_mc:
            pt_corr_DOWN = self.corrModule.pt_smearing_DOWN(self.var, ele.eta, ele.r9, ele.pt)
        else:
            pt_corr_DOWN = self.corrModule.pt_scale_DOWN(self.var, ele.seedGain, run, ele.eta, ele.r9, ele.pt)

#        print("Corr DOWN = " + str(pt_corr_DOWN))

        return pt_corr_DOWN



    def analyze(self, event):
        eles = Collection(event, "Electron")

        pt_corr = [0.]*len(eles)
        pt_corr_UP = [0.]*len(eles)
        pt_corr_DOWN = [0.]*len(eles)

        isData = int(not self.is_mc)

        for iele, ele in enumerate(eles):

            pt_corr[iele] = self.getPtCorr(ele, event.run)
            pt_corr_UP[iele] = self.getPtCorr_UP(ele, event.run)
            pt_corr_DOWN[iele] = self.getPtCorr_DOWN(ele, event.run)
#            print("FILIPPO PYTHON: uncorr = " + str(ele.pt) + "\t corr = " + str(pt_corr[iele]))
            pt_uncorr = list(ele.pt for ele in eles)
            self.out.fillBranch("Electron_uncorrected_pt", pt_uncorr)
            ########### ELE NOT APPLIED ##########
            #self.out.fillBranch("Electron_pt", pt_corr)
            ########### ELE NOT APPLIED ##########
            self.out.fillBranch("Electron_pt", pt_uncorr)
            self.out.fillBranch("Electron_pt_UP", pt_corr_UP)
            self.out.fillBranch("Electron_pt_DOWN", pt_corr_DOWN)

        return True

eleScaleSmear2022 = lambda: eleScaleSmearingProducer('electronSS_EtDependent_22pre.json.gz', 2022, "2022preEE")
eleScaleSmear2022EE = lambda: eleScaleSmearingProducer('electronSS_EtDependent_22post.json.gz', 2022, "2022postEE")
eleScaleSmear2023 = lambda: eleScaleSmearingProducer('electronSS_EtDependent_23preBPIX.json.gz', 2023, "2023preBPIX")
eleScaleSmear2023BPix = lambda: eleScaleSmearingProducer('electronSS_EtDependent_23postBPIX.json.gz', 2023, "2023postBPIX")
