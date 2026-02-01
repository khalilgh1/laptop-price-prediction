import pandas as pd

df = pd.read_csv('data_preprocesseds.csv')

# Find rows with 750S
i5_750s = df[df['CPU'].str.contains('750S', case=False, na=False)]

print(f'Found {len(i5_750s)} rows with 750S')

if len(i5_750s) > 0:
    print('\nDetails:')
    print(i5_750s[['CPU', 'mapped_cpu_name', 'cpu_tier', 'cpu_generation', 'model_name', 'gpu_name']].to_string(index=False))
    
    # Check if it's generic
    if 'is_generic_cpu' in i5_750s.columns:
        print(f"\nIs Generic: {i5_750s['is_generic_cpu'].values}")
    
    # Check inference level
    if 'inference_level' in i5_750s.columns:
        print(f"Inference Level: {i5_750s['inference_level'].values}")
