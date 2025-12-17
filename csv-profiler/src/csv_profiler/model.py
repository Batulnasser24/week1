from __future__ import annotations
from typing import Any, Dict, List 
from datetime import datetime

class ColumnProfile:
    def __init__(self, name: str, inferred_type: str, total: int, missing: int, unique: int, stats: Dict[str, Any], notes: List[str] = None):
        self.name = name
        self.inferred_type = inferred_type
        self.total = total
        self.missing = missing
        self.unique = unique
        self.stats = stats
        self.notes = notes or []

    @property
    def missing_pct(self) -> float:
        if self.total <= 0: return 0.0
        return round((self.missing / self.total) * 100, 2)

    def get_quality_label(self) -> str:
        if self.missing_pct > 50: return "🔴 Poor"
        return "🟢 Good"

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "name": self.name,
            "type": self.inferred_type,
            "quality": self.get_quality_label(),
            "missing": self.missing,           # أضفنا هذا ليسهل الوصول إليه
            "missing_pct": self.missing_pct,    # نرسله كرقم للرندر
            "unique": self.unique,
            "notes": self.notes
        }
        data.update(self.stats) 
        return data

class ProfileReport:
    # التعديل هنا: أضفنا notes في الـ __init__
    def __init__(self, row_count: int, columns: List[ColumnProfile], notes: List[str] = None):
        self.row_count = row_count
        self.columns = columns
        self.notes = notes or [] # استقبال الملاحظات القادمة من دالة basic_profile
        self.generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rows": self.row_count, 
            "generated_at": self.generated_at,
            "notes": self.notes,
            "columns": {col.name: col.to_dict() for col in self.columns}
        }