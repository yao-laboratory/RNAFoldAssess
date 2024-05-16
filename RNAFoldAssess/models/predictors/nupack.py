import os

import nupack


class NUPACK:
    def __init__(self):
        self.output = ""
        self.model = nupack.Model(material="RNA")

    def execute(self, sequence):
        mfe_ss = nupack.mfe(strands=[sequence], model=self.model)
        self.output = mfe_ss[0]

    def get_ss_prediction(self):
        return str(self.output.structure)

    def get_mfe(self):
        return self.output.energy

