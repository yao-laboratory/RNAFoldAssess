with open("align_human_chr1.slurm") as fh:
    template = fh.read()


chromosomes = [f"chr{i}" for i in range(2, 23)] + ["chrX", "chrY"]

for chromosome in chromosomes:
    num = chromosome.replace("chr", "")
    fstring = template.replace("h1", f"h{num}")
    fstring = fstring.replace("chr1", chromosome)
    with open(f"align_human_chr{num}.slurm", "w") as fh:
        fh.write(fstring)

