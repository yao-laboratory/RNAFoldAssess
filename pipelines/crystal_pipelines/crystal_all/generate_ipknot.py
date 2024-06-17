import os, datetime


from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.models.scorers import *


model_name = "IPKnot"
model = IPknot()
model_path = os.path.abspath("/common/yesselmanlab/ewhiting/ipknot-1.1.0-x86_64-linux/ipknot")

pdb_fastas = "/common/yesselmanlab/ewhiting/data/crystal_all/longFastaFiles"
fasta_files = [f for f in os.listdir(pdb_fastas) if f.endswith(".fasta")]

headers = "algo_name, datapoint_name, lenience, sequence, prediction, sensitivity, ppv, f1\n"
dbn_path = "/common/yesselmanlab/ewhiting/data/crystal_all/symmetric_chains_no_pseudoknot"
dps = DataPointFromCrystal.factory_from_dbn_files(dbn_path)
report_base = "/common/yesselmanlab/ewhiting/reports/crystal_all"
r0 = open(f"{report_base}/{model_name}_predictions_0_lenience.txt", "w")
r1 = open(f"{report_base}/{model_name}_predictions_1_lenience.txt", "w")
r0.write(headers)
r1.write(headers)

counter = 0
for dp in dps:
    counter += 1
    if counter % 250 == 0:
        print(f"Working {counter}")
    if len(dp.sequence) < 10:
        continue
    try:
        line_to_write0 = ""
        line_to_write1 = ""
        input_file_path = f"{pdb_fastas}/{dp.name}.fasta"
        model.execute(model_path, input_file_path)
        prediction = model.get_ss_prediction_ignore_pseudoknots()
        r0_scorer = BasePairScorer(dp.true_structure, prediction, 0)
        r1_scorer = BasePairScorer(dp.true_structure, prediction, 1)
        r0_scorer.evaluate()
        r1_scorer.evaluate()

        s0 = r0_scorer.sensitivity
        p0 = r0_scorer.ppv
        f10 = r0_scorer.f1
        s1 = r1_scorer.sensitivity
        p1 = r1_scorer.ppv
        f11 = r1_scorer.f1

        line_to_write0 = f"{model_name}, {dp.name}, 0, {dp.sequence}, {prediction}, {s0}, {p0}, {f10}\n"
        line_to_write1 = f"{model_name}, {dp.name}, 1, {dp.sequence}, {prediction}, {s1}, {p1}, {f11}\n"

        r0.write(line_to_write0)
        r1.write(line_to_write1)
    except:
        continue


r0.close()
r1.close()

