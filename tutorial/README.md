# RNAFoldAssess Tutorial

This tutorial will guide users on how to use RNAFoldAssess. It will cover a brief description of the package's purpose, then run through some examples with data provided in the `./example` directory.

## Example Use Cases

### Evaluating a new model

Say you have developed a new secondary structure prediction tool and want to compare it with existing tools such as SPOT-RNA and EternaFold. You may decide to run each tool against the PDB RNAs and compare scores. In this case, you would create a wrapper class in the `models/predictors` directory for your tool, as well as one for SPOT-RNA and EternaFold, then create a pipeline for ingesting the data, producing the predictions, scoring the predictions, and comparing the output.

### Evaluating a new sest of RNA data

Another use case for RNAFoldAssess is to evaluate how difficult or easy your new RNA library is to predict. For such a use case, you would likely want to collect performance information on two or more secondary structure prediction models on your new data, as well as some existing data. In this case, you would create a wrapper class for each model and create multiple pipelines to collect performance data on both your new data and existing data.

## Evaluating a new training set of RNA data

As something of a combination of the previous two use cases, perhaps you have developed a new set of RNA data for model training purposes and have used it to retrain an existing model. In this case, you will likely have the out-of-the-box model and the retrained model and want to compare their performance on existing RNA datasets. For such a use case, you will need one wrapper predictor class for the retrained model and one for the default model, then you will create a pipeline to predict and score their performance against another dataset.


# Setting up an Evaluation Pipeline

In this section, we will use the example data in `/tutorial` to set up an example pipeline.

## Preparing your data

RNAFoldAssess can accomplish a variety of analysis tasks but requires that the RNA data be formatted in a specific way. There are two acceptable file types for RNA data: JSON and CSV.

### CSV data

RNA data can be caputred in CSV format. The headers for this CSV need to be as follows:

```
name,sequence,ground_truth_type,ground_truth_data
```

For RNA data with chemical mapping readings, the `ground_truth_type` must be one of `DMS`, `SHAPE`, or `CMCT`. For chemical mapping readings, the `ground_truth_data` must be a semicolon (`;`) separated mapping of nucleotide position and reactivity. Consider the following example:

```
name,sequence,ground_truth_type,ground_truth_data
ETERNA_R48_0001,GGAAAGCUACGAGGAUAUGCGUAUCACAAAAGUGAUACGGUGGCAUCAAAAGAUGGCACCGAUGAUCAAAAGAUCAUCGCAGAAGGCGUAGCAAAGAAACAACAACAACAAC,SHAPE,6:-0.1088;7:-0.0451;8:-0.0646;9:-0.0811;10:0.0052;11:0.0716;12:0.214;13:0.6199;14:2.6621;15:0.1187;16:0.1195;17:0.1246;18:0.0018;19:-0.0166;20:-0.0005;21:-0.0166;22:-0.0136;23:-0.0126;24:0.0639;25:0.021;26:0.0253;27:1.1472;28:1.6762;29:1.0517;30:1.4134;31:-0.0346;32:0.0752;33:-0.0217;34:-0.0096;35:0.0239;36:0.1538;37:0.3676;38:0.0531;39:-0.0206;40:-0.0666;41:0.3891;42:0.4166;43:0.0053;44:0.067;45:-0.0062;46:0.0638;47:0.6818;48:1.7145;49:0.834;50:1.3121;51:0.0938;52:0.0359;53:0.062;54:0.0622;55:0.748;56:-0.0455;57:0.0702;58:-0.0203;59:0.0511;60:-0.0002;61:0.0103;62:0.0422;63:-0.051;64:-0.0158;65:-0.0148;66:0.0576;67:0.8079;68:1.5427;69:0.8555;70:1.2436;71:-0.1044;72:0.0165;73:-0.0053;74:-0.0127;75:-0.0026;76:0.0413;77:0.1657;78:0.0231;79:-0.0239;80:0.0411;81:0.0235;82:0.2466;83:0.148;84:0.2373;85:-0.0596
ETERNA_R49_0001,GGAAAGCGUGAAGGAUAUCGCUGCUACGCAAGUAGCAGACUGGCAUGGAAACAUGGCAGUGCGUCACGAAAGUGACGUCGAGAAGGUCACGCAAAGAAACAACAACAACAAC,SHAPE,6:-0.0089;7:0.0204;8:-0.0418;9:-0.04;10:-0.0093;11:0.6421;12:2.0899;13:1.3566;14:3.2181;15:0.7905;16:0.3371;17:-0.1027;18:0.1312;19:-0.0879;20:-0.064;21:-0.0099;22:-0.0398;23:0.0393;24:0.7661;25:-0.2989;26:-0.067;27:0.0651;28:0.4296;29:0.7538;30:0.6129;31:-0.0514;32:-0.035;33:-0.0081;34:-0.0231;35:0.0348;36:0.1978;37:0.1499;38:0.0523;39:-0.07;40:0.068;41:0.1454;42:2.1527;43:-0.0119;44:0.0597;45:0.0052;46:0.0777;47:0.1115;48:0.5463;49:0.2405;50:0.3265;51:-0.0172;52:0.0649;53:0.1763;54:0.0665;55:2.0325;56:-0.0029;57:0.0119;58:0.037;59:-0.3251;60:1.5021;61:0.0744;62:-0.0022;63:-0.0444;64:0.0435;65:0.0826;66:-0.0496;67:0.0742;68:1.3434;69:0.5806;70:0.5659;71:-0.0408;72:0.0981;73:0.0776;74:-0.0471;75:0.8453;76:0.5022;77:0.3368;78:0.2007;79:-0.0132;80:0.1304;81:0.085;82:0.2589;83:0.5904;84:2.3524;85:-0.1839
```

For RNA data with structure data, the `ground_truth_type` must be `DBN` and the `ground_truth_data` must be a dot-bracket notation (DBN) string. Consider the following example:

```
name,sequence,ground_truth_type,ground_truth_data
1KXK_chain_0,GUCUACCUAUCGGGCUAAGGAGCCGUAUGCGAUGAAAGUCGCACGUACGGUUCUAUGCCCGGGGGAAAAC,DBN,.....(((..(((((...(((((((((((((((....)))))..))))))))))..))))))))......
1L2X_chain_0,GGCGCGGCACCGUCCGCGGAACAAACGG,DBN,..(((((......)))))..........
```

There are some utility methods that will convert RNA data into acceptable file formats. For example `init_from_rdat_files` will take a directory path full of `.RDAT` files and convert them to a list of `DataPoint` (a class native to RNAFoldAssess) objects. The `DataPoint` static method `to_csv` can then be used to generate a CSV file properly formatted.

### JSON data

TODO: explain JSON shape requirements

## Using the `PredictionPipeline.run_prediction` Method

The `PredictionPipeline` class has a static method called `run_prediction` that can run in one of three modes. Mode 1 generates predictions from RNA data without scoring the predictions. This is useful if you have RNA data without ground-truth structure information like chemical reactivities. Mode 2 will ingest the output of mode 1 and score the predictions. This is useful if you have ground-truth data that you didn't have before and wish to score existing predictions. Mode 3 is for when you have ground truth data already and want to generate both a prediction and a score in one step. For each mode, the call to `run_prediction` will be slightly different.

### Mode 1 - Generating Predictions with no Score

Mode 1, the default mode, takes your RNA data along with a prediction model and generates a prediction only. That is, there is no scoring involved in this mode. This is most useful for when you have the RNA's sequence data, but not any ground truth data (such as chemical reactivities or structure information) yet. See `tutorial/tutorial_scripts/mode1_generate_predictions_only.py` for example usage.

```python
PredictionPipeline.run_prediction(
    dp_list,
    model,
    output_path,
    prediction_mode
)
```

The `dp_list` parameter takes a `list` of `DataPoint` objects. `DataPoint` objects can be created in various ways, usually by feeding a CSV file to the `DataPoint` class's static `init_from_csv_file` method. See the section above for creating CSV files that work with RNAFoldAssess.

The `model` parameter has to be an object of type `Predictor`. The parent `Predictor` class enforces methods that have to be defined in order for the package to work. This package comes with an `RNAFold` class, a child of `Predictor`. See the example scripts for how to use.

The `output_path` parameter is just a string that defines a relative path for where you want the prediction pipeline's output CSV to go.

The `prediction_mode` parameter tells the `run_prediction` method which mode to run. Mode 1 is the default mode, so in this case, it does not have to be specified.

### Mode 2 - Calculating Score from Previous Predictions

Mode 2 takes the output from Mode 1 and calculates a score for the prediction. The `run_prediction` method determines from your RNA ground-truth data whether to score with DSCI or confusion-matrix-based scoring. See `tutorial/tutorial_scripts/mode2_generate_scores_from_preds.py` for example usage.

```python
PredictionPipeline.run_prediction(
    dp_list,
    output_path,
    input_path,
    prediction_mode
)
```

The `dp_list` parameter takes a `list` of `DataPoint` objects. `DataPoint` objects can be created in various ways, usually by feeding a CSV file to the `DataPoint` class's static `init_from_csv_file` method. See the section above for creating CSV files that work with RNAFoldAssess.

The `output_path` parameter is just a string that defines a relative path for where you want the prediction pipeline's output CSV to go.

The `input_path` parameter is a string and should be a relative path to the file generated by mode 1. It is important that the CSV indicated in this parameter be generated by running a pipeline in mode 1 as the function expects the CSV to have specific columns.

In this case, `prediction_mode` needs to be set to 2. Other acceptable arguments to run in mode 2 are "2" (as in, the string value of 2), `"from predictions"`, `"FROM PREDICTIONS"`, `"from preds"`, and `"FROM PREDS"`

Note that we don't need a `model` input for this mode.

### Mode 3 - Generating Predictions and Score
Mode 3 combines Mode 1 and Mode 2 into one step. If your RNA data already has ground-truth data, use that data along with a prediction model to generate predictions for your RNA's secondarty structure as well as scores for those predictions based on your recorded ground-truth data. See `tutorial/tutorial_scripts/mode3_generate_preds_and_scores.py` for example usage.

```python
PredictionPipeline.run_prediction(
    dp_list,
    model,
    output_path,
    prediction_mode
)
```

The `dp_list` parameter takes a `list` of `DataPoint` objects. `DataPoint` objects can be created in various ways, usually by feeding a CSV file to the `DataPoint` class's static `init_from_csv_file` method. See the section above for creating CSV files that work with RNAFoldAssess.

The `model` parameter has to be an object of type `Predictor`. The parent `Predictor` class enforces methods that have to be defined in order for the package to work. This package comes with an `RNAFold` class, a child of `Predictor`. See the example scripts for how to use.

The `output_path` parameter is just a string that defines a relative path for where you want the prediction pipeline's output CSV to go.

To run mode 3, the `prediction_mode` parameter should be set to either 3,  "with score", "WITH SCORE", "score", or "SCORE".

