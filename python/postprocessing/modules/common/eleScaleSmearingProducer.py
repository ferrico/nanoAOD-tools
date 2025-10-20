import os

# Set up the NATModules eleScaleRes module
def getEleScaleRes(era, tag, is_mc, overwritePt=True, EtDependent=None):
    from PhysicsTools.NATModules.modules.eleScaleRes import eleScaleRes

    # Set default behavior: Standard for 2022, EtDependent for 2023
    #if EtDependent is None:
    #    EtDependent = (era == 2023)
    EtDependent = True

    # Check for supported eras
    if era not in [2022, 2023, 2024]:
        raise ValueError(f"getEleScaleRes: Era {era} not supported")

    if era == 2022:
            if EtDependent:
                #if not "EE" in tag :
                if 20220 == tag:
                    scaleKey = "EGMScale_Compound_Ele_2022preEE"
                    smearKey = "EGMSmearAndSyst_ElePTsplit_2022preEE" if is_mc else None
                    fname = "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-04-15/electronSS_EtDependent.json.gz"
                    #fname = "electronSS_EtDependent_22pre.json.gz"
                else:
                    scaleKey = "EGMScale_Compound_Ele_2022postEE"
                    smearKey = "EGMSmearAndSyst_ElePTsplit_2022postEE" if is_mc else None
                    fname = "electronSS_EtDependent_22post.json.gz"
                    fname = "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-04-15/electronSS_EtDependent.json.gz"
            else:
                #if not "EE" in tag :
                if 20220 == tag:
                    scaleKey = "2022Re-recoBCD_ScaleJSON"
                    smearKey = "2022Re-recoBCD_SmearingJSON" if is_mc else None
                    fname = "electronSS_EtDependent_2022preEE.json.gz"
                else:
                    scaleKey = "2022Re-recoE+PromptFG_ScaleJSON"
                    smearKey = "2022Re-recoE+PromptFG_SmearingJSON" if is_mc else None
                    fname = "electronSS_EtDependent_2022postEE.json.gz"

    elif era == 2023:
        #if not "BPix" in tag:
        if 20230 == tag:
            scaleKey = "EGMScale_Compound_Ele_2023preBPIX"
            smearKey = "EGMSmearAndSyst_ElePTsplit_2023preBPIX" if is_mc else None
            fname = "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-04-15/electronSS_EtDependent.json.gz"
        else:
            scaleKey = "EGMScale_Compound_Ele_2023postBPIX"
            smearKey = "EGMSmearAndSyst_ElePTsplit_2023postBPIX" if is_mc else None
            fname = "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-04-15/electronSS_EtDependent.json.gz"
    elif era == 2024:
            scaleKey = "EGMScale_Compound_Ele_2024"
            smearKey = "EGMSmearAndSyst_ElePTsplit_2024" if is_mc else None
            fname = "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-08-15/electronSS_EtDependent_v1.json.gz"

    else:
        print("ERROR")

    json = fname 
    #"%s/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/nanoAOD_skim/corrections/%s" % (os.environ['CMSSW_BASE'], fname)

    print("***eleScaleRes: era:", era, "tag:", tag, "is MC:", is_mc, "overwritePt:", overwritePt, "EtDependent:", EtDependent, "json:", json)
    return eleScaleRes(json, scaleKey, smearKey, overwritePt)
