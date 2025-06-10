import os, shutil

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
start = time.time()

for f in sequence_files:
seq_file = f"{sequence_data_path}/{file}"
    with open(seq_file) as fh:
        data = fh.readlines()
    seq = data[1].strip()

    cmd = f'../simfold/simfold -s "{sequence}" > outputs/rasp/{species}/{name}.dbn'
    os.system(cmd)


end = time.time()
elapsed = end - start

with open(f"{Simfold}_speed_test.txt", "w") as fh:
    fh.write(f"{model_name} took {elapsed} to predict 100 structures")
