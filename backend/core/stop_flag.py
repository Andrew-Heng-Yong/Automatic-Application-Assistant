from __future__ import annotations

import threading

STOP_EVENT = threading.Event()


def request_stop() -> None:
    STOP_EVENT.set()


def clear_stop() -> None:
    STOP_EVENT.clear()


def is_stop_requested() -> bool:
    return STOP_EVENT.is_set()
