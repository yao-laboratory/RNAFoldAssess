import os
import pandas as pd


base_dir = "/common/yesselmanlab/ewhiting/reports/ydata/analyses"
gg_path = f"{base_dir}/consistently_good_datapoints.txt"
bg_path = f"{base_dir}/consistently_bad_datapoints.txt"

gf = open(gg_path)
ggs = gf.readlines()
gf.close()
bf = open(bg_path)
bgs = bf.readlines()
bf.close()

g_lens = []
b_lens = []

g_gc = []
b_gc = []

for g in ggs:
    seq_len = len(g.split(", ")[1])
    g_content = g.upper().count("G")
    c_content = g.upper().count("C")
    gcs = float(g_content + c_content)
    gc_content = gcs / float(seq_len)
    g_gc.append(gc_content)
    g_lens.append(seq_len)

for g in bgs:
    seq_len = len(g.split(", ")[1])
    g_content = g.upper().count("G")
    c_content = g.upper().count("C")
    gcs = float(g_content + c_content)
    gc_content = gcs / float(seq_len)
    b_gc.append(gc_content)
    b_lens.append(seq_len)

s1 = pd.Series(g_lens)
g_std = s1.std()
g_mean = s1.median()
s2 = pd.Series(b_lens)
b_std = s2.std()
b_mean = s1.median()

print("Lenghts of good predictions:")
print(s1.describe())
print()
print("Lenghts of bad predictions:")
print(s2.describe())

g_outliers = 0
b_outliers = 0

g_hi, g_lo = ((3 * g_std) + g_mean, (3 * g_std) - g_mean)
for g in g_lens:
    if g > g_hi or g < g_lo:
        g_outliers += 1

b_hi, b_lo = ((3 * b_std) + b_mean, (3 * b_std) - b_mean)
for g in g_lens:
    if g > g_hi or g < g_lo:
        g_outliers += 1


print()
print(f"Number of lenght outliers in good predictions: {g_outliers}")
print(f"Number of lenght outliers in bad predictions: {b_outliers}")

s3 = pd.Series(g_gc)
s3_std = s3.std()
s3_mean = s3.median()
s4 = pd.Series(b_gc)
s4_std = s4.std()
s4_mean = s4.median()

print()
print("GC of good predictions:")
print(s3.describe())
print()
print("Lenghts of bad predictions:")
print(s4.describe())

g_outliers = 0
b_outliers = 0

g_hi, g_lo = ((3 * s3_std) + s3_mean, (3 * s3_std) - s3_mean)
for g in g_gc:
    if g > g_hi or g < g_lo:
        g_outliers += 1

b_hi, b_lo = ((3 * s4_std) + s4_mean, (3 * s4_std) - s4_mean)
for g in b_gc:
    if g > g_hi or g < g_lo:
        g_outliers += 1

print()
print()
print(f"Number of GC content outliers in good predictions: {g_outliers}")
print(f"Number of GC content outliers in bad predictions: {b_outliers}")
