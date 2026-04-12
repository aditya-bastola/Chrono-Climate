from __future__ import annotations

import io
import os
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from vision import process_water_image
from model import calculate_depletion_year

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

app = FastAPI(title="Chrono-Climate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze")
def analyze():
    """Run vision + regression on sampled historical images and return results."""
    sample_years = list(range(1984, 2023, 5))
    if sample_years[-1] != 2022:
        sample_years.append(2022)

    pixel_counts: list[int] = []
    for yr in sample_years:
        path = str(ASSETS_DIR / "historical" / f"{yr}.jpeg")
        count, _ = process_water_image(path)
        pixel_counts.append(count)

    depletion_year = calculate_depletion_year(sample_years, pixel_counts)

    return {
        "sample_years": sample_years,
        "pixel_counts": pixel_counts,
        "depletion_year": depletion_year,
    }


def _encode_jpeg(img_bgr: np.ndarray) -> bytes:
    success, buf = cv2.imencode(".jpeg", img_bgr)
    if not success:
        raise HTTPException(500, "Failed to encode image")
    return buf.tobytes()


@app.get("/api/images/{year}")
def get_historical_image(year: int, mask: bool = Query(False)):
    """Return a historical satellite image, optionally with segmentation overlay."""
    path = str(ASSETS_DIR / "historical" / f"{year}.jpeg")
    if not os.path.exists(path):
        raise HTTPException(404, f"No image for year {year}")

    if mask:
        _, seg_rgb = process_water_image(path)
        if seg_rgb is None:
            raise HTTPException(500, "Segmentation failed")
        img_bgr = cv2.cvtColor(seg_rgb, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = cv2.imread(path)

    return StreamingResponse(
        io.BytesIO(_encode_jpeg(img_bgr)),
        media_type="image/jpeg",
    )


@app.get("/api/images/future/{step}")
def get_future_image(step: int):
    """Serve a future projection image (1, 2, or 3)."""
    if step not in (1, 2, 3):
        raise HTTPException(400, "Step must be 1, 2, or 3")

    path = str(ASSETS_DIR / "future" / f"future{step}.jpeg")
    if not os.path.exists(path):
        raise HTTPException(404, f"No future image for step {step}")

    img_bgr = cv2.imread(path)
    return StreamingResponse(
        io.BytesIO(_encode_jpeg(img_bgr)),
        media_type="image/jpeg",
    )
