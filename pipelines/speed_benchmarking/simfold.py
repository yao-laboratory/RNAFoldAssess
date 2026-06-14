import os, time, shutil

model_name = "Simfold"

sequence_data_path = "/work/yesselmanlab/ewhiting/data/bprna/speed_dataset_fasta"

sequence_files = os.listdir(sequence_data_path)
# Copy files to scratch
# print("Copying files")
# for f in sequence_files:
#     seq_file = f"{sequence_data_path}/{f}"
#     dest = f"/scratch/{f}"
#     shutil.copy(seq_file, dest)

print("Starting evaluation")
report = ""
for i in range(10):
    start = time.time()
    
    for f in sequence_files:
        seq_file = f"{sequence_data_path}/{f}"
        with open(seq_file) as fh:
            data = fh.readlines()
        seq = data[1].strip()
   
        name = f.split(".")[0]
        cmd = f'/mnt/nrdstor/yesselmanlab/ewhiting/simfold/simfold -s "{seq}" > sim_outputs/{name}.dbn'
        os.system(cmd)
    
    
    end = time.time()
    elapsed = end - start
    report += f"Run {i + 1}: {elapsed}\n"
report += "For 100 structures"

with open(f"{model_name}_speed_test.txt", "w") as fh:
    fh.write(report)
