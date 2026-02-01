import pandas as pd

df = pd.read_csv('data_with_inferred_cpus.csv')

# Check for i3 11th gen
i3_11th = df[
    (df['cpu_tier'] == 'i3') & 
    (df['cpu_generation'] == 11.0) & 
    (~df['mapped_cpu_name'].str.startswith('Generic', na=False))
]

print(f'i3 11th gen CPUs: {len(i3_11th)} rows')
if len(i3_11th) > 0:
    print('\nMost common i3 11th gen CPUs:')
    print(i3_11th['mapped_cpu_name'].value_counts().head(10))
else:
    print('❌ No i3 11th gen data in dataset!')

# Check what GPUs are paired with i3 11th gen
if len(i3_11th) > 0:
    print('\nGPUs paired with i3 11th gen:')
    print(i3_11th['gpu_name'].value_counts().head(10))
