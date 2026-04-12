from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Union

import cv2
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel

from vision import process_water_image
from model import calculate_depletion_year

load_dotenv(Path(__file__).resolve().parent / ".env")

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


class ReportRequest(BaseModel):
    hotspot: str
    depletion_year: Union[int, str]
    sample_years: list[int]
    pixel_counts: list[int]


@app.post("/api/report")
def generate_report(req: ReportRequest):
    """Call OpenAI to generate a policy brief for politicians."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(500, "OPENAI_API_KEY not set")

    pixel_change = req.pixel_counts[0] - req.pixel_counts[-1]
    pct_loss = round(pixel_change / req.pixel_counts[0] * 100, 1) if req.pixel_counts[0] else 0

    prompt = (
        f"You are an environmental policy advisor briefing legislators. "
        f"Write a concise, urgent 3-sentence policy brief (no bullet points, plain prose) about {req.hotspot}. "
        f"Key data: satellite analysis shows {pct_loss}% water surface loss from "
        f"{req.sample_years[0]} to {req.sample_years[-1]}. "
        f"At the current rate of depletion, the water body is projected to reach critical lows by {req.depletion_year}. "
        f"Focus on 2-3 specific, actionable policy interventions legislators can enact now. "
        f"Be direct, data-driven, and politically actionable. Do not use headers or bullet points."
    )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )

    text = response.choices[0].message.content or ""
    return {"report": text.strip()}


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
