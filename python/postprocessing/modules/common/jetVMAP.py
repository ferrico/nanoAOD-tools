import os

def getJetVetoMap(era, tag) :
    #from PhysicsTools.NATModules.modules.jetVetoMap import jetVMAP
    from PhysicsTools.NanoAODTools.postprocessing.modules.common.jetVetoMap import jetVMAP

    if era not in [2022,2023]:
        raise ValueError("getJetvetoMap: Era", era, "not supported")
    print("tag = ", tag)
    if era == 2022:
            if ("Summer22Nano" in tag) or ("2022C" in tag) or ("2022D" in tag):
                folderKey = "2022_Summer22"
                corrName = "Summer22_23Sep2023_RunCD_V1"
            else:
                folderKey = "2022_Summer22EE"
                corrName = "Summer22EE_23Sep2023_RunEFG_V1"
    
    elif era == 2023:
            if ("Summer23Nano" in tag) or ("2023C" in tag):
                folderKey = "2023_Summer23"
                corrName = "Summer23Prompt23_RunC_V1"
            else:
                folderKey = "2023_Summer23BPix"
                corrName = "Summer23BPixPrompt23_RunD_V1"

    json_JVMAP = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/%s/jetvetomaps.json.gz" % (folderKey)
    veto_map_name= "jetvetomap"
    print("folder key ",folderKey)
    print("corrName ", corrName)
    print("***jetJVMAP: era:", era, "tag:", tag)

    return jetVMAP(json_JVMAP, corrName, veto_map_name)
