//auto cset = correction::CorrectionSet::from_file("/afs/cern.ch/work/f/ferrico/private/HZZ_Run3_LXP9/CMSSW_14_0_2/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_skim/2022_schemaV2.json");

#include <boost/math/special_functions/erf.hpp>
#include <string>
#include <PhysicsTools/NanoAODTools/interface/EleScaSmear.h>
#include <iostream>

using namespace std;

EleScaSmear::EleScaSmear(string json) : cset(correction::CorrectionSet::from_file(json)){}

double EleScaSmear::pt_smearing(std::string var, double eta, double r9, double pt){
	std::string var2 = "EGMSmearAndSyst_EleEtaR9_" + var;
//	std::cout<<"VAR = "<<var2<<std::endl;
	double rho = cset->at(var2)->evaluate({"smear", eta, r9});
	//double rho = cset->compound()[var]->evaluate({"smear", pt, r9, eta});
	double smearing = rng.Gaus(1., rho);
	double pt_smear = smearing * pt;
	return pt_smear;
}

double EleScaSmear::pt_smearing_UP(std::string var, double eta, double r9, double pt){
        std::string var2 = "EGMSmearAndSyst_EleEtaR9_" + var;
//        std::cout<<"VAR = "<<var2<<std::endl;
	double rho = cset->at(var2)->evaluate({"smear", eta, r9});
	double unc_rho = cset->at(var2)->evaluate({"smear_up", eta, r9});
	double smearing = rng.Gaus(1., rho + unc_rho);
        double pt_smear = smearing * pt;
        return pt_smear;
}

double EleScaSmear::pt_smearing_DOWN(std::string var, double eta, double r9, double pt){
        std::string var2 = "EGMSmearAndSyst_EleEtaR9_" + var;
//        std::cout<<"VAR = "<<var2<<std::endl;
	double rho = cset->at(var2)->evaluate({"smear", eta, r9});
        double unc_rho = cset->at(var2)->evaluate({"smear_down", eta, r9});
        double smearing = rng.Gaus(1., rho - unc_rho);
        double pt_smear = smearing * pt;
        return pt_smear;
}


double EleScaSmear::pt_scale(std::string var, double gain, int run, double eta, double r9, double pt){
	std::string var2 = "EGMScaleVsRun_" + var; 
//	std::cout<<"scale = "<<var2<<std::endl;
	double scale = cset->at(var2)->evaluate({"scale", gain, run, eta, r9, pt});	
	double pt_scale = scale * pt;
	return pt_scale;
}
double EleScaSmear::pt_scale_UP(std::string var, double gain, double run, double eta, double r9, double pt){
        std::string var2 = "EGMScaleVsRun_" + var;
//        std::cout<<"scale = "<<var2<<std::endl;
	double scale = cset->at(var2)->evaluate({"scale", gain, run, eta, r9, pt});
        double pt_scale = scale * pt;
	double unc_pt = cset->at(var2)->evaluate({"scale_up", gain, run, eta, r9, pt});
	double pt_scale_UP = (1 + unc_pt) * pt_scale;
        return pt_scale_UP;
}

double EleScaSmear::pt_scale_DOWN(std::string var, double gain, double run, double eta, double r9, double pt){
        std::string var2 = "EGMScaleVsRun_" + var;
//        std::cout<<"scale = "<<var2<<std::endl;
	double scale = cset->at(var2)->evaluate({"scale", gain, run, eta, r9, pt});
        double pt_scale = scale * pt;
        double unc_pt = cset->at(var2)->evaluate({"scale_down", gain, run, eta, r9, pt});
        double pt_scale_DOWN = (1 - unc_pt) * pt_scale;
        return pt_scale_DOWN;
}
