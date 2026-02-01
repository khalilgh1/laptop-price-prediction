import pandas as pd

# Load both files
df_with_cpus_gpus = pd.read_csv('data_with_cpus_gpus.csv')
df_preprocessed = pd.read_csv('data_preprocesseds.csv')

print("="*80)
print("COMPARING UNIQUE CPU NAMES")
print("="*80)

# Get unique CPU names from both files
cpus_original = set(df_with_cpus_gpus['mapped_cpu_name'].dropna().unique())
cpus_final = set(df_preprocessed['mapped_cpu_name'].dropna().unique())

print(f"\ndata_with_cpus_gpus.csv: {len(cpus_original)} unique CPUs")
print(f"data_preprocesseds.csv: {len(cpus_final)} unique CPUs")

# Find differences
cpus_lost = cpus_original - cpus_final
cpus_added = cpus_final - cpus_original

print(f"\n{'='*80}")
print(f"CPUS LOST (were in original, not in final): {len(cpus_lost)}")
print(f"{'='*80}")

if len(cpus_lost) > 0:
    print("\nCPUs that disappeared:")
    for cpu in sorted(list(cpus_lost))[:30]:
        # Check how many rows had this CPU
        count = len(df_with_cpus_gpus[df_with_cpus_gpus['mapped_cpu_name'] == cpu])
        print(f"  - {cpu} ({count} rows)")
    
    if len(cpus_lost) > 30:
        print(f"  ... and {len(cpus_lost) - 30} more")

print(f"\n{'='*80}")
print(f"CPUS ADDED (not in original, now in final): {len(cpus_added)}")
print(f"{'='*80}")

if len(cpus_added) > 0:
    print("\nNew CPUs added:")
    for cpu in sorted(list(cpus_added))[:30]:
        # Check how many rows have this CPU
        count = len(df_preprocessed[df_preprocessed['mapped_cpu_name'] == cpu])
        # Check if they have inference_level
        if 'inference_level' in df_preprocessed.columns:
            inferred = df_preprocessed[df_preprocessed['mapped_cpu_name'] == cpu]
            levels = inferred['inference_level'].value_counts()
            level_str = ", ".join([f"L{int(l)}: {c}" for l, c in levels.items() if pd.notna(l)])
            print(f"  + {cpu} ({count} rows) [{level_str}]")
        else:
            print(f"  + {cpu} ({count} rows)")
    
    if len(cpus_added) > 30:
        print(f"  ... and {len(cpus_added) - 30} more")

# Check Generic CPUs separately
print(f"\n{'='*80}")
print(f"GENERIC CPUs BREAKDOWN")
print(f"{'='*80}")

generic_original = df_with_cpus_gpus[df_with_cpus_gpus['mapped_cpu_name'].str.startswith('Generic', na=False)]
generic_final = df_preprocessed[df_preprocessed['mapped_cpu_name'].str.startswith('Generic', na=False)]

print(f"\nOriginal file: {len(generic_original)} rows with Generic CPUs")
print(f"Final file: {len(generic_final)} rows with Generic CPUs")
print(f"Reduction: {len(generic_original) - len(generic_final)} rows converted to specific CPUs")

# Show which Generic CPUs remain
print(f"\nGeneric CPUs remaining in final file:")
generic_counts_final = generic_final['mapped_cpu_name'].value_counts()
for cpu_name, count in generic_counts_final.head(20).items():
    print(f"  - {cpu_name}: {count} rows")

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
print(f"Total unique CPUs lost: {len(cpus_lost)}")
print(f"Total unique CPUs added: {len(cpus_added)}")
print(f"Net change: {len(cpus_final) - len(cpus_original):+d} unique CPUs")
print(f"Generic rows reduced: {len(generic_original) - len(generic_final)}")
