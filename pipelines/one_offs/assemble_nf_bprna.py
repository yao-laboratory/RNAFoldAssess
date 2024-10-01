import os

from RNAFoldAssess.models.scorers import BasePairScorer


pred_base = "/work/yesselmanlab/ewhiting/neuralfold_outputs/bprna"
pred_files = os.listdir(pred_base)

dbn_base = "/work/yesselmanlab/ewhiting/data/bprna/dbnFiles"
report_base = "/work/yesselmanlab/ewhiting/bprna_preds/redo_reports"

reports = [
    open(f"{report_base}/NeuralFold_master_0_lenience.txt", "w"),
    open(f"{report_base}/NeuralFold_master_1_lenience.txt", "w")
]

# Headers
for r in reports:
    r.write("model_name, dp_name, lenience, sequence, true_structure, predicted_structure, sensitivity, ppv, f1\n")

all_stats = [
    [[], [], []],
    [[], [], []]
]

for pf in pred_files:
    try:
        with open(f"{pred_base}/{pf}") as f:
            data = f.readlines()
        name = pf.split(".")[0]
        seq = data[2].strip()
        pred = data[3].strip()
        dbn_file = f"{dbn_base}/{pf}"
        with open(dbn_file) as f:
            dbn_data = f.readlines()
        dbn = dbn_data[4].strip()
        for lenience in [0, 1]:
            line = f"NeuralFold, {name}, {lenience}, {seq}, {dbn}, {pred}, "
            scorer = BasePairScorer(dbn, pred, lenience)
            scorer.evaluate()
            s = scorer.sensitivity
            p = scorer.ppv
            f1 = scorer.f1
            all_stats[lenience][0].append(s)
            all_stats[lenience][1].append(p)
            all_stats[lenience][2].append(f1)
            line += f"{s}, {p}, {f1}\n"
            reports[lenience].write(line)
    except Exception as e:
        print(f"Problem with {pf}: {e}")
        continue


for i, stats in enumerate(all_stats):
    sensitivity = sum(stats[0]) / len(stats[0])
    ppv = sum(stats[1]) / len(stats[1])
    f1 = sum(stats[2]) / len(stats[2])
    report_string = f"NeuralFold\nLenience: {i}\n"
    report_string += f"Datapoints analyzed: {len(stats[0])}\n"
    report_string += f"Sensitivity: {sensitivity}\nPPV: {ppv}\nF1: {f1}\n"
    with open(f"{report_base}/NeuralFold_{i}_lenience_summary.txt", "w") as f:
        f.write(report_string)
