import pandas as pd

df = pd.read_csv('data_with_inferred_cpus.csv')

# Check specific_cpus (non-generic)
specific = df[~df['mapped_cpu_name'].str.startswith('Generic', na=False)]

# Check i3 + gen 11
i3_11 = specific[(specific['cpu_tier'] == 'i3') & (specific['cpu_generation'] == 11.0)]
print(f"i3 + gen 11.0: {len(i3_11)} rows")

# Check what CPUs
if len(i3_11) > 0:
    cpu_counts = i3_11['mapped_cpu_name'].value_counts()
    print(f"Most common: {cpu_counts.index[0]} ({cpu_counts.iloc[0]} rows)")
    print(f"Confidence: {cpu_counts.iloc[0] / len(i3_11):.1%}")

# Check if this meets Level 4 threshold (>=3 rows, >=2 count or >=25% confidence)
if len(i3_11) >= 3:
    print("✓ Meets Level 4 group size threshold (>=3 rows)")
    if cpu_counts.iloc[0] >= 2:
        print("✓ Meets Level 4 count threshold (>=2)")
    if (cpu_counts.iloc[0] / len(i3_11)) >= 0.25:
        print("✓ Meets Level 4 confidence threshold (>=25%)")
