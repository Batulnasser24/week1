from __future__ import annotations
from typing import Any, Dict, List, Optional

class ColumnProfile:
    """Represents the complete profile and statistics for a single column."""
    def __init__(
        self,
        name: str,
        inferred_type: str,
        total: int,
        missing: int,
        unique: int,
        stats: Dict[str, Any],
        # ⬅️ تمت إضافة notes هنا لاستقبال الوسيط وتجنب الخطأ
        notes: List[str] 
    ) -> None:
        self.name = name
        self.inferred_type = inferred_type
        self.total = total
        self.missing = missing
        self.unique = unique
        self.stats = stats
        self.notes = notes # ⬅️ تخزين الملاحظات
        
    @property
    def non_missing(self) -> int:
        return self.total - self.missing

    @property
    def non_missing_pct(self) -> float:
        return 0.0 if self.total == 0 else 100.0 * self.non_missing / self.total

    @property
    def missing_pct(self) -> float:
        return 0.0 if self.total == 0 else 100.0 * self.missing / self.total

    def to_dict(self) -> Dict[str, Any]:
        """Converts the column object into a dictionary format for output."""
        result = {
            "name": self.name,
            "type": self.inferred_type,
            "total": self.total,
            "missing": self.missing,
            "non_missing": self.non_missing,
            "missing_pct": self.missing_pct,
            "non_missing_pct": self.non_missing_pct,
            "unique": self.unique,
            "notes": self.notes, # ⬅️ إضافة الملاحظات إلى الإخراج
        }
        # Merge specialized statistics (numeric or text)
        result.update(self.stats)
        
        return result

    def __repr__(self) -> str:
        return (
            f"ColumnProfile(name={self.name!r}, type={self.inferred_type!r}, "
            f"missing={self.missing}, total={self.total}, unique={self.unique})"
        )


class ProfileReport:
    """A container for the entire profiling report."""
    def __init__(self, row_count: int, columns: List[ColumnProfile], notes: List[str]):
        self.row_count = row_count
        self.columns = columns
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        """Converts the entire report object into a dictionary format for output."""
        return {
            "rows": self.row_count,
            "columns": {col.name: col.to_dict() for col in self.columns},
            "notes": self.notes,
        }
    
    def __repr__(self) -> str:
        return f"ProfileReport(rows={self.row_count}, columns={len(self.columns)})"