import json, os

from Bio.PDB import *
from biopandas.mmcif import PandasMmcif


base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis/latest/all_predictions"
motifs_path = f"{base_dir}/pdb_difficult_motifs.txt"

with open(motifs_path) as fh:
    hard_motifs = [line.strip() for line in fh.readlines()]


motif_data = {}
for hm in hard_motifs:
    _type, seq, stc = hm.split("_")
    seq_stc = zip(seq.split("&"), stc.split("&"))
    # Also adding some fields we'll need
    motif_data[hm] = {"structure_info": [], "datapoint_to_use": "", "pdb_positions": []}
    for ss in seq_stc:
        motif_data[hm]["structure_info"].append(ss)


with open(f"{base_dir}/pdb_missed_motifs.txt") as fh:
    lines = [line.split(" ") for line in fh.readlines()]

dp_motif = [(d[0], d[3]) for d in lines]

for dp, motif in dp_motif:
    motif_data[motif]["datapoint_to_use"] = dp


# with open(f"hard_motifs_with_dps.json", "w") as fh:
#     json.dump(motif_data, fh)

# item = motif_data["HELIX_CACAGU&GCUGUG_((((((&))))))"]["datapoint_to_use"]
# pdb_id = item[:4]

# pmmcif = PandasMmcif().fetch_mmcif(pdb_id)

cif_location = "/common/yesselmanlab/ewhiting/data/crystal_all/release_2024/all_cif_files"

def get_structure(pdb_id):
    location = f"{cif_location}/{pdb_id}.cif"
    parser = MMCIFParser()
    structure = parser.get_structure("structure", location)
    return structure

def get_pdb_id_from_dp_name(dp_name):
    return dp_name[:4]


def get_numbered_chain_from_dp_name(dp_name):
    return dp_name[5:5+len("chain_x")]


rna_three_to_one = {
    'A': 'A', 'C': 'C', 'G': 'G', 'U': 'U',
    'DA': 'A', 'DC': 'C', 'DG': 'G', 'DT': 'T',  # DNA residues (in case of mixed structures)
}


def get_chain_positions(dp_name, target_sequence):
    pdb_id = get_pdb_id_from_dp_name(dp_name)
    # numbered_chain = get_numbered_chain_from_dp_name(dp_name) Don't think I need this yet (or ever)
    sequence_len = len(target_sequence)
    results = []

    structure = get_structure(pdb_id)
    for model in structure:
        for chain in model:
            chain_id = chain.id
            residues = [r for r in chain.get_residues() if r.id[0] == " "]
            chain_sequence = "".join([rna_three_to_one.get(res.resname, 'N') for res in residues])  # Use 'N' for unknown

            # Look for the target sequence in this chain's sequence
            for start_idx in range(len(chain_sequence) - sequence_len + 1):
                if chain_sequence[start_idx:start_idx + sequence_len] == target_sequence:
                    # Record positions of the residues in the matched sequence
                    positions = [res.id[1] for res in residues[start_idx:start_idx + sequence_len]]
                    results.append((chain_id, positions))

    return results


print("Getting pdb locations")
for md in motif_data:
    dp_name = motif_data[md]["datapoint_to_use"]
    seqs_stcs = motif_data[md]["structure_info"]
    positions = []
    for seq, stc in seqs_stcs:
        positions.append(get_chain_positions(dp_name, seq))
    motif_data[md]["pdb_positions"] = positions


test_motif = "HELIX_CACAGU&GCUGUG_((((((&))))))"
# 'HELIX_CACAGU&GCUGUG_((((((&))))))'
# (Pdb) motif_data[test_motif]
# {'structure_info': [('CACAGU', '(((((('), ('GCUGUG', '))))))')], 'datapoint_to_use': '5TPY_chain_0', 'pdb_positions': [[('A', [23, 24, 25, 26, 27, 28])], [('A', [38, 39, 40, 41, 42, 43])]]}

with open(f"hard_motifs_with_dps.json", "w") as fh:
    json.dump(motif_data, fh)

chain_info = {}
for md, values in motif_data.items():
    pdb_id = values["datapoint_to_use"][:4]
    chain_info[pdb_id] = {"predicted_motif": md, "location_ids": []}
    structure_info = values["structure_info"] #  [('CACAGU', '(((((('), ('GCUGUG', '))))))')]
    pdb_positions = values["pdb_positions"]   #  [[('A', [23, 24, 25, 26, 27, 28])], [('A', [38, 39, 40, 41, 42, 43])]]
    assembled_data = list(zip(structure_info, pdb_positions)) # [(('CACAGU', '(((((('), [('A', [23, 24, 25, 26, 27, 28])]), (('GCUGUG', '))))))'), [('A', [38, 39, 40, 41, 42, 43])])]
    for ad in assembled_data:
        # (('CACAGU', '(((((('), [('A', [23, 24, 25, 26, 27, 28])])
        try:
            chain = ad[1][0][0]
            pdb_locs = ad[1][0][1]
            seq = ad[0][0]
            stc = ad[0][1]
            #chain_id-residue-location-
            seq = list(seq)
            for i, residue in enumerate(seq):
                location_id = f"{chain}-{residue}-{pdb_locs[i]}-"
                chain_info[pdb_id]["location_ids"].append(location_id)
        except IndexError:
            print(f"Index error on {md}")
            continue


with open(f"hard_motif_pdb_data.json", "w") as fh:
    json.dump(chain_info, fh)
