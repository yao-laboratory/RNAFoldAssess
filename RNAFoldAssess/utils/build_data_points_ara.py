import os


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


def assemble_coords2(reads):
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
    return contiguous_by_chromosome


def get_sequences(fasta_file_loc):
    f = open(fasta_file_loc)
    fcontents = f.read()
    f.close()
    chunks = fcontents.split(">")
    # Remove blank line
    chunks.pop(0)
    chrom_seq = {}
    for c in chunks:
        split = c.split("\n")
        chromosome_annotation = split.pop(0).split()[0]
        # Remove newline characters
        sequence = [s.strip() for s in split]
        chrom_seq[chromosome_annotation] = "".join(sequence)
    return chrom_seq



def merge_data(sequences, coords):
    keys = list(coords.keys())
    readings = {}
    for k in keys:
        chrom_sequence = sequences[k]
        index = 0
        readings[k] = []
        for item in coords[k]:
            coordinates, dms, signs = item
            dms = [float(d) for d in dms]
            sequence = [chrom_sequence[c] for c in coordinates]
            sequence = "".join(sequence).replace("T", "U")
            sign_str = "".join(signs)
            reading = {
                "name": f"chromosome_{k}_number_{index}",
                "coordinates": coordinates,
                "sequence": sequence,
                "dms": dms,
                "sign": sign_str
            }
            readings[k].append(reading)
            index += 1
    return readings


def filter_out_one_len_readings(readings):
    new_readings = {}
    for chromosome, data in readings.items():
        new_readings[chromosome] = []
        for d in data:
            coords = d["coordinates"]
            if len(coords) == 1:
                continue
            else:
                new_readings[chromosome].append(d)
    return new_readings


def analyze_readings(readings):
    keys = list(readings.keys())
    bad_matches = []
    for k in keys:
        items = readings[k]
        for item in items:
            num_of_dms_reads = len(item["dms"])
            if num_of_dms_reads > 1:
                sign_str = item["sign"]
                if len(set(sign_str)) != 1:
                    bad_matches.append(item)
    return bad_matches


def check_signs(readings):
    bad_readings = []
    for c, data in readings.items():
        for d in data:
            if d["sign"][0] not in "+-":
                bad_readings.append(d)
    return bad_readings


from Bio.Seq import Seq
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





import json
bed_file_loc = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/Structure-seq_TAIR10_Nature_2014_DMS_invivo_both_score_TAIR10_score_FIRST.bed"
fasta_file = "/common/yesselmanlab/ewhiting/data/rasp_data/ara-tha/TAIR10.fa"
species = "arabidopsis"

reads = preprocess_dms_data(bed_file_loc)
coords = assemble_coords2(reads)
sequences = get_sequences(fasta_file)
readings = merge_data(sequences, coords)
readings = filter_out_one_len_readings(readings)
# check = check_signs(readings)
readings = translate_negative_readings(readings)

def to_datapoint_json(readings, species):
    for k in readings:
        data = []
        for item in readings[k]:
            dp = {
                "name": item["name"],
                "sequence": item["sequence"],
                "data": item["dms"],
                "reads": 0,
                "coordinates": item["coordinates"]
            }
            data.append(dp)

        file_name = f"processed/arabidopsis/round2/rasp_{species}_chromosome_{k}.json"
        with open(file_name, "w") as outfile:
            json.dump(data, outfile)


to_datapoint_json(readings, species)

# Check reactivity
chs = list(readings.keys())
for c in chs:
    ch = readings[c]
    all_readings = 0
    ac_pos_readings = 0
    ug_pos_readings = 0
    for reading in ch:
        seq = reading["sequence"]
        dms = reading["dms"]
        for i, read in enumerate(dms):
            if read > 0:
                all_readings += 1
                if seq[i] in ["A", "C"]:
                    ac_pos_readings += 1
                if seq[i] in ["U", "G"]:
                    ug_pos_readings += 1
    ac_rate = round((ac_pos_readings / all_readings) * 100, 2)
    ug_rate = round((ug_pos_readings / all_readings) * 100, 2)
    print(f"For {c}:")
    print(f"\tPositive A/C readings: {ac_pos_readings}")
    print(f"\tPositive U/G readings: {ug_pos_readings}")
    print(f"\tA/C were {ac_rate}% of positive readings")
    print(f"\tU/G were {ug_rate}% of positive readings")
