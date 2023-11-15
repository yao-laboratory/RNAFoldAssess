import os



# I need to update the script that checks the canonical page before running this.
# Should probably also make sure Crystal1 is still good.
asterisks = "****************************************************************************"
ss_string = "Secondary structures"

def parse_file(path):
    f = open(path)
    raw_data = f.read()
    f.close()
    data = raw_data.split(asterisks)
    ss_data = None
    for d in data:
        if ss_string in d:
            ss_data = d
            break
    if not ss_data:
        print(f"No secondary structure in {path}")
        return None
    ss_data = ss_data.split("\n")
    whole_seq = ""
    whole_structure = ""
    chains = []
    for i in range(len(ss_data)):
        if "[whole]" in ss_data[i]:
            whole_seq = ss_data[i+1]
            whole_structure = ss_data[i+2]
        if "[chain]" in ss_data[i]:
            chain_id = ss_data[i].split("-")[1].split(" ")[0]
            chains.append({
                "chain_id": chain_id,
                "sequence": ss_data[i+1],
                "structure": ss_data[i+2]
            })
    return {
        "name": path.split(".")[0].split("/")[-1],
        "sequence": whole_seq,
        "structure": whole_structure,
        "chains": chains
    }


def symmetric_chain(ss):
    return ss.count("(") == ss.count(")")

def contains_pseudoknots(ss):
    return ("[" in ss or "]" in ss)


def write_data_to_file(data, base_path, split_tolerance=1):
    if data == None:
        return None
    sf = open(f"{base_path}/symmetric_structures.txt", "w")
    af = open(f"{base_path}/asymmetric_structures.txt", "w")
    pf = open(f"{base_path}/pseudoknot_structures.txt", "w")
    all_data = len(data)
    sf_records = 0
    af_records = 0
    pf_records = 0
    for d in data:
        if d == None:
            continue
        seq = d["sequence"]
        ss = d["structure"]
        count_splits = d["sequence"].count("&")
        if contains_pseudoknots(ss):
            text = f">{d['name']}\n{seq}\n{ss}\n"
            pf.write(text)
            pf_records += 1
        elif count_splits <= split_tolerance:
            seq = seq.replace("&", "")
            ss = ss.replace("&", "")
            if len(seq) != len(ss):
                raise Exception(f"Sequence and structure length different after removing ampersands in {d['name']}")
            text = f">{d['name']}\n{seq}\n{ss}\n"
            sf.write(text)
            sf_records += 1
        else:
            base_name = d["name"]
            chains = d["chains"]
            text = ""
            for chain in chains:
                text += f">{base_name} - {chain['chain_id']}\n{chain['sequence']}\n{chain['structure']}\n"
            all_symmetric = all(symmetric_chain(s["structure"]) for s in chains)
            if all_symmetric:
                sf.write(text)
                sf_records += 1
            else:
                af.write(text)
                af_records += 1
    sf.close()
    af.close()
    pf.close()
    print(f"Total of {all_data} records:")
    print(f"Wrote {sf_records} symmetric records")
    print(f"Wrote {af_records} asymmetric records")
    print(f"Wrote {pf_records} records with pseudoknots")



crystal2_base_path = "/common/yesselmanlab/ewhiting/data/crystal2"

rna_only_base_ss_path = f"{crystal2_base_path}/rna_only/structures"
w_protein_base_ss_path = f"{crystal2_base_path}/with_protein/structures"

rna_only_files = os.listdir(rna_only_base_ss_path)
w_protein_files = os.listdir(w_protein_base_ss_path)



rna_only_data = []
print("Assembling RNA Only data ...")
for f in rna_only_files:
    rna_only_data.append(
        parse_file(f"{rna_only_base_ss_path}/{f}")
    )


w_protein_data = []
print("Assembling RNA-with-protein data ...")
for f in w_protein_files:
    w_protein_data.append(
        parse_file(f"{w_protein_base_ss_path}/{f}")
   )

print("Starting to write RNA only data")
write_data_to_file(rna_only_data, rna_only_base_ss_path)
print("Starting to write with-protein data")
write_data_to_file(w_protein_data, w_protein_base_ss_path)

