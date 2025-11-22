import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 1. LOAD THE DATA
# ============================================
print("=" * 60)
print("1. LOADING DATA")
print("=" * 60)

import os

file_path = r'C:\Moataz Programming\DEPI_Final_Project\LAData.csv'

if not os.path.exists(file_path):
    print(f"ERROR: Cannot find '{file_path}'")
    print(f"Current directory: {os.getcwd()}")
    print("\nPlease update the file_path variable to the correct location.")
    exit()

print(f"Loading {file_path}...")
try:
    df = pd.read_csv(file_path)
    print(f"✓ File loaded successfully!")
    print(f"Initial shape: {df.shape}")
except Exception as e:
    print(f"ERROR loading file: {e}")
    exit()

print(f"\nActual columns in file:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")
print()

# ============================================
# 2. CREATE COLUMN MAPPING
# ============================================
print("=" * 60)
print("2. MAPPING COLUMN NAMES")
print("=" * 60)

column_mapping = {}
for col in df.columns:
    col_lower = col.lower().strip()
    
    if col_lower == 'dr_no':
        column_mapping['dr_no'] = col
    elif col_lower == 'date rptd':
        column_mapping['date_rptd'] = col
    elif col_lower == 'date occ':
        column_mapping['date_occ'] = col
    elif col_lower == 'time occ':
        column_mapping['time_occ'] = col
    elif col_lower == 'area':
        column_mapping['area'] = col
    elif col_lower == 'area name':
        column_mapping['area_name'] = col
    elif col_lower == 'rpt dist no':
        column_mapping['rpt_dist_no'] = col
    elif col_lower == 'part 1-2':
        column_mapping['part_1_2'] = col
    elif col_lower == 'crm cd' and '1' not in col_lower and '2' not in col_lower and '3' not in col_lower and '4' not in col_lower:
        column_mapping['crm_cd'] = col
    elif col_lower == 'crm cd desc':
        column_mapping['crm_cd_desc'] = col
    elif col_lower == 'mocodes':
        column_mapping['mocodes'] = col
    elif col_lower == 'vict age':
        column_mapping['vict_age'] = col
    elif col_lower == 'vict sex':
        column_mapping['vict_sex'] = col
    elif col_lower == 'vict descent':
        column_mapping['vict_descent'] = col
    elif col_lower == 'premis cd':
        column_mapping['premis_cd'] = col
    elif col_lower == 'premis desc':
        column_mapping['premis_desc'] = col
    elif col_lower == 'weapon used cd':
        column_mapping['weapon_cd'] = col
    elif col_lower == 'weapon desc':
        column_mapping['weapon_desc'] = col
    elif col_lower == 'status':
        column_mapping['status'] = col
    elif col_lower == 'status desc':
        column_mapping['status_desc'] = col
    elif col_lower == 'crm cd 1':
        column_mapping['crm_cd_1'] = col
    elif col_lower == 'crm cd 2':
        column_mapping['crm_cd_2'] = col
    elif col_lower == 'crm cd 3':
        column_mapping['crm_cd_3'] = col
    elif col_lower == 'crm cd 4':
        column_mapping['crm_cd_4'] = col
    elif col_lower == 'location':
        column_mapping['location'] = col
    elif col_lower == 'cross street':
        column_mapping['cross_street'] = col
    elif col_lower == 'lat':
        column_mapping['lat'] = col
    elif col_lower == 'lon':
        column_mapping['lon'] = col

print(f"Mapped {len(column_mapping)} columns:")
for std_name, actual_name in column_mapping.items():
    print(f"  {std_name} -> {actual_name}")
print()

# Rename columns to standard names
df = df.rename(columns={v: k for k, v in column_mapping.items()})

# ============================================
# 3. SELECT AND KEEP ONLY NECESSARY COLUMNS
# ============================================
print("=" * 60)
print("3. SELECTING ESSENTIAL COLUMNS")
print("=" * 60)

cols_to_keep = [
    'dr_no', 'date_rptd', 'date_occ', 'time_occ',
    'area', 'area_name', 'rpt_dist_no', 'part_1_2',
    'crm_cd', 'crm_cd_1', 'crm_cd_2', 'crm_cd_3', 'crm_cd_4',
    'crm_cd_desc', 'mocodes',
    'vict_age', 'vict_sex', 'vict_descent',
    'premis_cd', 'premis_desc', 'weapon_cd', 'weapon_desc',
    'status', 'status_desc',
    'location', 'cross_street', 'lat', 'lon'
]

# Check which columns exist
available_cols = [col for col in cols_to_keep if col in df.columns]
missing_cols = [col for col in cols_to_keep if col not in df.columns]

if missing_cols:
    print(f"⚠ Warning: The following columns are not available:")
    for col in missing_cols:
        print(f"    - {col}")
    print()

print(f"Keeping {len(available_cols)} out of {len(df.columns)} columns")
print("Columns to keep:")
for col in available_cols:
    print(f"  - {col}")
print()

# Drop unnecessary columns
df = df[available_cols].copy()
print(f"✓ Dropped {len(column_mapping) - len(available_cols)} unnecessary columns")
print(f"New shape: {df.shape}")
print()

# ============================================
# 4. HANDLE MISSING VALUES
# ============================================
print("=" * 60)
print("4. MISSING VALUES ANALYSIS")
print("=" * 60)

missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing_Count': missing,
    'Percentage': missing_pct
})
missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

if len(missing_df) > 0:
    print(missing_df)
else:
    print("No missing values found!")
print()

# ============================================
# 5. CLEAN DATE/TIME FIELDS
# ============================================
print("=" * 60)
print("5. CLEANING DATE/TIME FIELDS")
print("=" * 60)

# Convert date fields to datetime
if 'date_rptd' in df.columns:
    df['date_rptd'] = pd.to_datetime(df['date_rptd'], errors='coerce')

if 'date_occ' in df.columns:
    df['date_occ'] = pd.to_datetime(df['date_occ'], errors='coerce')

# Check for invalid dates
current_date = pd.Timestamp.now()
future_rptd = (df['date_rptd'] > current_date).sum() if 'date_rptd' in df.columns else 0
future_occ = (df['date_occ'] > current_date).sum() if 'date_occ' in df.columns else 0
old_dates = ((df['date_rptd'] < '1900-01-01').sum() if 'date_rptd' in df.columns else 0) + \
            ((df['date_occ'] < '1900-01-01').sum() if 'date_occ' in df.columns else 0)

print(f"Future report dates: {future_rptd}")
print(f"Future occurrence dates: {future_occ}")
print(f"Dates before 1900: {old_dates}")

# Flag problematic dates
df['date_flag'] = False
if 'date_rptd' in df.columns:
    df['date_flag'] = df['date_flag'] | (df['date_rptd'] > current_date) | (df['date_rptd'] < '1900-01-01') | df['date_rptd'].isna()
if 'date_occ' in df.columns:
    df['date_flag'] = df['date_flag'] | (df['date_occ'] > current_date) | (df['date_occ'] < '1900-01-01') | df['date_occ'].isna()

# Clean TIME OCC
if 'time_occ' in df.columns:
    df['time_occ'] = df['time_occ'].astype(str).str.strip()
    df['time_occ'] = df['time_occ'].str.replace('.0', '', regex=False)
    df['time_occ'] = df['time_occ'].str.zfill(4)
    
    # Validate military time
    def validate_military_time(time_str):
        try:
            if len(time_str) != 4:
                return False
            hour = int(time_str[:2])
            minute = int(time_str[2:])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    df['time_valid'] = df['time_occ'].apply(validate_military_time)
    invalid_times = (~df['time_valid']).sum()
    print(f"Invalid military times: {invalid_times}")
else:
    df['time_valid'] = False

# Create datetime column
if 'date_occ' in df.columns and 'time_occ' in df.columns:
    def create_datetime(row):
        if pd.notna(row['date_occ']) and row['time_valid']:
            try:
                hour = int(row['time_occ'][:2])
                minute = int(row['time_occ'][2:])
                return row['date_occ'] + pd.Timedelta(hours=hour, minutes=minute)
            except:
                return pd.NaT
        return pd.NaT
    
    df['datetime_occ'] = df.apply(create_datetime, axis=1)
    successful = df['datetime_occ'].notna().sum()
    print(f"Successfully created datetime for {successful:,} records")
print()

# ============================================
# 6. CLEAN VICTIM AGE
# ============================================
print("=" * 60)
print("6. CLEANING VICTIM AGE")
print("=" * 60)

if 'vict_age' in df.columns:
    df['vict_age'] = pd.to_numeric(df['vict_age'], errors='coerce')
    
    print(f"Age statistics:")
    print(f"  Min: {df['vict_age'].min()}")
    print(f"  Max: {df['vict_age'].max()}")
    print(f"  Mean: {df['vict_age'].mean():.2f}")
    print(f"  Median: {df['vict_age'].median()}")
    
    # Flag unrealistic ages
    df['age_flag'] = (df['vict_age'] < 0) | (df['vict_age'] > 120) | df['vict_age'].isna()
    invalid_ages = df['age_flag'].sum()
    print(f"Invalid ages (< 0 or > 120 or null): {invalid_ages}")
    
    if invalid_ages > 0:
        problematic = df[df['age_flag']]['vict_age'].value_counts().head(10)
        print(f"\nTop problematic age values:")
        print(problematic)
else:
    df['age_flag'] = False
print()

# ============================================
# 7. STANDARDIZE CATEGORICAL FIELDS
# ============================================
print("=" * 60)
print("7. CLEANING CATEGORICAL FIELDS")
print("=" * 60)

# Clean text fields - strip whitespace and uppercase
text_columns = ['vict_sex', 'vict_descent', 'status']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.upper()

# Validate Vict Sex
if 'vict_sex' in df.columns:
    valid_sex = ['F', 'M', 'X', 'NAN', 'NONE']
    df['sex_flag'] = ~df['vict_sex'].isin(valid_sex)
    print(f"Vict Sex - Invalid values: {df['sex_flag'].sum()}")
    if df['sex_flag'].sum() > 0:
        print("  Unique invalid values:", df[df['sex_flag']]['vict_sex'].unique()[:10])
    print("  Value counts:")
    print(df['vict_sex'].value_counts())
else:
    df['sex_flag'] = False

# Validate Vict Descent
if 'vict_descent' in df.columns:
    valid_descent = list('ABCDFGHIJKLOPSUVWXZ') + ['NAN', 'NONE', '-']
    df['descent_flag'] = ~df['vict_descent'].isin(valid_descent)
    print(f"\nVict Descent - Invalid values: {df['descent_flag'].sum()}")
    if df['descent_flag'].sum() > 0:
        print("  Unique invalid values:", df[df['descent_flag']]['vict_descent'].unique()[:10])
    print("  Value counts:")
    print(df['vict_descent'].value_counts())
else:
    df['descent_flag'] = False

# Check Status values
if 'status' in df.columns:
    print(f"\nStatus field unique values:")
    print(df['status'].value_counts())
print()

# ============================================
# 8. CLEAN GEOGRAPHIC DATA
# ============================================
print("=" * 60)
print("8. CLEANING GEOGRAPHIC DATA")
print("=" * 60)

# Convert to numeric
if 'lat' in df.columns:
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
if 'lon' in df.columns:
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

if 'lat' in df.columns and 'lon' in df.columns:
    print(f"Latitude range: {df['lat'].min():.4f} to {df['lat'].max():.4f}")
    print(f"Longitude range: {df['lon'].min():.4f} to {df['lon'].max():.4f}")

    # LA County boundaries (approximate)
    LA_LAT_MIN, LA_LAT_MAX = 33.7, 34.35
    LA_LON_MIN, LA_LON_MAX = -118.7, -118.1

    # Flag invalid coordinates
    df['coord_flag'] = (
        ((df['lat'] == 0) & (df['lon'] == 0)) |
        (df['lat'] < LA_LAT_MIN) | (df['lat'] > LA_LAT_MAX) |
        (df['lon'] < LA_LON_MIN) | (df['lon'] > LA_LON_MAX) |
        df['lat'].isna() | df['lon'].isna()
    )

    invalid_coords = df['coord_flag'].sum()
    zero_coords = ((df['lat'] == 0) & (df['lon'] == 0)).sum()
    print(f"Invalid coordinates: {invalid_coords}")
    print(f"  Zero coordinates (0,0): {zero_coords}")
    print(f"  Out of LA bounds: {invalid_coords - zero_coords}")
else:
    df['coord_flag'] = False
print()

# ============================================
# 9. CHECK DUPLICATES
# ============================================
print("=" * 60)
print("9. CHECKING FOR DUPLICATES")
print("=" * 60)

if 'dr_no' in df.columns:
    duplicate_dr_no = df['dr_no'].duplicated().sum()
    print(f"Duplicate DR_NO records: {duplicate_dr_no}")
    
    if duplicate_dr_no > 0:
        print("\nSample duplicate DR_NO values:")
        dups = df[df['dr_no'].duplicated(keep=False)]['dr_no'].value_counts().head()
        print(dups)
print()

# ============================================
# 10. VALIDATE CRIME CODE CONSISTENCY
# ============================================
print("=" * 60)
print("10. VALIDATING CRIME CODES")
print("=" * 60)

if 'crm_cd' in df.columns and 'crm_cd_1' in df.columns:
    df['crm_cd'] = df['crm_cd'].astype(str).str.strip()
    df['crm_cd_1'] = df['crm_cd_1'].astype(str).str.strip()
    
    mismatch = (df['crm_cd'] != df['crm_cd_1']) & df['crm_cd_1'].notna()
    print(f"Crime code mismatches (crm_cd vs crm_cd_1): {mismatch.sum()}")

if 'crm_cd' in df.columns:
    print("\nTop 10 Crime Codes:")
    print(df['crm_cd'].value_counts().head(10))
print()

# ============================================
# 11. CLEAN TEXT FIELDS
# ============================================
print("=" * 60)
print("11. CLEANING TEXT FIELDS")
print("=" * 60)

text_fields = ['location', 'cross_street', 'area_name', 'premis_desc', 
               'weapon_desc', 'status_desc', 'crm_cd_desc']

for col in text_fields:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace('nan', np.nan)
        df[col] = df[col].replace('None', np.nan)

print("✓ Text fields cleaned and standardized")
print()

# ============================================
# 12. AREA VALIDATION
# ============================================
print("=" * 60)
print("12. VALIDATING AREA CODES")
print("=" * 60)

if 'area' in df.columns:
    df['area'] = pd.to_numeric(df['area'], errors='coerce')
    valid_areas = df['area'].between(1, 21, inclusive='both')
    invalid_areas = (~valid_areas & df['area'].notna()).sum()
    
    print(f"Invalid area codes (should be 1-21): {invalid_areas}")
    print(f"Area distribution:")
    print(df['area'].value_counts().sort_index())
print()

# ============================================
# 13. CREATE COMPREHENSIVE QUALITY FLAG
# ============================================
print("=" * 60)
print("13. CREATING QUALITY FLAGS")
print("=" * 60)

df['has_quality_issues'] = (
    df['date_flag'] | 
    ~df['time_valid'] |
    df['age_flag'] |
    df['sex_flag'] |
    df['descent_flag'] |
    df['coord_flag']
)

quality_issues = df['has_quality_issues'].sum()
quality_pct = (quality_issues / len(df)) * 100

print(f"Records with quality issues: {quality_issues:,}")
print(f"Percentage: {quality_pct:.2f}%")
print(f"\nBreakdown of issues:")
print(f"  Date issues: {df['date_flag'].sum():,}")
print(f"  Time issues: {(~df['time_valid']).sum():,}")
print(f"  Age issues: {df['age_flag'].sum():,}")
print(f"  Sex issues: {df['sex_flag'].sum():,}")
print(f"  Descent issues: {df['descent_flag'].sum():,}")
print(f"  Coordinate issues: {df['coord_flag'].sum():,}")
print()

# ============================================
# 14. DEFINE FINAL 19 COLUMNS
# ============================================
print("=" * 60)
print("14. SELECTING FINAL 19 COLUMNS")
print("=" * 60)

final_columns = [
    'dr_no', 'date_rptd', 'date_occ', 'time_occ',
    'area', 'area_name', 'rpt_dist_no',
    'crm_cd', 'crm_cd_desc',
    'vict_age', 'vict_sex', 'vict_descent',
    'premis_desc', 'weapon_desc', 'status', 'status_desc',
    'location', 'cross_street', 'lat', 'lon'
]

# Check which final columns exist
final_cols_available = [col for col in final_columns if col in df.columns]
final_cols_missing = [col for col in final_columns if col not in df.columns]

if final_cols_missing:
    print(f"⚠ Warning: The following columns are not available:")
    for col in final_cols_missing:
        print(f"    - {col}")
    print()

print(f"Final dataset will have {len(final_cols_available)} columns:")
for i, col in enumerate(final_cols_available, 1):
    print(f"  {i:2d}. {col}")
print()

# ============================================
# 15. SAVE CLEANED DATA (3 FILES)
# ============================================
print("=" * 60)
print("15. SAVING CLEANED DATA")
print("=" * 60)

# Define quality flag columns
quality_flag_cols = ['date_flag', 'time_valid', 'age_flag', 'sex_flag', 
                     'descent_flag', 'coord_flag', 'has_quality_issues']

# FILE 1: Complete dataset with quality flags (for debugging)
df_with_flags = df[final_cols_available + quality_flag_cols].copy()
df_with_flags.to_csv('LAData_with_flags.csv', index=False)
print(f"✓ Saved: LAData_with_flags.csv")
print(f"  Records: {len(df_with_flags):,}")
print(f"  Columns: {len(final_cols_available) + len(quality_flag_cols)} ({len(final_cols_available)} data + {len(quality_flag_cols)} flags)")
print(f"  Purpose: Quality control and debugging")
print()

# FILE 2: High-quality records only (RECOMMENDED FOR ANALYSIS)
df_high_quality = df[~df['has_quality_issues']][final_cols_available].copy()
df_high_quality.to_csv('LAData_high_quality.csv', index=False)
print(f"✓ Saved: LAData_high_quality.csv ⭐ RECOMMENDED")
print(f"  Records: {len(df_high_quality):,} ({len(df_high_quality)/len(df)*100:.1f}% of total)")
print(f"  Columns: {len(final_cols_available)} (essential columns only)")
print(f"  Purpose: Production-ready for dashboards and analysis")
print()

# FILE 3: Problematic records only (for review)
df_issues = df[df['has_quality_issues']][final_cols_available + quality_flag_cols].copy()
df_issues.to_csv('LAData_issues.csv', index=False)
print(f"✓ Saved: LAData_issues.csv")
print(f"  Records: {len(df_issues):,} ({len(df_issues)/len(df)*100:.1f}% of total)")
print(f"  Columns: {len(final_cols_available) + len(quality_flag_cols)} ({len(final_cols_available)} data + {len(quality_flag_cols)} flags)")
print(f"  Purpose: Manual review and data quality investigation")
print()

# ============================================
# FINAL SUMMARY
# ============================================
print("=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"Original records: {len(df):,}")
print(f"High quality records: {len(df_high_quality):,} ({len(df_high_quality)/len(df)*100:.1f}%)")
print(f"Records with issues: {len(df_issues):,} ({len(df_issues)/len(df)*100:.1f}%)")
print(f"\nOutput files created (3 files):")
print(f"  1. LAData_with_flags.csv")
print(f"     - All records with quality flags")
print(f"     - {len(final_cols_available) + len(quality_flag_cols)} columns")
print(f"     - Use for: Quality control")
print(f"")
print(f"  2. LAData_high_quality.csv ⭐ USE THIS")
print(f"     - Clean records only ({len(df_high_quality):,} records)")
print(f"     - {len(final_cols_available)} columns")
print(f"     - Use for: Dashboards, visualizations, analysis")
print(f"")
print(f"  3. LAData_issues.csv")
print(f"     - Problematic records only ({len(df_issues):,} records)")
print(f"     - {len(final_cols_available) + len(quality_flag_cols)} columns (includes flags)")
print(f"     - Use for: Data quality review")
print("\n✓ Data cleaning pipeline complete!")
print("=" * 60)