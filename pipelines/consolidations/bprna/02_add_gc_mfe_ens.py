import os

# go to /common/yesselmanlab/ewhiting/vienna

import vienna

base_dir = "/mnt/nrdstor/yesselmanlab/ewhiting/reports/higher_level_analysis"
src_dir = f"{base_dir}/consolidated"

files = {
    "easy": f"{src_dir}/bprna_easy_cases.txt",
    "hard": f"{src_dir}/bprna_hard_cases.txt"
}

def get_gc_content(seq):
    gs = seq.count("G") + seq.count("g")
    cs = seq.count("C") + seq.count("c")
    gc_content = (gs + cs) / len(seq)
    return gc_content

def get_ed_and_mfe(seq):
    fr = vienna.fold(seq)
    ens_defect = fr.ens_defect
    mfe = fr.mfe
    return ens_defect, mfe

print("Starting")
for kind, f in files.items():
    print(f"Working {kind} cases")
    new_file_name = f.replace(f"{kind}_cases.txt", f"{kind}_cases_with_data.txt")
    new_file = open(new_file_name, "w")
    new_file.write("dp,sequence,structure,gc_content,ensemble_defect,MFE\n")
    with open(f) as fh:
        lines = [line.split(", ") for line in fh.readlines()]
    
    for line in lines:
        name = line[0]
        seq = line[1]
        stc = line[2].strip()
        gc = get_gc_content(seq)
        ed, mfe = get_ed_and_mfe(seq)

        new_line = f"{name},{seq},{stc},{gc},{ed},{mfe}\n"
        new_file.write(new_line)
    new_file.close()

print("Done")
