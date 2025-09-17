# RNAFoldAssess Tutorial

This tutorial will guide users on how to use RNAFoldAssess. It will cover a brief description of the package's purpose, then run through some examples with data provided in the `./example` directory.

# Purpose

The purpose of the RNAFoldAssess package is to compare the performance of multiple RNA secondary structure prediction tools. The package comes with some predictor models, scoring schemes, and utility functions to support unbiased evaluation. The package is also able to be extended to add other predictor models or scoring schemes and provides instructions for how to do so.

## Overview

Typically, an RNAFoldAssess user will either have a new set of RNA secondary structure data, or a new secondary structure predction model. In either case, the typical goal is to evaluate two or more models against one or more set of data. In either case, the user will pick some number of prediction algorithms to run on some set of data, and then evaluate the performance of each model on each set of data. RNAFoldAssess supports prediction models by wrapping the tool in a `predictor` class. The model's prediciton of a secondary structure is then scored via some scoring scheme. Scoring schemes are supported in RNAFoldAssess via the `Scorer` base class. RNAFoldAssess comes with 3 different scoring schemes, one for chemical mapping, and two for known structure; one that accounts for pseudoknots and one that doesn't.

## Example Use Cases

### Evaluating a new model

Say you have developed a new secondary structure prediction tool and want to compare it with existing tools such as SPOT-RNA and EternaFold. You may decide to run each tool against the PDB RNAs and compare scores. In this case, you would create a wrapper class in the `models/predictors` directory for your tool, as well as one for SPOT-RNA and EternaFold, then create a pipeline for ingesting the data, producing the predictions, scoring the predictions, and comparing the output.

### Evaluating a new sest of RNA data

Another use case for RNAFoldAssess is to evaluate how difficult or easy your new RNA library is to predict. For such a use case, you would likely want to collect performance information on two or more secondary structure prediction models on your new data, as well as some existing data. In this case, you would create a wrapper class for each model and create multiple pipelines to collect performance data on both your new data and existing data.

## Evaluating a new training set of RNA data

As something of a combination of the previous two use cases, perhaps you have developed a new set of RNA data for model training purposes and have used it to retrain an existing model. In this case, you will likely have the out-of-the-box model and the retrained model and want to compare their performance on existing RNA datasets. For such a use case, you will need one wrapper predictor class for the retrained model and one for the default model, then you will create a pipeline to predict and score their performance against another dataset.


# Setting up an Evaluation Pipeline

In this section, we will use the example data in `/tutorial` to set up an example pipeline.

## Step 0 - Preparing your data

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

## Step 1 - Loading the Data

in RNAFoldAssess, the `DataPoint` object is the main starting point for almost all operations supported by the package. The `DataPoint` object contains all the data of an individual RNA, such as:
* *Name* - a unique identifier for the RNA
* *Sequence* - the nucleotide sequence of the RNA
* *Ground Truth Data* - This is the RNA's structural data. The ground truth can be either a dot-bracket notation (DBN) string or a collection of chemical reactivities at given nucleotides in the RNA.
* *Cohort (optional)* - This is used for grouping RNAs of similar origin together for future detailed analysis. It is optional and thus does not have to be supplied.

Imagine you have an RNA and chemical reactivity data for it. It might look like this:

```
RNA name: Sequence 001
Cohort: DMS Run 5
Sequence: AAACCCUUUGGG
Reactivities: 0.5, 0.5, 0.1, 0.7, 0.3, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
```

You could create a `DataPoint` object directly from this data by hardcoding it into a Python script:

```python
name = "sequence_001"
cohort = "DMS_Run_5"
sequence = "AAACCCUUUGGG"
reactivities = {
    0: 0.5, 1: 0.5, 2: 0.1,
    3: 0.7, 4: 0.3, 5: 0.7,
    6: 0.0, 7: 0.0, 8: 0.0,
    9: 0.0, 10: 0.0, 11: 0.0
}

dp = DataPoint(
    name=name,
    sequence=sequence,
    ground_truth_type="DMS",
    ground_truth_data=reactivities,
    cohort=cohort
)
```

However, RNAFoldAssess comes with methods to import large quantities of this kind of data into a `list` of `DataPoint` objects. The most accessible way is to prepare a CSV file with the following headers:

```
name,sequence,ground_truth_type,ground_truth_data
```

Fill the CSV rows with the adjacent data and use the `init_from_csv_file` method on `DataPoint` as shown in `tutorial/tutorial_scripts/01_loading_data.py`. Running this method will return a list of `DataPoint` objects.

### How to record `ground_truth_data` in the CSV

`DataPoint` objects have a `ground_truth_data` attribute that contains structural data about the RNA. This data is used in the scoring step of the package when a prediction is evlauted against the known data (i.e., the `ground_truth_data`). This can be a dot-bracket notation (DBN) string, or a reactivity map in the case of reactivities.

If a DBN string is being used for `ground_truth_data`, the `ground_truth_type` value needs to be either "DBN" or "dbn". If the `ground_truth_data` is from chemical probing experiments, the `ground_truth_type` needs to be either "DMS", "SHAPE", or "CMCT".

The ***reactivity map*** is a string that has a nucleotide position followed by a reactivity measure, separated by a semicolon (`;`). So if you have the sequence `AACCUUGG`, and you have DMS reactivities for only the first (0.5), third (0.1), and fourth (0.4) nucleotides, your map would look like this:

```
0:0.5;2:0.1;3:0.4
```

Notice that the nucleotide numbers are 0-indexed, so the first nucleotide is at position 0.

You can see an example of a SHAPE data CSV in `tutorial\processed_data\example_data_chem_mapping.csv`, and an example of structural data (that is, with DBN strings instead of reactivity data) in `tutorial\processed_data\example_data_structure.csv`.
