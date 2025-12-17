import typer
import time
import subprocess
import sys
from pathlib import Path

# استيراد الوظائف من الحزمة
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown

app = typer.Typer(help="Professional CSV Profiling Tool")

@app.command()
def profile(
    input_file: Path = typer.Argument(..., help="Path to the input CSV file."),
    output: Path = typer.Option(Path("outputs"), "--output", "-o", help="Directory for reports.")
):
    """تحليل بيانات CSV وإنشاء تقارير JSON و Markdown."""
    start_time = time.perf_counter()

    if not input_file.exists():
        typer.secho(f"❌ File not found: {input_file}", fg="red", bold=True)
        raise typer.Exit(code=1)

    output.mkdir(exist_ok=True)
    typer.echo(f"🔍 Processing: {input_file.name}")
    
    # تنفيذ المنطق الأساسي
    rows = read_csv_rows(input_file)
    report = basic_profile(rows)

    # حفظ النتائج
    write_json(report, output / "report.json")
    write_markdown(report, output / "report.md")

    duration = (time.perf_counter() - start_time) * 1000
    typer.secho(f"✅ Completed in {duration:.2f}ms", fg="green", bold=True)
    typer.echo(f"📂 Reports saved to: {output.absolute()}")

@app.command()
def web():
    """تشغيل واجهة الويب التفاعلية (Streamlit)."""
    typer.secho("🚀 Starting Web Interface...", fg="cyan", bold=True)
    
    # تحديد مسار ملف app.py الموجود في المجلد الرئيسي للمشروع
    # بما أن cli.py موجود في src/csv_profiler/، نعود 3 مستويات للأعلى
    base_dir = Path(__file__).resolve().parent.parent.parent
    app_path = base_dir / "app.py"
    
    if not app_path.exists():
        typer.secho(f"❌ Error: app.py not found at {app_path}", fg="red", bold=True)
        typer.echo("Make sure app.py is in the root directory of your project.")
        raise typer.Exit(code=1)

    try:
        # تشغيل streamlit باستخدام subprocess
        # نستخدم sys.executable لضمان استخدام نفس بيئة بايثون (venv)
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)
    except KeyboardInterrupt:
        typer.echo("\n👋 Web interface stopped.")
    except Exception as e:
        typer.secho(f"❌ Failed to start Streamlit: {e}", fg="red")

if __name__ == "__main__":
    app()