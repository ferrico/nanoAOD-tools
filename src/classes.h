#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionScaleFactorWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetParametersWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"
#include "PhysicsTools/NanoAODTools/interface/ReduceMantissa.h"
#include <PhysicsTools/NanoAODTools/interface/MuonScaRe.h>
#include <PhysicsTools/NanoAODTools/interface/EleScaSmear.h>

PyJetResolutionWrapper jetRes;
PyJetResolutionScaleFactorWrapper jetResScaleFactor;
PyJetParametersWrapper jetParams;
WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
