from RNAFoldAssess.utils import *
from RNAFoldAssess.models.predictors import *


model_name = "NUPACK"
model = NUPACK()


# predict_rasp_with_exons(
#     model,
#     model_name,
#     "",
#     "human",
#     specific_chrs=["chr1"]
# )

specific_chrs = ["chr1"]
species = "human"


base_dir = "/common/yesselmanlab/ewhiting/data/rasp_data"
json_dir = f"{base_dir}/{species}/json_files"
json_files = os.listdir(json_dir)
ch_map = {}
for jf in json_files:
    ch = jf.replace("_exons.json", "")
    if len(specific_chrs) > 0 and ch not in specific_chrs:
        continue
    if species == "human" and ch not in ["chr1", "chr2", "chr18", "chr19"]:
        continue
    with open(f"{json_dir}/{jf}") as fh:
        ch_map[ch] = json.load(fh)
        break


