import subprocess
import sys


from fastapi import FastAPI, Depends
from shared_utils.auth import get_current_user, RoleChecker

from shared_utils.db_migration import router as migration_router
from .auth import router as auth_router



app = FastAPI(title="Admin Service API", description="APIs for admin operations.", version="1.0.0")

app.include_router(migration_router, tags=["Migration"])
app.include_router(auth_router, tags=["Auth"])


@app.post("/run-tests", tags=["Admin"], summary="Run backend test cases", description="Trigger pytest and return the results.")
def run_tests(user=Depends(get_current_user), role=Depends(RoleChecker(["admin"]))):
    """Run all backend tests and return the output."""
    try:
        # For host-based testing, use localhost URLs in the test script.
        # For container-based testing, use Docker service names in the test script.
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests", "--maxfail=5", "--disable-warnings", "-q"
        ], capture_output=True, text=True, cwd="/app")
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/health", tags=["Health"], summary="Health Check", description="Check if the Admin service is running.")
def health():
    return {"status": "ok"}


@app.get("/admin-data", tags=["Admin"], summary="Get Admin Data", description="Get admin data, requires 'admin' role.")
def admin_data(user=Depends(get_current_user), role=Depends(RoleChecker(["admin"]))):
    return {"data": "admin info"}
