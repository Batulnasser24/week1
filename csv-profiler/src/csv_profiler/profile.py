from __future__ import annotations
from typing import Any, Dict, List
from collections import Counter
from csv_profiler.model import ColumnProfile, ProfileReport # Ensure this path is correct

# --- Configuration Constants ---

# Set of strings considered as missing values
MISSING = {"", "na", "n/a", "null", "none", "nan"}
# Threshold for considering a column as numeric (e.g., 0.9 means 90% must be numbers)
NUMERIC_THRESHOLD = 0.9

# --- Helper Functions for Type Inference and Extraction ---

def is_missing(value: str | None) -> bool:
    """Checks if the given value is considered a missing value."""
    if value is None:
        return True
    return value.strip().casefold() in MISSING


def try_float(value: str) -> float | None:
    """Attempts to convert the string value to a float. Returns None on failure."""
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    """Infers the general data type (Integer, Float, String) for a list of values."""
    
    non_missing_values = [v for v in values if not is_missing(v)]

    if not non_missing_values:
        return "Unknown"

    int_count = 0
    float_count = 0
    total_non_missing = len(non_missing_values)
    
    for value in non_missing_values:
        f_val = try_float(value)
        if f_val is not None:
            if f_val == int(f_val):
                int_count += 1
            else:
                float_count += 1

    # Check if the proportion of numeric values meets the threshold
    if (int_count + float_count) / total_non_missing >= NUMERIC_THRESHOLD:
        if float_count == 0:
            return "Integer"
        else:
            return "Float"
    
    return "String"


def column_values(rows: list[Dict[str, str]], col: str) -> list[str]:
    """
    Extracts a list of all string values for a single specified column 
    from a list of row dictionaries. Returns empty string if column is missing.
    """
    return [row.get(col, "") for row in rows]


def numeric_stats(values: list[str]) -> Dict[str, Any]:
    """
    Compute descriptive statistics (min, max, mean, count, unique) 
    for column values assumed to be numeric (strings).
    Raises ValueError if a non-numeric, non-missing value is found.
    """
    
    usable_values = [v for v in values if not is_missing(v)]
    missing_count = len(values) - len(usable_values)
    
    nums: list[float] = []
    
    for v in usable_values:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)
        
    count = len(nums)
    
    if count == 0:
        return {
            "count": 0, 
            "missing": missing_count,
            "unique": 0,
            "min": None, 
            "max": None, 
            "mean": None
        }

    unique_count = len(set(nums))
    min_val = min(nums)
    max_val = max(nums)
    mean_val = sum(nums) / count
    
    return {
        "count": count,
        "missing": missing_count,
        "unique": unique_count,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
    }


def text_stats(values: list[str], top_k: int = 5) -> Dict[str, Any]:
    """
    Computes descriptive statistics (count, missing, unique) and the Top K 
    most common values for column values assumed to be text (strings).
    """
    
    usable_values = [v for v in values if not is_missing(v)]
    total_count = len(values)
    usable_count = len(usable_values)
    missing_count = total_count - usable_count
    
    if usable_count == 0:
        return {
            "count": 0, 
            "missing": missing_count,
            "unique": 0,
            "top": []
        }

    counts = Counter(usable_values)
    unique_count = len(counts)
    
    top_items = counts.most_common(top_k)
    
    # Format the top items as a list of dictionaries
    top_formatted = [{"value": v, "count": c} for v, c in top_items]
    
    return {
        "count": usable_count,
        "missing": missing_count,
        "unique": unique_count,
        "top": top_formatted,
    }


# --- Core Profiling Function (Integration of all stats and Model Classes) ---

def basic_profile(rows: List[Dict[str, str]]) -> ProfileReport:
    """
    Generates a ProfileReport object containing ColumnProfile objects for the dataset.
    This function orchestrates data reading, type inference, specialized statistics 
    calculation, and assembly into the final report object.
    """
    row_count = len(rows)
    
    if row_count == 0:
        return ProfileReport(row_count=0, columns=[], notes=["Empty dataset"])

    columns = list(rows[0].keys())
    column_profiles: List[ColumnProfile] = []
    
    for c in columns:
        values = column_values(rows, c)
        inferred_type = infer_type(values)
        stats: Dict[str, Any] = {}
        notes: List[str] = []
        
        # 1. Calculate specialized statistics based on inferred type
        try:
            if inferred_type in ["Integer", "Float"]:
                # Attempt to run numeric calculation
                stats = numeric_stats(values)
            else:
                # Run text calculation
                stats = text_stats(values)
                
        except ValueError:
            # If numeric_stats fails (e.g., found unexpected text), 
            # fall back to text stats and change the type for safety
            stats = text_stats(values)
            inferred_type = "String"
            notes.append("Type inferred as numeric, but non-numeric values were found; reverted to String stats.")
            
        # 2. Extract core counts from the calculated stats object
        missing_count = stats.get("missing", 0)
        unique_count = stats.get("unique", 0) 

        # 3. Instantiate the ColumnProfile object
        column_profile = ColumnProfile(
            name=c,
            inferred_type=inferred_type,
            total=row_count,
            missing=missing_count,
            unique=unique_count,
            stats=stats,
            notes=notes
        )
        
        column_profiles.append(column_profile)

    # 4. Return the final ProfileReport object
    return ProfileReport(
        row_count=row_count,
        columns=column_profiles,
        notes=[]
    )