import pandas as pd

df = pd.read_csv('data_preprocesseds.csv')

# Find the i7→i5 mismatches
mismatches = df[(df['CPU'].str.contains('CORE I7', case=False, na=False)) & 
                 (df['mapped_cpu_name'].str.contains('i5', case=False, na=False))]

print(f'Found {len(mismatches)} i7→i5 mismatches')
print('\nDetails:')
for idx, row in mismatches[['CPU', 'mapped_cpu_name', 'model_name', 'gpu_name', 'cpu_generation', 'inference_level']].iterrows():
    print(f"\nRow {idx}:")
    print(f"  CPU: {row['CPU']}")
    print(f"  Mapped: {row['mapped_cpu_name']}")
    print(f"  Model: {row['model_name']}")
    print(f"  GPU: {row['gpu_name']}")
    print(f"  Generation: {row['cpu_generation']}")
    print(f"  Inference Level: {row['inference_level']}")
