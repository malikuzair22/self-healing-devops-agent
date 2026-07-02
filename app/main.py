import random
import time
import logging
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Self-Healing DevOps Agent — Target App",
    description="Intentionally buggy app for the agentic SRE demo.",
    version="1.0.0"
)

# ── Prometheus metrics (auto-instruments all routes) ─────────────────────────
Instrumentator().instrument(app).expose(app)


# ── 1. /health ────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    """
    Basic liveness check.
    Always returns 200 OK when the pod is alive.
    """
    logger.info("Health check called")
    return {"status": "healthy", "service": "target-app"}


# ── 2. /process ───────────────────────────────────────────────────────────────
@app.get("/process")
def process(items: int = 10):
    """
    Simulates normal workload processing.
    Accepts an 'items' query param (default 10).
    Adds a small realistic delay proportional to items.
    """
    if items < 1 or items > 1000:
        raise HTTPException(status_code=400, detail="items must be between 1 and 1000")

    start = time.time()
    # Simulate work
    result = sum(i * random.random() for i in range(items))
    duration = round(time.time() - start, 4)

    logger.info(f"Processed {items} items in {duration}s")
    return {
        "status": "ok",
        "items_processed": items,
        "result": round(result, 4),
        "duration_seconds": duration
    }


# ── 3. /risky ─────────────────────────────────────────────────────────────────
FAILURE_MODE = None  # Set via /set-failure for demo control


@app.post("/set-failure")
def set_failure(mode: str = "none"):
    """
    Demo control endpoint.
    Set failure mode: 'none' | 'exception' | 'oom' | 'slow'
    """
    global FAILURE_MODE
    allowed = {"none", "exception", "oom", "slow"}
    if mode not in allowed:
        raise HTTPException(status_code=400, detail=f"mode must be one of {allowed}")
    FAILURE_MODE = mode
    logger.warning(f"Failure mode set to: {mode}")
    return {"failure_mode": FAILURE_MODE}


@app.get("/risky")
def risky():
    """
    Intentionally buggy endpoint that can simulate 3 failure modes:
    - exception : raises an unhandled 500 error
    - oom       : allocates a huge list to simulate memory spike
    - slow      : sleeps for 15 seconds to simulate timeout
    - none      : runs normally (default)
    """
    global FAILURE_MODE

    logger.warning(f"Risky endpoint called | failure_mode={FAILURE_MODE}")

    if FAILURE_MODE == "exception":
        logger.error("Simulating unhandled exception!")
        raise Exception("Simulated application crash — unhandled exception")

    elif FAILURE_MODE == "oom":
        logger.error("Simulating memory spike!")
        # Allocate ~500MB to simulate OOM pressure
        _ = [bytearray(1024 * 1024) for _ in range(500)]
        return {"status": "oom simulation complete (if you see this, OOM did not kill the pod)"}

    elif FAILURE_MODE == "slow":
        logger.warning("Simulating slow response — sleeping 15s")
        time.sleep(15)
        return {"status": "slow response completed"}

    else:
        # Normal execution
        return {"status": "ok", "message": "Risky endpoint executed safely — no failure mode set"}


# ── 4. /status ────────────────────────────────────────────────────────────────
@app.get("/status")
def status():
    """
    Returns current failure mode and app metadata.
    Useful for the Streamlit dashboard to display app state.
    """
    return {
        "service": "target-app",
        "version": "1.0.0",
        "current_failure_mode": FAILURE_MODE or "none",
        "endpoints": ["/health", "/process", "/risky", "/status", "/metrics"]
    }