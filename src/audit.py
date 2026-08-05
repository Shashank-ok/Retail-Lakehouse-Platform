from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


AUDIT_FILE = Path("data") / "pipeline_audit.jsonl"


def log_pipeline_run(
    pipeline_name: str,
    status: str,
    rows_processed: int = 0,
    error_message: str | None = None,
) -> None:
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "run_id": str(uuid.uuid4()),
        "pipeline_name": pipeline_name,
        "status": status,
        "rows_processed": rows_processed,
        "error_message": error_message,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")