import os

r_data_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only/uniques"
r_pdbs = os.listdir(r_data_dir)
p_data_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein/uniques"
p_pdbs = os.listdir(p_data_dir)
r_dest = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only/preprocessed"
p_dest = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein/preprocessed"


def pre_process(pdbs, data_dir, destination):
    for pdb in pdbs:
        file = f"{data_dir}/{pdb}"
        f = open(file)
        lines = f.readlines()
        f.close()
        ss = lines[-1].strip()
        ss.replace("[", ".")
        ss.replace("]", ".")
        breaks = ss.count("&")
        if breaks > 0:
            if ss_chains_are_symmetric(ss):
                data = f'{lines[0]}{lines[1].replace("&", "")}{ss.replace("&", "")}\n'
                f = open(f"{destination}/{pdb}", "w")
                f.write(data)
                f.close()
        else:
            cmd = f"cp {data_dir}/{pdb} {destination}/{pdb}"
            os.system(cmd)


def ss_chains_are_symmetric(ss):
    chains = ss.split("&")
    for chain in chains:
        opens = chain.count("(")
        closes = chain.count(")")
        if opens != closes:
            return False
    return True


pre_process(r_pdbs, r_data_dir, r_dest)
pre_process(p_pdbs, p_data_dir, p_dest)
