from typing import Any, Dict
import json
from pathlib import Path
from csv_profiler.model import ProfileReport 


def write_json(report: ProfileReport, path: Path) -> None:
    """
    Writes the profiling report to a JSON file.
    The report object must implement a to_dict() method.
    """
    data = report.to_dict() 
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Report saved to: {path}")


def write_markdown(report: ProfileReport, path: Path) -> None:
    """
    Writes the profiling report to a Markdown file.
    """
    data = report.to_dict() 
    
    output = []
    
    # 1. Header (Overall Report Summary)
    output.append(f"# Data Profiling Report")
    output.append(f"\n| Metric | Value |")
    output.append(f"| :--- | :--- |")
    output.append(f"| Total Rows | {data['rows']} |")
    output.append(f"| Total Columns | {len(data['columns'])} |")
    
    # 2. Column Details
    output.append(f"\n## Column Details")
    
    for name, col_data in data['columns'].items():
        output.append(f"\n### Column: `{name}`")
        output.append(f"\n| Attribute | Value |")
        output.append(f"| :--- | :--- |")
        output.append(f"| Data Type | {col_data['type']} |")
        output.append(f"| Missing Values | {col_data['missing']} ({col_data['missing_pct']:.2f}%) |")
        output.append(f"| Unique Values | {col_data['unique']} |")
        
        # 3. Add Specialized Stats (Numeric/Text)
        if col_data['type'] in ["Integer", "Float"]:
            output.append(f"\n#### Numeric Statistics")
            output.append(f"| Statistic | Value |")
            output.append(f"| :--- | :--- |")
            output.append(f"| Mean | {col_data.get('mean', 'N/A'):.2f} |")
            output.append(f"| Min | {col_data.get('min', 'N/A')} |")
            output.append(f"| Max | {col_data.get('max', 'N/A')} |")
            
        elif col_data['type'] == "String":
            output.append(f"\n#### Top 5 Most Frequent Values")
            
            top_k_list = col_data.get('top', [])
            output.append(f"| Value | Count |")
            output.append(f"| :--- | :--- |")
            
            if top_k_list:
                for item in top_k_list:
                    output.append(f"| `{item['value']}` | {item['count']} |")
            else:
                output.append(f"| (No non-missing values) | 0 |")
                
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

    print(f"Report saved to: {path}")