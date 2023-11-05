BASE_DATA_PATH=/common/yesselmanlab/ewhiting/data/dp_fasta
DESTINATION_BASE=/common/yesselmanlab/ewhiting/data/spot_rna_ct_files
SPOT_RNA_PATH=/home/yesselmanlab/ewhiting/SPOT-RNA/SPOT-RNA.py

for dir in $(ls $BASE_DATA_PATH); do
    for f in $(ls $BASE_DATA_PATH/$dir); do
        FASTA_FILE=$BASE_DATA_PATH/$dir/$f
        EXEC_STR="python3 $SPOT_RNA_PATH --inputs $FASTA_FILE --outputs $DESTINATION_BASE"
        conda run -n spot $EXEC_STR
	rm $DESTINATION_BASE/*.prob
	rm $DESTINATION_BASE/*.bpseq
    done
done
