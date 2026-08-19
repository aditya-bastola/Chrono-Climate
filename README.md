# 🌍 Chrono-Climate

> **See the past. Measure the present. Visualize the future.**

Chrono-Climate turns decades of satellite imagery into an intuitive visual story about shrinking water bodies. It combines computer vision with a simple, explainable regression model to measure historical water coverage, estimate a depletion year, and visualize future stages of decline.

The goal is simple: make long-term environmental change understandable in the time it takes to look at a chart—and useful enough to support conversations about intervention.

## ✨ What It Does

Chrono-Climate presents a five-step analysis experience:

1. **Choose a hotspot** — Explore supported locations including Lake Mead, the Aral Sea, and Jakarta.
2. **Run temporal analysis** — The app processes the historical imagery and builds the analysis.
3. **Reveal the past** — Compare satellite imagery from **1984, 2003, and 2022**, with an optional segmentation overlay.
4. **Project the future** — Measure water pixels across the historical series and fit a linear regression to estimate when the measured water area could reach zero.
5. **Drive the takeaway** — View the projected depletion result, future-stage imagery, and download a projection report.

## 🧠 How It Works

### 1. Water segmentation

Chrono-Climate uses OpenCV to convert each satellite image into HSV color space. Multiple color masks identify likely water pixels, while an additional mask excludes warm brown/orange/tan arid land. The resulting mask provides:

- A water-pixel count for quantitative analysis
- A visual segmentation overlay for human inspection

This approach is deliberately transparent and lightweight: the thresholds are visible in `vision.py` and can be tuned for different imagery datasets.

### 2. Historical trend modeling

The application samples historical imagery from **1984–2022**, measures the water-pixel count for each available year, and fits a `scikit-learn` `LinearRegression` model against year.

If the fitted trend is negative, Chrono-Climate extrapolates the year in which the modeled water-pixel count reaches zero. If the slope is non-negative, it reports that no depletion trend was detected.

> **Important:** the depletion year is a linear extrapolation of image-derived pixel counts, not a physical climate model or a guarantee of future conditions. Satellite coverage, segmentation thresholds, image quality, and changing environmental conditions can all affect the result.

### 3. Future visualization

The interface includes three staged future images that can be explored with an interactive slider, turning the numerical projection into an immediately understandable visual narrative.

## 🖥️ Tech Stack

| Layer | Technology |
| --- | --- |
| App | Streamlit |
| Language | Python |
| Computer vision | OpenCV, NumPy |
| Machine learning | scikit-learn |
| Data handling | Pandas |
| Visualization | Streamlit charts, Matplotlib |
| Image processing | Pillow |

Dependencies are defined in [`requirements.txt`](requirements.txt).

## 📁 Project Structure

```text
Chrono-Climate/
├── app.py                  # Streamlit application and user experience
├── vision.py               # HSV segmentation and water-pixel measurement
├── model.py                # Linear regression depletion estimate
├── requirements.txt        # Python dependencies
├── assets/
│   ├── historical/         # Historical satellite imagery
│   └── future/             # Future projection stages
├── backend/                # Backend-related project resources
├── frontend/               # Frontend-related project resources
└── plan.md                 # Project planning notes
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ recommended
- A local copy of this repository

### Installation

```bash
git clone https://github.com/aditya-bastola/Chrono-Climate.git
cd Chrono-Climate

python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## 🧪 Working With Your Own Imagery

The segmentation pipeline expects image files that OpenCV can read. Historical imagery is loaded from:

```text
assets/historical/<year>.jpeg
```

The current application references specific years while constructing its historical analysis, so adding a new year requires updating the available asset set and, where appropriate, the sampling logic in `app.py`.

For different satellite sources or landscapes, the HSV thresholds in `vision.py` may also need calibration. This is especially important when imagery has different atmospheric conditions, sensors, seasons, or color characteristics.

## 📊 Interpretation & Limitations

Chrono-Climate is designed as an **exploratory visualization and policy-communication tool**, not as a replacement for hydrological or climate-science forecasting.

Results can be affected by:

- Image resolution and acquisition conditions
- Clouds, haze, shadows, and seasonal variation
- HSV threshold selection
- Differences between satellite datasets
- The assumption of a linear historical trend
- Using pixel count as a proxy for water-surface area

For policy or scientific decisions, treat the projection as a signal for investigation and pair it with validated geospatial, hydrological, and climate datasets.

## 🎯 Why Chrono-Climate?

Climate change is often communicated through spreadsheets, scientific papers, and abstract projections. Chrono-Climate starts with something more immediate: **showing how a landscape changes through time**.

By pairing visual evidence with a transparent measurement and an interpretable trend model, the project aims to help researchers, communicators, students, and policymakers move from *“something is changing”* to *“here is the evidence, here is the trend, and here is what we should investigate next.”*

## 🤝 Contributing

Contributions are welcome. Useful areas include:

- Improved water segmentation methods
- More robust geospatial area measurements
- Additional satellite datasets and locations
- Non-linear or physically informed forecasting
- Better uncertainty estimates
- Automated report generation
- Tests and reproducible evaluation datasets

Please open an issue to discuss substantial changes before submitting a pull request.

## 📄 License

No license file is currently included in the repository. Until a license is added, the code should be treated as **all rights reserved**.

---

**Chrono-Climate** — making long-term environmental change visible, measurable, and actionable.
