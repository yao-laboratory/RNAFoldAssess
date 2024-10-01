import os, sys

args = sys.argv
partition = args[1]


dbn_dir = f"/work/yesselmanlab/ewhiting/data/bprna/dbnFiles_sep/part_{partition}"
destination = "/work/yesselmanlab/ewhiting/bprna_preds/simfold/outputs"
dbn_files = [f for f in os.listdir(dbn_dir) if f.endswith("dbn")]

for df in dbn_files:
    try:
        with open(f"{dbn_dir}/{df}") as fh:
            data = fh.readlines()
        seq = data[3].strip()
        dbn = data[4].strip()
        name = df.strip(".")[0]
        cmd = f'../simfold/simfold - s "{seq}" > {destination}/{name}.dbn'
        os.system(cmd)
        # Add real structure to save time
        os.system(f'\nReal Structure: "{dbn}" >> {destination}/{name}.dbn')
    except:
        continue
