import json
import numpy as np
import awkward as ak
from time import perf_counter

offline_jets = ak.from_parquet("offline_jets.parquet")
trigger_jets = ak.from_parquet("trigger_jets.parquet")

def AssignByLoops(offline_jets, trigger_jets, event_num=-1):
    offline_jets = offline_jets[:event_num]
    trigger_jets = trigger_jets[:event_num]
    
    # Step 1: Calculating dRs
    ti_dR = perf_counter()
    dRs = np.zeros(len(trigger_jets),dtype=object)

    # looping over events
    for event in range(len(dRs)):
        if event%10000==0: print(event)
        dRs[event] = np.zeros(len(trigger_jets[event]),dtype=object)
        
        # looping over trigger_jets
        for t, trigger_jet in enumerate(trigger_jets[event]):
            dRs[event][t] = np.zeros(len(offline_jets[event]))
            
            # looping over offline_jets
            for j, offline_jet in enumerate(offline_jets[event]):
                dR = np.sqrt((trigger_jet.eta-offline_jet.eta)**2 + (trigger_jet.phi-offline_jet.phi)**2)
                dRs[event][t][j] = dR
    tf_dR = perf_counter()

    # Step 2: Producing array of filterBits
    ti_fB = perf_counter()
    filterBitsToAdd = list(np.zeros(len(dRs),dtype=object))

    # looping over events
    for event in range(len(dRs)):
        if event%10000==0: print(event)
        filterBitsToAdd[event] = list(np.full(len(offline_jets[event]),-999))

        # looping over trigger_jets
        for trigjet in range(len(dRs[event])):
            min_index = ak.argmin((dRs[event][trigjet]))
            filterBitsToAdd[event][min_index] = trigger_jets[event][trigjet].filterBits
    tf_fB = perf_counter()

    # Step 3: Assigning filterBits to appropriate jets
    offline_jets = ak.with_field(offline_jets, filterBitsToAdd, "filterBits")

    # Recording times
    t_dR  = tf_dR - ti_dR
    t_fB  = tf_fB - ti_fB
    t_tot = tf_fB - ti_dR
    return offline_jets, t_dR, t_fB, t_tot

def AssignByVector(offline_jets, trigger_jets, event_num=-1):
    offline_jets = offline_jets[:event_num]
    trigger_jets = trigger_jets[:event_num]

    # Step 1: Calculating dRs
    ti_dR = perf_counter()
    TrigOFFcombo = ak.cartesian({"tri": trigger_jets, "off": offline_jets[:,np.newaxis]})
    dRs = np.sqrt((TrigOFFcombo.tri.eta-TrigOFFcombo.off.eta)**2 + (TrigOFFcombo.tri.phi-TrigOFFcombo.off.phi)**2)
    tf_dR = perf_counter()

    # Step 2: Producing array of filterBits
    ti_fB = perf_counter()
    mindRindex = ak.argmin(dRs,axis=-1)
    filterBitsToAdd = np.full(np.shape(ak.pad_none(offline_jets.eta,ak.max(ak.num(offline_jets.eta))+1,axis=-1)),-999)
    event_index = np.expand_dims(np.arange(len(filterBitsToAdd)),-1)
    mindRindex = ak.fill_none(ak.pad_none(mindRindex,ak.max(ak.num(mindRindex))),-1)
    filterBits = ak.fill_none(ak.pad_none(trigger_jets.filterBits,ak.max(ak.num(trigger_jets.filterBits))),-999)

    filterBitsToAdd[event_index,mindRindex] = filterBits
    
    shape_preservation = ak.full_like(offline_jets.eta,True,dtype=bool)
    shape_preservation = ak.fill_none(ak.pad_none(shape_preservation,ak.max(ak.num(offline_jets))+1),False)
    filterBitsToAdd = ak.Array(filterBitsToAdd)[shape_preservation]
    tf_fB = perf_counter()

    # Step 3: Assigning filterBits to appropriate jets
    offline_jets = ak.with_field(offline_jets, filterBitsToAdd, "filterBits")

    # Recording times
    t_dR  = tf_dR - ti_dR
    t_fB  = tf_fB - ti_fB
    t_tot = tf_fB - ti_dR
    return offline_jets, t_dR, t_fB, t_tot

event_nums = [2000000, 665484, 221434, 73680, 24516, 8157, 2714, 903, 300, 100]

print("-----loops-----")
loop_t_dRs, loop_t_fBs, loop_t_tots = [], [], []
for e in event_nums:
    print(f"starting {e}...")
    loop_offline_jets, loop_t_dR, loop_t_fB, loop_t_tot = AssignByLoops(offline_jets, trigger_jets, e)
    loop_t_dRs.append(loop_t_dR)
    loop_t_fBs.append(loop_t_fB)
    loop_t_tots.append(loop_t_tot)
print("\n")

print("-----vectors-----")
vect_t_dRs, vect_t_fBs, vect_t_tots = [], [], []
for e in event_nums:
    print(f"starting {e}...")
    vect_offline_jets, vect_t_dR, vect_t_fB, vect_t_tot = AssignByVector(offline_jets, trigger_jets, e)
    vect_t_dRs.append(vect_t_dR)
    vect_t_fBs.append(vect_t_fB)
    vect_t_tots.append(vect_t_tot)

timedict = {
    "event_nums": event_nums,
    "loop_t_dRs": loop_t_dRs,
    "loop_t_fBs": loop_t_fBs, 
    "loop_t_tots": loop_t_tots,
    "vect_t_dRs": vect_t_dRs, 
    "vect_t_fBs": vect_t_fBs,
    "vect_t_tots": vect_t_tots
}

with open('times.json', 'w') as f: json.dump(timedict, f, indent=4)