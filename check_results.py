import pandas as pd

df = pd.read_csv('data_with_inferred_cpus.csv')

print(f'Total rows: {len(df)}')
print(f'Generic remaining: {df["is_generic_cpu"].sum()}')
print(f'Specific: {(~df["is_generic_cpu"]).sum()}')

# Check Level 5 usage
if 'inference_level' in df.columns:
    level_counts = df[df['inference_level'].notna()]['inference_level'].value_counts().sort_index()
    print(f'\nInference level usage:')
    for level, count in level_counts.items():
        print(f'  Level {int(level)}: {count} CPUs')
