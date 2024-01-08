import os

from RNAFoldAssess.models import DataPointFromCrystal
from RNAFoldAssess.models.predictors import *
from RNAFoldAssess.utils import *

rna_data_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/rna_only/preprocessed/twenty_plus"
pro_data_dir = "/common/yesselmanlab/ewhiting/data/crystal2/secondary_structures/with_protein/preprocessed/twenty_plus"

rna_fasta_dir = "/common/yesselmanlab/ewhiting/data/crystal2/fasta_files/rna_only"
pro_fasta_dir = "/common/yesselmanlab/ewhiting/data/crystal2/fasta_files/with_protein"

model_name = "EternaFold"
model = Eterna()
model_path = os.path.abspath("/home/yesselmanlab/ewhiting/EternaFold")
data_type_name = "crystal2"

crystal_evals(
    model=model,
    model_name=model_name,
    model_path=model_path,
    dbn_path=rna_data_dir,
    data_type_name=data_type_name,
    fasta_file_location=rna_fasta_dir,
    crystal2_dataset=True,
    rna_only=True,
    testing=False
)

crystal_evals(
    model=model,
    model_name=model_name,
    model_path=model_path,
    dbn_path=pro_data_dir,
    data_type_name=data_type_name,
    fasta_file_location=pro_fasta_dir,
    crystal2_dataset=True,
    with_protein=True,
    testing=False
)
