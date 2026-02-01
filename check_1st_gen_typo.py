import pandas as pd

df = pd.read_csv('data_preprocesseds.csv')

# Find the "1ST GEN" i3 rows
typo_rows = df[(df['CPU'].str.contains('1ST GEN INTEL CORE I3', case=False, na=False))]

print(f"Found {len(typo_rows)} rows with '1ST GEN INTEL CORE I3'")
print("\nDetails:")
for idx, row in typo_rows.iterrows():
    print(f"\nRow {idx}:")
    print(f"  CPU: {row['CPU']}")
    print(f"  Mapped: {row['mapped_cpu_name']}")
    print(f"  Tier: {row.get('cpu_tier', 'N/A')}")
    print(f"  Generation: {row.get('cpu_generation', 'N/A')}")
    print(f"  GPU: {row.get('gpu_name', 'N/A')}")
    print(f"  Inference Level: {row.get('inference_level', 'N/A')}")
    print(f"  Is Generic: {row.get('is_generic_cpu', 'N/A')}")
