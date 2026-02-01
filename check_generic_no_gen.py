import pandas as pd

# Load the data with inferred CPUs
df = pd.read_csv('data_with_inferred_cpus.csv')

# Find generic CPUs (mapped_cpu_name starts with "Generic")
generic_cpus = df[df['mapped_cpu_name'].str.startswith('Generic', na=False)].copy()

print(f"Total generic CPUs: {len(generic_cpus)}")

# Check which have cpu_generation
generic_with_gen = generic_cpus[generic_cpus['cpu_generation'].notna()]
generic_no_gen = generic_cpus[generic_cpus['cpu_generation'].isna()]

print(f"Generic CPUs WITH generation: {len(generic_with_gen)}")
print(f"Generic CPUs WITHOUT generation: {len(generic_no_gen)}")

# Among those WITHOUT generation, find ones that have both model_name and gpu_name
generic_no_gen_with_info = generic_no_gen[
    (generic_no_gen['model_name'].notna()) & 
    (generic_no_gen['gpu_name'].notna())
]

print(f"\n{'='*80}")
print(f"Generic CPUs (NO generation) but WITH model + GPU: {len(generic_no_gen_with_info)}")
print(f"{'='*80}")

if len(generic_no_gen_with_info) > 0:
    # Show sample
    display_cols = ['CPU', 'mapped_cpu_name', 'cpu_tier', 'cpu_generation', 'model_name', 'gpu_name']
    print("\nSample rows (first 30):")
    print(generic_no_gen_with_info[display_cols].head(30).to_string(index=False))
    
    # Group by tier to see distribution
    print(f"\n{'='*80}")
    print("Distribution by tier:")
    print(f"{'='*80}")
    tier_counts = generic_no_gen_with_info['cpu_tier'].value_counts()
    for tier, count in tier_counts.items():
        print(f"  {tier}: {count} CPUs")
    
    # Check if these model+GPU combinations exist in specific CPU data
    print(f"\n{'='*80}")
    print("Checking if these combinations exist in specific CPU data...")
    print(f"{'='*80}")
    
    specific_cpus = df[~df['mapped_cpu_name'].str.startswith('Generic', na=False)]
    
    # Check first 10 generic CPUs
    found_count = 0
    not_found_count = 0
    
    for idx, row in generic_no_gen_with_info.head(10).iterrows():
        model = row['model_name']
        gpu = row['gpu_name']
        tier = row['cpu_tier']
        
        # Look for this model+GPU combination in specific CPUs
        matches = specific_cpus[
            (specific_cpus['model_name'] == model) & 
            (specific_cpus['gpu_name'] == gpu)
        ]
        
        if len(matches) > 0:
            # Get the CPUs used for this combo
            cpu_names = matches['mapped_cpu_name'].value_counts().head(3)
            print(f"\n✓ FOUND: {model} + {gpu} (tier={tier})")
            print(f"  Used in {len(matches)} specific rows with CPUs:")
            for cpu_name, count in cpu_names.items():
                print(f"    - {cpu_name} ({count}x)")
            found_count += 1
        else:
            print(f"\n✗ NOT FOUND: {model} + {gpu} (tier={tier})")
            not_found_count += 1
    
    print(f"\n{'='*80}")
    print(f"Summary (first 10 checked): {found_count} found, {not_found_count} not found")
    print(f"{'='*80}")

print("\nDone!")
