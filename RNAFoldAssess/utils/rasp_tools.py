from Bio.Seq import Seq


class RASPTools:
    @staticmethod
    def make_location_file(path, species, dest="."):
        with open(path) as f:
            data = f.readlines()
        data = [d.split("\t") for d in data]
        data = [d for d in data if "gene" in d[2].lower()]
        counter = 0
        names = []
        gene_locs = []
        for d in data:
            start = d[3]
            end = d[4]
            name = d[8].split(";")[0].split("ID=")[1]
            if name in names:
                counter += 1
                name = f"{name}_{counter}"
            else:
                counter = 0
                names.append(name)
            gene_locs.append((name, start, end))
        fstring = ""
        for gl in gene_locs:
            fstring += f"{gl[0]} {gl[1]} {gl[2]}\n"
        with open(f"{dest}/{species}_loc.txt", "w") as f:
            f.write(fstring)


    @staticmethod
    def make_dms_location_file(path, species, dest="."):
        with open(path) as p:
            bed_data = [d.strip().split() for d in p.readlines()]
        loc_dms = []
        fstring = ""
        for bd in bed_data:
            start = int(bd[1])
            end = int(bd[2])
            dms = bd[4]
            sign = bd[5]
            rep_string = ""
            for pos in range(start, end):
                rep_string += f"{pos} {dms} {sign}\n"
            fstring += rep_string
        with open(f"{dest}/{species}_dms_locations.txt", "w") as f:
            f.write(fstring)


    @staticmethod
    def process_data(locs_path, bed_path, fasta_path, sepcies):
        with open(locs_path) as lp:
            loc_data = [d.strip().split(" ") for d in lp.readlines()]

        # with open(dms_path) as bp:
        #     dms_data = [d.strip().split() for d in bp.readlines()]

        # with open(fasta_path) as fp:
        #     fasta_data = [d.strip() for d in fp.readlines()]

        print("Assembling DMS coordinates")
        reads = RASPTools.preprocess_dms_data(bed_path)
        coords = RASPTools.assemble_coords(reads)
        print("Finished assembling DMS coordinates")

        print("Assembling sequence ranges")
        range_data = {}
        for name, start, end in loc_data:
            range_data[name] = {"ranges": [], "dms_data": []}
            for i in range(int(start), int(end)):
                range_data[name]["ranges"].append(i)
        print("Finished assembling sequence ranges")

        print("Unifying coordinate and DMS data")
        len_coords = len(coords)
        counter = 0
        for cd in coords:
            counter += 1
            if counter % 200 == 0:
                print(f"Working {counter} of {len_coords}")
                fstring = ""
                for k in range_data:
                    d = range_data[k]
                    fstring += f"{k} --> Locations: {d['ranges'][:10]} ... DMS: {d['dms_data']}\n"
                f = open("interim_data.txt", "w")
                f.write(fstring)
                f.close()
                break
            coordinates = set(cd[0])
            for k in range_data:
                if coordinates <= set(range_data[k]["ranges"]):
                    range_data[k]["dms_data"] = cd
                    break

        print("Finished unifying coordinates and DMS data")
        return range_data



    @staticmethod
    def translate_negative_readings(readings):
        new_readings = {}
        for chromosome, data in readings.items():
            new_readings[chromosome] = []
            for d in data:
                sign = d["sign"][0]
                if sign == "+":
                    new_readings[chromosome].append(d)
                else:
                    seq = Seq(d["sequence"])
                    dms = d["dms"]
                    reverse_complement = str(seq.reverse_complement_rna())
                    reverse_dms = dms[::-1]
                    d["sequence"] = reverse_complement
                    d["dms"] = reverse_dms
                    new_readings[chromosome].append(d)
        return new_readings


    def preprocess_dms_data(bed_file_loc):
        f = open(bed_file_loc)
        data = f.readlines()
        f.close()
        reads_by_chrom = {}
        data = [d.split() for d in data]
        for d in data:
            chrom, start, end, _1, dms, sign = d
            current_keys = list(reads_by_chrom.keys())
            if chrom not in current_keys:
                reads_by_chrom[chrom] = {}
            for i in range(int(start), int(end)):
                reads_by_chrom[chrom][i] = {"chromosome": chrom, "dms": dms, "sign": sign, "start": start, "end": end}
        return reads_by_chrom


    def assemble_coords(reads):
        chromosomes = list(reads.keys())
        contiguous_by_chromosome = {}
        # Sort the data
        for c in chromosomes:
            data = reads[c]
            positions = list(data.keys())
            positions.sort()
            contiguous_by_chromosome[c] = []
            for i, pos in enumerate(positions):
                sign = reads[c][pos]["sign"]
                if len(contiguous_by_chromosome[c]) > 0 and pos in contiguous_by_chromosome[c][-1][0]:
                    continue
                else:
                    counter = i + 1
                    if counter == len(positions):
                        break
                    segment = [pos]
                    offset = 1
                    while abs(positions[counter] - pos) == offset:
                        segment.append(positions[counter])
                        counter += 1
                        if counter == len(positions):
                            break
                        offset += 1
                    dms = []
                    signs = []
                    for s in segment:
                        dms.append(reads[c][s]["dms"])
                        signs.append(reads[c][s]["sign"])
                    contiguous_by_chromosome[c].append((segment, dms, signs))
        list_out = []
        for k in contiguous_by_chromosome:
            list_out += contiguous_by_chromosome[k]
        return list_out
