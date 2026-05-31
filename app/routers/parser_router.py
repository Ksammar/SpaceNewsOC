import threading

from fastapi import APIRouter, HTTPException

from app.services.parser import run_parser

router = APIRouter(prefix="/api/parser", tags=["Parser"])

_parsing_lock = threading.Lock()
_is_parsing = False


@router.post("/run")
async def trigger_parser():
    global _is_parsing

    if _is_parsing:
        raise HTTPException(status_code=409, detail="Parser already running")

    _is_parsing = True

    def _run():
        global _is_parsing
        try:
            run_parser()
        finally:
            _is_parsing = False

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return {"status": "started", "message": "Parser started in background"}


@router.get("/status")
async def parser_status():
    return {"is_running": _is_parsing}
