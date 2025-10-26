# RNAFoldAssess Tutorial

This tutorial will guide users on how to use RNAFoldAssess. It will cover a brief description of the package's purpose, then run through some examples with data provided in the `./example` directory.

# Installation

If you have not yet installed RNAFoldAssess, please follow these instructions:

```
> git clone git@github.com:yao-laboratory/RNAFoldAssess.git
> cd RNAFoldAssess
> pip isntall -r requirements.txt
> pip install -e .
```

Alternatively, you can download the [RNAFoldAssess code in a .zip file](https://github.com/yao-laboratory/RNAFoldAssess/archive/refs/heads/package-only.zip0) and extract it on your local computer. From the directory in which you extracted it, run the following commands:

```
> cd RNAFoldAssess
> pip install -r requirements.txt
> pip install -e .
```

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

Users can also encapsulate data in JSON. For JSON data, RNAFoldAssess expects a list of dictionaries, where each dictionary has at least a `name` and `sequence` key-value pair, and *either* a `reactivity_map` or `dbn` key-value pair. See the CSV Data section above for an explanation of how those ground-truth types are used.

## Prediction Pipeline Modes

Generating secondary structure predictions from some model for a number of RNAs is a "prediction pipeline." RNAFoldAssess supports three modes for prediction pipelines, all of which can be called via `PredictionPipeline.run_prediction`:

### Mode 1 - Make and Evaluate Prediction

Mode 1 is the most comprehensive pipeline mode. In this mode, a model predicts an RNA secondary structure from a given sequence and that prediction is evaluated based on the provided ground truth. For this mode, the RNA data must have ground truth data included. This mode also requires a model. The method call to run a Mode 1 pipeline is as follows:

```python
PredictionPipeline.run_prediction(
    datapoints, # a Python list of DataPoint objects
    model, # an instance of the `Predictor` class
    output_path, # the path of the CSV file for the results to go
    prediction_mode # Optional, as mode 1 is the default, but you can put the number 1 here
)
```

See the script `tutorial/tutorial_scripts/mode1_generate_preds_and_evals.py` for an example of this mode in use.

### Mode 2 - Make Prediction Only

Mode 2 takes RNA data and a model and generates only a prediction for each RNA in the data; that is, there is no evaluation of the prediction. This is useful if you don't yet have ground truth data or you just want to generate secondary structure predictions for a bunch of data. For this mode, the RNA data does not need to have ground-truth data (though it may). Using this mode requires as model. The method call to run a Mode 2 pipeline is as follows:

```python
PredictionPipeline.run_prediction(
    datapoints, # a Python list of DataPoint objects
    model, # an instance of the `Predictor` class
    output_path, # the path of the CSV file for the results to go
    prediction_mode # For mode 2, this value can be 2, without evaluation, WITHOUT evaluation, no evaluation, or NO EVALUATION
)
```

See the script `tutorial/tutorial_scripts/mode2_generate_preds_only.py` for an example of this mode in use.

### Mode 3 - Evaluate Existing Predictions

Mode 3 takes a CSV generated by Mode 2 and performs evaluation on all the secondary structure predictions. To run Mode 3, the user has to provide a list of `DataPoint` objects and the path to the CSV generated by a Mode 2 output. There is no requirement to provide a model. The method call to run a Mode 3 pipeline is as follows:

```python
PredictionPipeline.run_prediction(
    datapoints, # a Python list of DataPoint objects
    output_path, # the path of the CSV file for the results to go
    input_path, # the path to the CSV output by a Mode 2 pipeline
    prediction_mode # For mode 3, this value can be 3, from predictions, FROM PREDICTIONS, from preds, or FROM PREDS
)
```
