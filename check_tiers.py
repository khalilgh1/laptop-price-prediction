import pandas as pd

df = pd.read_csv('data_with_inferred_cpus.csv')

# Check i5 -> i7 mismatches
bad_i5_to_i7 = df[(df['CPU'].str.contains('CORE I5', case=False, na=False)) & 
                   (df['mapped_cpu_name'].str.contains('i7', case=False, na=False))]
print(f'i5 wrongly mapped to i7: {len(bad_i5_to_i7)}')
if len(bad_i5_to_i7) > 0:
    print('\nExamples:')
    print(bad_i5_to_i7[['CPU', 'mapped_cpu_name']].head(10))

print()

# Check i7 -> i5 mismatches
bad_i7_to_i5 = df[(df['CPU'].str.contains('CORE I7', case=False, na=False)) & 
                   (df['mapped_cpu_name'].str.contains('i5', case=False, na=False))]
print(f'i7 wrongly mapped to i5: {len(bad_i7_to_i5)}')
if len(bad_i7_to_i5) > 0:
    print('\nExamples:')
    print(bad_i7_to_i5[['CPU', 'mapped_cpu_name']].head(10))
