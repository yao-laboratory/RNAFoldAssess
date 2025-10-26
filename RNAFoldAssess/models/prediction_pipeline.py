from pathlib import Path
from typing import Union

from RNAFoldAssess.models import DataPoint
from RNAFoldAssess.models.predictors import Predictor


class PredictionPipeline:
    PREDICITON_MODES = {
        'with score': 1,
        'WITH SCORE': 1,
        'score': 1,
        'SCORE': 1,
        1: 1,
        'without evaluation': 2,
        'WITHOUT EVALUATION': 2,
        'no evaluation': 2,
        'NO EVALUATION': 2,
        2: 2,
        'from predictions': 3,
        'FROM PREDICTIONS': 3,
        'from preds': 3,
        'FROM PREDS': 3,
        3: 3,
    }

    @staticmethod
    def run_prediction(dp_list, model:Union[Predictor, None]=None, output_path:Union[str, Path]="./predictions_no_score.csv", input_path:Union[str, Path]="", prediction_mode=1):
        if prediction_mode not in PredictionPipeline.PREDICITON_MODES:
            raise ValueError(f'Invalid prediction mode: {prediction_mode}. Supported modes are: {list(PredictionPipeline.PREDICITON_MODES.keys())}')
        mode = PredictionPipeline.PREDICITON_MODES[prediction_mode]

        if mode == 1:
            if not model:
                raise Exception("Must provide Predictor model for mode 1")
            PredictionPipeline.to_csv_file_with_prediction_and_score(dp_list, model, output_path)
        elif mode == 2:
            if not model:
                raise Exception("Must provide predictor model for mode 2")
            PredictionPipeline.to_csv_file_with_prediction(dp_list, model, output_path)
        elif mode == 3:
            if input_path == "":
                raise Exception("No prediction CSV provided")
            PredictionPipeline.to_csv_from_pred_only(dp_list, input_path, output_path)


    @staticmethod
    def to_csv_file_with_prediction(dp_list, model:Predictor, path:Union[str, Path]="./predictions_no_score.csv"):
        lines = ["model,name,sequence,prediction"]
        for dp in dp_list:
            model.execute(dp)
            prediction = model.get_ss_prediction()
            lines.append(f"{model},{dp.name},{dp.sequence},{prediction}")

        with open(path, "w") as fh:
            fh.write("\n".join(lines))
        return path


    @staticmethod
    def to_csv_from_pred_only(dp_list, input_path:Union[str, Path], output_path:Union[str, Path]="./predictions.csv"):
        skipped = 0
        with open(input_path) as fh:
            data = fh.readlines()
        data.pop(0) # Get rid of headers
        data = [d.strip().split(",") for d in data]
        dp_pred_map = {}
        for d in data:
            model = d[0]
            name = d[1]
            pred = d[3]
            dp_pred_map[name] = pred

        dbn_headers = "model,name,sequence,ground_truth_type,ground_truth_data,prediction,sensitivity,ppv,f1\n"
        chem_map_headers = "model,name,sequence,ground_truth_type,ground_truth_data,prediction,DSCI_score,p_value\n"
        lines = []
        for dp in dp_list:
            if dp.name not in dp_pred_map:
                print(f"Cannot find {dp.name} in prediction CSV.")
                skipped += 1
                continue
            prediction = dp_pred_map[dp.name]
            score = dp.evaluate_prediction(prediction)
            if "F1" in score.keys():
                headers = dbn_headers
                score_string = f"{score['sensitivity']},{score['PPV']},{score['F1']}"
            else:
                headers = chem_map_headers
                score_string = f"{score['accuracy']},{score['p']}"

            line = f"{model},{dp.name},{dp.sequence},{dp.ground_truth_type},"
            if dp.ground_truth_type in DataPoint.CHEMICAL_MAPPING_TYPES:
                reactivity_map = dp.reactivity_map
                ground_truth_data = ";".join([f"{p}:{r}" for p, r in reactivity_map.items()])
            elif dp.ground_truth_type in ["DBN", "dbn"]:
                ground_truth_data = dp.ground_truth_data
            else:
                ground_truth_data = None
            line += f"{ground_truth_data},{prediction},{score_string}"
            lines.append(line)

        fstring = headers + "\n".join(lines) # type: ignore
        with open(output_path, "w") as fh:
            fh.write(fstring)

        return output_path



    @staticmethod
    def to_csv_file_with_prediction_and_score(dp_list, model:Predictor, path:Union[str, Path]="./predictions.csv"):
        dbn_headers = "model,name,sequence,ground_truth_type,ground_truth_data,prediction,sensitivity,ppv,f1\n"
        chem_map_headers = "model,name,sequence,ground_truth_type,ground_truth_data,prediction,DSCI_score,p_value\n"
        lines = []
        headers = ""
        for dp in dp_list:
            model.execute(dp)
            prediction = model.get_ss_prediction()
            score = dp.evaluate_prediction(prediction)

            if "F1" in score.keys():
                headers = dbn_headers
                score_string = f"{score['sensitivity']},{score['PPV']},{score['F1']}"
            else:
                headers = chem_map_headers
                score_string = f"{score['accuracy']},{score['p']}"

            line = f"{model},{dp.name},{dp.sequence},{dp.ground_truth_type},"
            if dp.ground_truth_type in DataPoint.CHEMICAL_MAPPING_TYPES:
                reactivity_map = dp.reactivity_map
                ground_truth_data = ";".join([f"{p}:{r}" for p, r in reactivity_map.items()])
            elif dp.ground_truth_type in ["DBN", "dbn"]:
                ground_truth_data = dp.ground_truth_data
            else:
                ground_truth_data = None
            line += f"{ground_truth_data},{prediction},{score_string}"
            lines.append(line)

        fstring = headers + "\n".join(lines) # type: ignore
        with open(path, "w") as fh:
            fh.write(fstring)

        return path
