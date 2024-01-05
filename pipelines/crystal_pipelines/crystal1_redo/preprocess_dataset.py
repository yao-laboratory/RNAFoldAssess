import os


base_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY"
ss_dir = f"{base_dir}/redo_analysis/secondary_structures"
destination_dir = f"{ss_dir}/preprocessed"


def chain_is_symmetric(chain):
    opens = chain.count("(")
    closes = chain.count(")")
    return opens == closes

def write_ss_file(name, header, seq, dbn):
    dbn = dbn.replace("[", ".")
    dbn = dbn.replace("]", ".")
    data = f"{header}\n{seq}\n{dbn}\n"
    f = open(f"{destination_dir}/{name}", "w")
    f.write(data)
    f.close()

def write_chain_ss_files(name, lines):
    header = lines[0].strip()
    seqs = lines[1].strip()
    ss = lines[2].strip()
    chains_ss = ss.split("&")
    chains_seq = seqs.split("&")
    counter = 0
    for seq, dbn in zip(chains_seq, chains_ss):
        if chain_is_symmetric(dbn):
            n, ext = name.split(".")
            new_name = f"{n}_{counter}.{ext}"
            write_ss_file(new_name, header, seq.upper(), dbn)
        counter += 1


dbns = [dbn for dbn in os.listdir(ss_dir) if dbn.endswith("dbn")]
# # for testing
# dbns = dbns[0:10]

progress_counter = 0
dbns_len = len(dbns)
for dbn in dbns:
    if progress_counter % 100 == 0:
        print(f"Working {progress_counter} of {dbns_len}")
    f = open(f"{ss_dir}/{dbn}")
    lines = f.readlines()
    f.close()
    ss = lines[-1].strip()
    breaks = ss.count("&")
    if breaks > 0:
        write_chain_ss_files(dbn, lines)
    else:
        write_ss_file(
            dbn,
            lines[0].strip(),
            lines[1].strip().upper(),
            ss
        )
    progress_counter += 1


