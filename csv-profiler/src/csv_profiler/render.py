from typing import Any, Dict
import json
from pathlib import Path
from csv_profiler.model import ProfileReport 

def render_markdown(report: ProfileReport) -> str:
    """تحويل التقرير إلى نص Markdown (للاستخدام في الويب والملفات)"""
    data = report.to_dict() 
    output = []
    
    output.append(f"# Data Profiling Report")
    output.append(f"\n| Metric | Value |")
    output.append(f"| :--- | :--- |")
    output.append(f"| Total Rows | {data['rows']} |")
    output.append(f"| Total Columns | {len(data['columns'])} |")
    
    output.append(f"\n## Column Details")
    for name, col_data in data['columns'].items():
        output.append(f"\n### Column: `{name}`")
        output.append(f"\n| Attribute | Value |")
        output.append(f"| :--- | :--- |")
        output.append(f"| Data Type | {col_data['type']} |")
        output.append(f"| Missing Values | {col_data['missing']} ({col_data['missing_pct']:.2f}%) |")
        output.append(f"| Unique Values | {col_data['unique']} |")
        
        if col_data['type'] in ["Integer", "Float"]:
            output.append(f"\n#### Numeric Statistics")
            output.append(f"| Statistic | Value |")
            output.append(f"| :--- | :--- |")
            # استخدام .get للحماية من الأخطاء في حال غياب المفتاح
            mean = col_data.get('mean', 'N/A')
            output.append(f"| Mean | {f'{mean:.2f}' if isinstance(mean, (int, float)) else mean} |")
            output.append(f"| Min | {col_data.get('min', 'N/A')} |")
            output.append(f"| Max | {col_data.get('max', 'N/A')} |")
            
        elif col_data['type'] == "String":
            output.append(f"\n#### Top 5 Values")
            output.append(f"| Value | Count |")
            output.append(f"| :--- | :--- |")
            for item in col_data.get('top', []):
                output.append(f"| `{item['value']}` | {item['count']} |")
                
    return '\n'.join(output)

def write_markdown(report: ProfileReport, path: Path) -> None:
    """حفظ النص المولد في ملف (لـ CLI)"""
    content = render_markdown(report)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Report saved to: {path}")

def write_json(report: ProfileReport, path: Path) -> None:
    data = report.to_dict() 
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Report saved to: {path}")