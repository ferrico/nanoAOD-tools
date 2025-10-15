import os
def getMuonScaleRes(era, tag, is_mc, overwritePt=True) :
    from PhysicsTools.NATModules.modules.muonScaleRes import muonScaleRes 

    if era not in [2022, 2023, 2024]:  # Add support for 2023
        raise ValueError(f"getMuonScaleRes: Era {era} is not supported")

    if era == 2022:
        if not "EE" in tag :
            fname = "2022_Summer22.json"
        else :
            fname = "2022_Summer22EE.json"
    elif era == 2023:
        if not "BPix" in tag:
            fname = "2023_Summer23.json"
        else:
            fname = "2023_Summer23BPix.json"
    elif era == 2024:
            fname = "2024.json"
    else:
        print("ERROR")

    # Json files for Muons Scale and Smearing corrections are taken from https://gitlab.cern.ch/cms-muonPOG/muonscarekit/-/tree/master/corrections
    json = "%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_skim/corrections/%s" % (os.environ['CMSSW_BASE'], fname)

    print("***muonScaleRes: era:", era, "tag:", tag, "is MC:", is_mc, "overwritePt:", overwritePt, "json:", json)
    return muonScaleRes(json, is_mc, overwritePt)

