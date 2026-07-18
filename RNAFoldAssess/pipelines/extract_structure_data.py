import csv
import statistics
from itertools import combinations

from RNAFoldAssess.utils.secondary_structure_tools import (
    SecondaryStructureTools as sst,
)


prediction_columns = [
    "ContextFold_prediction",
    "ContraFold_prediction",
    "EternaFold_prediction",
    "RNAFold_prediction",
    "RNAStructure_prediction",
    "pKnots_prediction",
    "IPKnot_prediction",
    "Simfold_prediction",
    "NUPACK_prediction",
    "NeuralFold_prediction",
    "MXFold_prediction",
    "MXFold2_prediction",
    "SPOT-RNA_prediction",
]


def average_hamming_distance(strings: list[str]) -> float:
    distances = [
        sum(char_a != char_b for char_a, char_b in zip(string_a, string_b))
        for string_a, string_b in combinations(strings, 2)
    ]

    return sum(distances) / len(distances)


def median_or_zero(values) -> float:
    return statistics.median(values) if values else 0


def get_motif_size(motif: str) -> int:
    seq = motif.split("_")[1].replace("&", "")
    return len(seq)


def new_features(input_csv: str, output_csv: str) -> None:
    with open(input_csv, newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)

    headers = rows.pop(0)

    prediction_indexes = [
        headers.index(prediction_column)
        for prediction_column in prediction_columns
    ]

    for row in rows:
        sequence = row[1]

        motifs = []
        predictions = []
        gu_pair_counts = []
        basepairs_predicted = []

        helix_counts = []
        hairpin_counts = []
        loop_counts = []
        mway_counts = []

        for prediction_index in prediction_indexes:
            structure = row[prediction_index]
            predictions.append(structure)

            structure_motifs = list(
                sst.get_structural_motif_data(
                    sequence,
                    structure,
                ).keys()
            )

            motifs.extend(structure_motifs)

            helix_counts.append(
                sum(
                    motif.startswith("HELIX")
                    for motif in structure_motifs
                )
            )
            hairpin_counts.append(
                sum(
                    motif.startswith("HAIRPIN")
                    for motif in structure_motifs
                )
            )
            loop_counts.append(
                sum(
                    motif.startswith("LOOP")
                    for motif in structure_motifs
                )
            )
            mway_counts.append(
                sum(
                    motif.startswith("MWAY")
                    for motif in structure_motifs
                )
            )

            # Add len(...) here if get_gu_pairs returns a collection.
            gu_pair_counts.append(
                sst.get_gu_pairs(sequence, structure)
            )

            basepairs_predicted.append(
                len(sst.get_pairings(sequence, structure))
            )

        helices = [
            motif
            for motif in motifs
            if motif.startswith("HELIX")
        ]

        hairpins = [
            motif
            for motif in motifs
            if motif.startswith("HAIRPIN")
        ]

        median_helix_count = statistics.median(helix_counts)
        median_hairpin_count = statistics.median(hairpin_counts)
        median_loop_count = statistics.median(loop_counts)
        median_mway_count = statistics.median(mway_counts)

        median_gu_pairs = statistics.median(gu_pair_counts)
        median_basepairs = statistics.median(basepairs_predicted)

        five_prime_sizes = [
            get_motif_size(motif)
            for motif in motifs
            if motif.startswith("5PER")
        ]

        three_prime_sizes = [
            get_motif_size(motif)
            for motif in motifs
            if motif.startswith("3PER")
        ]

        helix_sizes = [
            get_motif_size(helix)
            for helix in helices
        ]

        median_5prime_size = median_or_zero(five_prime_sizes)
        median_3prime_size = median_or_zero(three_prime_sizes)
        median_helix_size = median_or_zero(helix_sizes)
        longest_helix = max(helix_sizes, default=0)

        prediction_hamming_distance = average_hamming_distance(
            predictions
        )

        au_helix_pairs = [
            sst.get_au_helix_end_pairs(helix)
            for helix in helices
        ]

        median_au_helix_pairs = median_or_zero(au_helix_pairs)

        reverse_complementary_helix_count = sum(
            sst.helix_is_self_complementary_duplex(helix)
            for helix in helices
        )

        hairpins_with_gt4_unpaired_nts = sum(
            sst.search_unpaired_nts_in_hairpin(hairpin)
            for hairpin in hairpins
        )

        row.extend([
            median_helix_count,
            median_hairpin_count,
            median_loop_count,
            median_mway_count,
            median_gu_pairs,
            median_basepairs,
            median_5prime_size,
            median_3prime_size,
            median_helix_size,
            longest_helix,
            prediction_hamming_distance,
            median_au_helix_pairs,
            reverse_complementary_helix_count,
            hairpins_with_gt4_unpaired_nts,
        ])

    headers.extend([
        "median_helix_count",
        "median_hairpin_count",
        "median_loop_count",
        "median_mway_count",
        "median_gu_pairs",
        "median_basepairs_predicted",
        "median_5prime_size",
        "median_3prime_size",
        "median_helix_size",
        "longest_helix_predicted",
        "avg_hamming_distance_of_predictions",
        "median_au_helix_pairs",
        "count_of_reverse_complementary_helices",
        "hairpins_with_gt4_unpaired_nts",
    ])

    with open(output_csv, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)