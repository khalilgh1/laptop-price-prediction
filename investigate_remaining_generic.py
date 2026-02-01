import pandas as pd

# Load the final data
df = pd.read_csv('data_preprocesseds.csv')

# Find the remaining Generic CPUs with generation
remaining_with_gen = df[
    (df['mapped_cpu_name'].str.startswith('Generic', na=False)) &
    (df['cpu_generation'].notna())
]

print(f"Found {len(remaining_with_gen)} Generic CPUs WITH generation that weren't inferred")
print(f"\n{'='*80}")
print("INVESTIGATING WHY THESE WEREN'T INFERRED")
print(f"{'='*80}")

# Group by mapped_cpu_name to see patterns
grouped = remaining_with_gen.groupby('mapped_cpu_name')

for cpu_name, grp in grouped:
    count = len(grp)
    print(f"\n{cpu_name}: {count} rows")
    
    # Show first few examples with details
    sample = grp[['CPU', 'cpu_tier', 'cpu_generation', 'model_name', 'gpu_name']].head(3)
    print(sample.to_string(index=False))
    
    # Check if these combinations exist in specific CPU data
    specific_cpus = df[~df['mapped_cpu_name'].str.startswith('Generic', na=False)]
    
    # Check one example
    example = grp.iloc[0]
    tier = example['cpu_tier']
    gen = example['cpu_generation']
    model = example['model_name']
    gpu = example['gpu_name']
    
    # Look for matches with same tier+gen
    if pd.notna(tier) and pd.notna(gen):
        matches_tier_gen = specific_cpus[
            (specific_cpus['cpu_tier'] == tier) &
            (specific_cpus['cpu_generation'] == gen)
        ]
        print(f"  → {len(matches_tier_gen)} specific CPUs with tier={tier} + gen={gen}")
        
        # Look for matches with same model+tier+gen
        if pd.notna(model):
            matches_model = matches_tier_gen[matches_tier_gen['model_name'] == model]
            print(f"  → {len(matches_model)} with model={model}")
            if len(matches_model) > 0:
                cpu_counts = matches_model['mapped_cpu_name'].value_counts().head(3)
                print(f"     Most common CPUs:")
                for cpu, c in cpu_counts.items():
                    print(f"       - {cpu} ({c}x)")
        
        # Look for matches with same GPU+tier+gen
        if pd.notna(gpu):
            matches_gpu = matches_tier_gen[matches_tier_gen['gpu_name'] == gpu]
            print(f"  → {len(matches_gpu)} with gpu={gpu}")
            if len(matches_gpu) > 0:
                cpu_counts = matches_gpu['mapped_cpu_name'].value_counts().head(3)
                print(f"     Most common CPUs:")
                for cpu, c in cpu_counts.items():
                    print(f"       - {cpu} ({c}x)")

print(f"\n{'='*80}")
print("CONCLUSION")
print(f"{'='*80}")
print("\nThese should be inferred if:")
print("1. The specific CPU data has matching tier+gen combinations")
print("2. The inference map building has sufficient data (>=2 rows for Level 2, >=3 for Level 3, >=5 for Level 4)")
print("3. The confidence threshold is met")
