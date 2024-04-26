import os

from RNAFoldAssess.models import DataPoint


species = [
  "arabidopsis",
  "covid",
  "ecoli",
  "HIV",
  "human"
]

species_data = {}
for s in species:
    print(f"Loading data for {s}")
    p = f"/common/yesselmanlab/ewhiting/data/rasp_data/processed/{s}"
    json_files = os.listdir(p)
    species_data[s] = []
    for j in json_files:
        dps = DataPoint.factory(f"{p}/{j}")
        dps = [d for d in dps if len(d.sequence) > 10]
        species_data[s] += dps

destination_dir = "/common/yesselmanlab/ewhiting/data/descriptions"

def generate_len_file_name(species):
    return f"{destination_dir}/rasp_{species}_lengths.txt"

def generate_gc_file_name(species):
    return f"{destination_dir}/rasp_{species}_gc_content.txt"


def get_gc_content(seq):
    seq = seq.strip().upper() # Just in case
    gs = seq.count("G")
    cs = seq.count("C")
    gc_count = gs + cs
    gc_count = float(gc_count)
    slen = float(len(seq))
    gc_content = gc_count / slen
    gc_content = round(gc_content, 6)
    return gc_content


allenf = open(generate_len_file_name("all"), "w")
allgcf = open(generate_gc_file_name("all"), "w")

for s in species:
    print(f"Working {s}")
    dps = species_data[s]
    lenf = open(generate_len_file_name(s), "w")
    gcf = open(generate_gc_file_name(s), "w")
    for d in dps:
        slen = len(d.sequence)
        gc = get_gc_content(d.sequence)
        slen_w = f"{slen}\n"
        gc_w = f"{gc}\n"
        lenf.write(slen_w)
        gcf.write(gc_w)
        allenf.write(slen_w)
        allgcf.write(gc_w)
    lenf.close()
    gcf.close()

allenf.close()
allgcf.close()
