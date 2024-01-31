# RNAFoldAssess

RNAFoldAssess is a framework for comparing the performance of RNA secondary structure prediction algorithms against multiple data sets. The framework provides classes and functions that simplify the process of analzying multiple prediction algorithms (e.g., RNAFold, EternaFold, MXFold), multiple data types (e.g., chemical mapping, crystal structure), or multiple scoring schemes (e.g., DSCI, confusion matrix, etc.).

The framework is specifically designed to be easily extendible. That is, RNAFoldAssess was designed with the intention that users would add their own classes and scripts to run their analyses. Despite this, however, RNAFoldAsssess comes with out of the box support for:
* RNAFold
* ContraFold
* DSCI scoring scheme
* Confusion matrix scoring

# Tutorial

## How to Use the Built-In Algorithms of This Project

The RNAFoldAssess comes with support for two secondary structure prediction algorithms: RNAFold and ContraFold. This section shows you how to use them in the RNAFoldAssess framework.

### ContraFold

To use ContraFold in the RNAFoldAssess framework, you must first install the ContraFold tool on your system. Installation instructions for ContraFold can be found at http://contra.stanford.edu/contrafold/download.html.

Once you have installed ContraFold, copy the path to the package. For example, my ContraFold package is located at `/home/users/ewhiting/EternaFold`.

**NOTE** The path to ContraFold is probably different on your system.
**SECOND NOTE** You can see from the example above that my ContraFold path is in a path for EternaFold. This is because [the EternaFold tool](https://github.com/eternagame/EternaFold) has ContraFold built in and is a little easier to install than the one at the ContraFold link.

Now that you have the path, you can use the `ContraFold` class. The `ContraFold` tool expects a `.seq` file, consider this example seq file which we'll call `rna1.seq`:

```
ACGUGCGCCCACCG
```

Now, get the path to this file. For the sake of this example, let's say the path is `/home/data/rna1.seq`. To generate a secondary structure prediction on this sequence using the `ContraFold` class, you will write the following Python code:

```python
from RNAFoldAssess.models.predictors import ContraFold

predictor = ContraFold()
path_to_contrafold = os.path.abspath("/home/users/ewhiting/EternaFold")
path_to_seq_file = os.path.abspath("/home/data/rna1.seq")

model.execute(path_to_contrafold, path_to_seq_file)
secondary_structure_prediction = model.get_ss_prediction()
```

Note that running the model's `execute` method sets its `output` value. The ContraFold tool outputs multiple lines, so the `get_ss_prediction` method is designed to extract just the dot-bracket notation of the secondary structure prediction from that output. So, if you run the above code, the `prediction` variable will be a string in dot-bracket notation of the ContraFold tool's secondary structure prediction for the RNA sequence in `rna1.seq`. If you want to view the full output of the ContraFold tool, you can retrieve that with `model.output` after running the `execute` method.

### RNAFold

To use RNAFold in the RNAFoldAssess framework, you must first install the ViennaRNA package. Installation instructions for this package can be found at  https://www.tbi.univie.ac.at/RNA/ViennaRNA/doc/html/install.html. Once you have ViennaRNA installed, you have access to RNAFold and can use the `RNAFold` predictor model in RNAFoldAssess.

After installing ViennaRNA, take note of the binary location. For example, mine is located `/home/users/ewhiting/ViennaRNA/bin/RNAFold`.

**NOTE** The path to RNAFold is probably different on your system.
**SECOND NOTE** The RANFold tool expects the system in which it's running to have Java installed and in the path. Please make sure you have Java installed on your system before using.

The RNAFold tool expects a fasta file, consider this example fasta file which we'll call `rna1.fasta`:

```
>rna1
ACGUGCGCCCACCG
```

Now, get the path to this file. For the sake of this example, let's say the path is `/home/data/rna1.fasta`. To generate a secondary structure prediction on this sequence using the `RNAFold` class, you will write the following Python code:

```python
from RNAFoldAssess.models.predictors import RNAFold

model = RNAFold()
path_to_rnafold = os.path.abspath("/home/users/ewhiting/ViennaRNA/bin/RNAFold")
path_to_fasta_file = os.path.abspath()

model.execute(path_to_rnafold, path_to_fasta_file)
prediction = model.get_ss_prediction()
```

Note that running the model's `execute` method sets its `output` value. The RNAFold tool outputs multiple lines, so the `get_ss_prediction` method is designed to extract just the dot-bracket notation of the secondary structure prediction from that output. So, if you run the above code, the `prediction` variable will be a string in dot-bracket notation of the RNAFold tool's secondary structure prediction for the RNA sequence in `rna1.fasta`. If you want to view the full output of the RNAFold tool, you can retrieve that with `model.output` after running the `execute` method.

## How to Add a New Prediction Algorithm

The RNAFoldAssess tool is designed to compare the performance of many secondary structure prediction algorithms. As such, you will likely want to add support for additional prediction algorithms besides just RNAFold and ContraFold. This section will describe how to do that.

### Install the Tool

Please note that before writing any code, you have to install the tool that you're planning to use. For our examples, we will be writing support for the [MXFold](https://github.com/mxfold/mxfold) predictor in the RNAFoldAssess framework.

### Add the Class

Once you've followed the installation instructions for the predictor you're adding to RNAFoldAssess, the next thing to do is add a new Python file to the `models/predictors` directory. Since the example we're creating is for MXFold, we will add the file `RNAFoldAssess/models/predictors/mxfold.py`.

Note that predictor classes should have an `output` attribute, and `__init__`, `execute` and `get_ss_prediction` methods. The `__init__` method is to instantiate an object of the predictor you're adding and should at least set the `output` attribute to an empty string. We'll talk about the other methods in the coming sections. For now, our example class for MXFold will look like this:

```python
class MXFold:
    def __init__(self):
        self.output = ""

    def execute(self):
        pass

    def get_ss_prediction(self):
        pass
```

### Configure the Execution

Almost every prediction tool has a command line string that will execute the tool and output a secondary structure prediction. We will configure that string in the `execute` method. The `execute` method will take at least two arguments: a path to the tool's executable, and an RNA input. Different predictors can handle different outputs; some require a fasta file, some a seq file, and other can take a raw string. You will have to figure this out for the tool you are writing.

Since we are using the MXFold tool as an example, let's see how the MXFold tool is used. According to its documentation, the way of executing the MXFold tool is like so:

```sh
$> /path/to/mxfold/build/mxfold path/to/input_rna.fasta
```

From this we can tell that we will need a path to a fasta file, and the MXFold executable path. So we'll rewrite the `execute` method to use the `popen` method from the Python `os` module and set the output to the model's output:

```python
import os

class MXFold:
    def __init__(self):
        self.output = ""

    def execute(self, path, fasta_file):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()

    def get_ss_prediction(self):
        pass
```

Sometimes, you may only want the fasta file to exist for the purposes of generating a secondary structure prediction. As such, you may want to include the argument `remove_file_when_done`. This isn't necessary, but could be useful sometimes. Our class now looks like this:

```python
import os

class MXFold:
    def __init__(self):
        self.output = ""

    def execute(self, path, fasta_file, remove_file_when_done=False):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            try:
                os.remove(fasta_file)
            except FileNotFoundError:
                print(f"MXFold: Couldn't find {fasta_file} to delete")

    def get_ss_prediction(self):
        pass
```

This is likely useful if you're using objects of the RNAFoldAssess `DataPoint` model which can generate fasta and seq files. If you are working with those data points in memory, deleting the fasta (or seq or other) files after generating a prediction might be a good idea so you don't unexpectedly use up a lot of disk space.

### Parse out the Secondary Structure Prediction

As mentioned before, each tool will have different outputs. If you used the `os` module's `popen` method like the example above, the tool's output is piped into the `MXFold`'s `output` attribute. The output of the tool you're adding likely has more information than you need, especially if all you want is the predicted secondary structure. This is where the `get_ss_prediction` method comes in. In this method, you will write the code to parse out the secondary structure from the tool's output, or raise an exception if there is no output. Let's continue with our MXFold example.

When the MXFold tool is run on the command line, it produces output like this:

```
> DS4440
GGAUGGAUGUCUGAGCGGUUGAAAGAGUCGGUCUUGAAAACCGAAGUAUUGAUAGGAAUACCGGGGGUUCGAAUCCCUCUCCAUCCG
>structure
(((((((........(((((..(((.......)))...)))))..(((((......))))).(((((.......)))))))))))).
```

This is what is piped to the `MXFold` object's `output` attribute, so to get the secondary structure, we should split the `output` on the newline character and get the last item. Consider the new code in `get_ss_prediction` of our `MXFold` class:

```python
import os

class MXFold:
    def __init__(self):
        self.output = ""

    def execute(self, path, fasta_file, remove_file_when_done=False):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            try:
                os.remove(fasta_file)
            except FileNotFoundError:
                print(f"MXFold: Couldn't find {fasta_file} to delete")

    def get_ss_prediction(self):
        strings = self.output.split("\n")
        prediction = strings[3]
        return prediction
```

The `get_ss_prediction` method splits the output from the MXFold tool (which was saved to the `output` attribute) and splits it into a list of four items. The last item is the secondary structure prediction, so that's what the model returns.

Sometimes, we configure something wrong such as sending an incorrect path or messing up the execution string somehow. In this case, the error from the tool is usually piped to STDERR and thus the `read` method chained to the `popen` method will not return anything. In this case, the object's `output` attribute will still be an emptry string. If we run the above code an empty string, it will throw an error. In a lot of cases, it's best to handle this possibility with a `try`/`except` block in the `get_ss_prediction` method. Check out the final rewrite of our class:

```python
import os

class MXFold:
    def __init__(self):
        self.output = ""

    def execute(self, path, fasta_file, remove_file_when_done=False):
        path_to_mx_fold = os.path.abspath(path)
        exec_string = f"{path} {fasta_file}"
        self.output = os.popen(exec_string).read()
        if remove_file_when_done:
            try:
                os.remove(fasta_file)
            except FileNotFoundError:
                print(f"MXFold: Couldn't find {fasta_file} to delete")

    def get_ss_prediction(self):
        if self.output == "":
            raise Exception(f"MXFold exception: no output generated")
        strings = self.output.split("\n")
        prediction = strings[3]
        return prediction
```

This way, if you're running an anlysis pipeline on thousands of files, you can gracefully handle exceptions without stopping the whole pipeline.

## How to Add a New Scoring Method

## How to Create an Analysis Pipeline

# Example Use Cases

Please consider the following use cases:

## Example Use-Case - Which prediction algorithm is best for my current work?

There are several RNA secondary structure prediction algorithms available to researchers. All of them have different means of accomplishing the task of predicitng secondary structure; some require fasta files as inputs, some require sequence files as inputs, others can take raw strings from the command line.

## Example Use-Case - How does this prediction algorithm perform on a certain kind of data?

## Example Use-Case - I created a new prediction algorithm, how does it compare to existing tools?


### Scorer

In this module, we put different scoring algorithms. For example, the DSCI scorer--which uses the Mann-Whitney U-test--is encapsulated in the `DSCI` class. All classes in this module must inherit the base `Scorer` class and override the `evaluate method`. Note that the `Scorer` class is instantiated with a `DataPoint` object, algorithm name (e.g., EternaFold), and an optional parameter called `evaluate_immediately`. The `evaluate_immediately` parameter defaults to `True` and is used to indicate if the user wants the secondary structure prediction to be scored as soon as the `Scorer` object is instantiated. In other words, when `evaluate_immediately` is `True`, the `evaluate` method will be called at the end of the `__init__` method. If not, the user will have to manually call the `evaluate` method on the `Scorer` object.

### `predictors`

This file contains classes that encapsulate different ways in which the algorithms must be executed and evaluated. For example, the `Eterna` class calls the prediction method for EternaFold on a given sequence file. Conversely, the `SPOT_RNA` class executes the prediction algoirthm, but also converts the output `.ct` files into a secondary structure dot-brakcet string so the predictions can be evaluated.

## `script.py`

This file simply exists to test and show examples of how to use the `executions` models and evaluations.

## TODO

This project has a long way to go. Currently, some of the work remains to standardize inputs and make it painfully obvious how users can add new tools.
