import sys
from pathlib import Path

# ضبط مسار المصدر للوصول إلى الحزمة
current_dir = Path(__file__).resolve().parent
src_path = current_dir / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    # الآن نستورد الـ app بعد ضبط المسار
    from csv_profiler.cli import app
except ImportError as e:
    print(f"❌ Critical Error: Could not load csv_profiler. {e}")
    sys.exit(1)

if __name__ == "__main__":
    # تشغيل البرنامج
    app()