import streamlit as st
import pandas as pd
import time
import os
import cv2

from vision import process_water_image
from model import calculate_depletion_year

st.set_page_config(page_title="Chrono-Climate", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = 1

# ---------------------------------------------------------------------------
# Step 1 — The Landing Page (The Hook)
# ---------------------------------------------------------------------------
if st.session_state.step == 1:
    st.markdown("# See the Future of Our Lakes")
    hotspot = st.selectbox(
        "Explore Global Hotspots",
        ["Lake Mead", "Aral Sea", "Jakarta"],
    )
    if st.button("Run Temporal Analysis"):
        st.session_state.hotspot = hotspot
        st.session_state.step = 2
        st.rerun()

# ---------------------------------------------------------------------------
# Step 2 — The "Processing" Illusion (The Flex)
# ---------------------------------------------------------------------------
elif st.session_state.step == 2:
    with st.status("Running Chrono-Climate Engine…", expanded=True) as status:
        st.write("[10%] Loading Historical Satellite Imagery...")
        time.sleep(1.2)
        st.write("[40%] Running Zero-Shot Segmentation...")
        time.sleep(1.5)
        st.write("[70%] Calculating Pixel Delta (Water vs. Arid Land)...")
        time.sleep(1.3)
        st.write("[90%] Generating Regression Models...")
        time.sleep(1.0)
        status.update(label="Analysis complete!", state="complete")
    st.session_state.step = 3
    st.rerun()

# ---------------------------------------------------------------------------
# Steps 3–5 render together after processing
# ---------------------------------------------------------------------------
else:
    # -------------------------------------------------------------------
    # Step 3 — The Historical Reveal (The "Eyes")
    # -------------------------------------------------------------------
    st.subheader("Historical Analysis (1984 – 2022)")

    showcase_years = ["1984", "2003", "2022"]
    showcase_paths = [
        os.path.join("assets", "historical", f"{y}.jpeg") for y in showcase_years
    ]

    images_raw = []
    images_seg = []
    for path in showcase_paths:
        raw = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        _, seg = process_water_image(path)
        images_raw.append(raw)
        images_seg.append(seg)

    show_mask = st.toggle("Show AI Segmentation Mask")

    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            st.image(
                images_seg[i] if show_mask else images_raw[i],
                caption=showcase_years[i],
                use_container_width=True,
            )

    st.divider()

    # -------------------------------------------------------------------
    # Step 4 — The Future Projection (The "Brain")
    # -------------------------------------------------------------------
    sample_years = list(range(1984, 2023, 5))
    if sample_years[-1] != 2022:
        sample_years.append(2022)

    pixel_counts = []
    for yr in sample_years:
        path = os.path.join("assets", "historical", f"{yr}.jpeg")
        count, _ = process_water_image(path)
        pixel_counts.append(count)

    depletion_year = calculate_depletion_year(sample_years, pixel_counts)

    if isinstance(depletion_year, int):
        st.error(f"🚨 Estimated Total Depletion: Year {depletion_year}")
    else:
        st.warning(depletion_year)

    chart_df = pd.DataFrame(
        {"Year": sample_years, "Water Pixels": pixel_counts}
    ).set_index("Year")
    st.line_chart(chart_df)

    future_step = st.slider(
        "Visualize Future Depletion",
        min_value=1,
        max_value=3,
        value=1,
    )
    future_path = os.path.join("assets", "future", f"future{future_step}.jpeg")
    future_img = cv2.cvtColor(cv2.imread(future_path), cv2.COLOR_BGR2RGB)
    st.image(future_img, caption=f"Projected Future — Stage {future_step}", use_container_width=True)

    st.divider()

    # -------------------------------------------------------------------
    # Step 5 — The Takeaway (Call to Action)
    # -------------------------------------------------------------------
    st.subheader("Intervention")

    if isinstance(depletion_year, int):
        st.markdown(
            f"At the current rate of decay, this body of water is losing significant "
            f"surface area annually. Immediate policy intervention is required before "
            f"**{depletion_year}**."
        )
    else:
        st.markdown(
            "Current trends do not indicate imminent depletion, but continued "
            "monitoring is critical."
        )

    st.download_button(
        label="Download Projection Report for Local Policy Distribution",
        data="Chrono-Climate Projection Report — placeholder content.",
        file_name="chrono_climate_report.txt",
        mime="text/plain",
    )
