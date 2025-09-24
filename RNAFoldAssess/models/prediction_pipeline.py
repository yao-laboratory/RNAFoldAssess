from RNAFoldAssess.models import *


class PredictionPipeline:
    PREDICITON_MODES = {
        'without score': 1,
        'WITHOUT SCORE': 1,
        'no score': 1,
        'NO SCORE': 1,
        1: 1,
        'with score': 2,
        'WITH SCORE': 2,
        'score': 2,
        'SCORE': 2,
        2: 2,
    }
    @staticmethod
    def run_prediction(dp_list, model:Predictor, output_path:Union[str, Path]="./predictions_no_score.csv", prediction_mode=1):
        if prediction_mode not in PredictionPipeline.PREDICITON_MODES:
            raise ValueError(f'Invalid prediction mode: {prediction_mode}. Supported modes are: {list(PredictionPipeline.PREDICITON_MODES.keys())}')
        mode = PredictionPipeline.PREDICITON_MODES[prediction_mode]

        if mode == 1:
            DataPoint.to_csv_file_with_prediction(dp_list, model, output_path)
        elif mode == 2:
            DataPoint.to_csv_file_with_prediction_and_score(dp_list, model, output_path)

