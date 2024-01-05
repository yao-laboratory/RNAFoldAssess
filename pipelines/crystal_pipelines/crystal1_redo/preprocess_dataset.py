import os


base_dir = "/common/yesselmanlab/ewhiting/data/crystal1_XRAY"
ss_dir = f"{base_dir}/redo_analysis/secondary_structures"
destination_dir = f"{ss_dir}/preprocessed"

def ss_chains_are_symmetric(ss):
    chains = ss.split("&")
    for chain in chains:
        opens = chain.count("(")
        closes = chain.count(")")
        if opens != closes:
            return False
    return True

dbns = [dbn for dbn in os.listdir(ss_dir) if dbn.endswith("dbn")]

for dbn in dbns:
    f = open(f"{ss_dir}/{dbn}")
    lines = f.readlines()
    f.close()
    ss = lines[-1].strip()
    ss = ss.replace("[", ".")
    ss = ss.replace("]", ".")
    breaks = ss.count("&")
    if breaks > 0:
        if ss_chains_are_symmetric(ss):
            data = f'{lines[0]}{lines[1].replace("&", "")}{ss.replace("&", "")}\n'
            f = open(f"{destination_dir}/{dbn}", "w")
            f.write(data)
            f.close()
        else:
            cmd = f"cp {ss_dir}/{dbn} {destination_dir}/{dbn}"
            os.system(cmd)

