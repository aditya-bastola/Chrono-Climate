# Chrono-Climate: Master Implementation Plan

**Context for AI Agent:** Act as a senior Python engineer building a hackathon MVP. Implement this exact specification. Do not overcomplicate the architecture. Prioritize a working, linear Streamlit narrative over perfect software engineering patterns.

---

## Phase 1: Environment Setup

1. **Create a `requirements.txt` file with the following:**
   ```text
   streamlit
   opencv-python
   scikit-learn
   numpy
   pillow
   pandas
   matplotlib
   ```

2. **Verify the folder structure exists exactly as follows** (The user already has the JPEGs populated):
   ```text
   /assets/
     ├── historical/  (contains 1984.jpeg through 2022.jpeg)
     └── future/      (contains future1.jpeg, future2.jpeg, future3.jpeg)
   app.py
   vision.py
   model.py
   ```

---

## Phase 2: Computer Vision Pipeline (`vision.py`)

**Goal:** Process historical images, isolate water pixels using HSV color thresholding, and return both the pixel count and a visual segmentation mask.

**Implementation Details for `vision.py`:**
* Import `cv2` and `numpy`.
* Create a function `process_water_image(image_path)`:
  * Read the image using `cv2.imread`. If the image fails to load, return `(0, None)`.
  * Convert the image from BGR to HSV.
  * Define NumPy arrays for a blue/dark water color range (e.g., `lower_blue = np.array([90, 50, 50])`, `upper_blue = np.array([130, 255, 255])` - *leave a comment that these may need tuning*).
  * Use `cv2.inRange` to create a binary mask.
  * Count the non-zero pixels in the mask (this is the water area).
  * Create a "Segmentation View" image by applying a bright neon blue color over the masked area on the original image (for Step 3 of the UI). Convert it back to RGB for Streamlit compatibility.
  * Return `(water_pixel_count, segmented_rgb_image)`.

---

## Phase 3: Machine Learning Engine (`model.py`)

**Goal:** Run a linear regression on the historical pixel data to predict the year the water pixels reach 0.

**Implementation Details for `model.py`:**
* Import `numpy` and `LinearRegression` from `sklearn.linear_model`.
* Create a function `calculate_depletion_year(years_list, pixel_counts_list)`:
  * Reshape `years_list` into a 2D NumPy array `X`.
  * Convert `pixel_counts_list` into a NumPy array `y`.
  * Initialize and fit the `LinearRegression` model.
  * Extract the slope (`coef_`) and intercept (`intercept_`).
  * If the slope is `>= 0`, return a string indicating no depletion.
  * Otherwise, solve for x when y=0 (`x = -intercept / slope`).
  * Return the predicted year as an integer.

---

## Phase 4: The Narrative Dashboard (`app.py`)

**Goal:** Build a 5-step interactive Streamlit app that perfectly executes the user flow narrative.

**Implementation Details for `app.py`:**
* Import `streamlit as st`, `pandas`, `time`, `os`, and the functions from `vision.py` and `model.py`.
* Set page config to `layout="wide"`, title to `"Chrono-Climate"`.
* Use `st.session_state` to track the user's progress through the app (e.g., `session_state.step`). Initialize it to `1`.

### Implement the 5-Step Flow exactly like this:

* **Step 1: The Landing Page (The Hook)**
  * Display a bold title: `"See the Future of Our Lakes"`.
  * Create a dropdown for "Explore Global Hotspots" (Options: "Lake Mead", "Aral Sea", "Jakarta" - default to Lake Mead).
  * Add a button: `"Run Temporal Analysis"`. When clicked, advance to Step 2.

* **Step 2: The "Processing" Illusion (The Flex)**
  * If the user clicked the analysis button, trigger an `st.status` or `st.spinner`.
  * Use `time.sleep()` to artificially stagger these status updates:
    1. `"[10%] Loading Historical Satellite Imagery..."`
    2. `"[40%] Running Zero-Shot Segmentation..."`
    3. `"[70%] Calculating Pixel Delta (Water vs. Arid Land)..."`
    4. `"[90%] Generating Regression Models..."`
  * Once complete, advance `session_state` to Step 3 and `st.rerun()`.

* **Step 3: The Historical Reveal (The "Eyes")**
  * Display a subheader: `"Historical Analysis (1984 - 2022)"`.
  * Load three specific images using `process_water_image()`: `assets/historical/1984.jpeg`, `assets/historical/2003.jpeg`, and `assets/historical/2022.jpeg`.
  * Create a toggle: `st.toggle("Show AI Segmentation Mask")`.
  * Display the images side-by-side using `st.columns(3)`. If the toggle is OFF, show the raw original images. If ON, show the neon-colored segmentation masks returned from `vision.py`.

* **Step 4: The Future Projection (The "Brain")**
  * Programmatically loop through a sample of the historical images (e.g., every 5 years from 1984 to 2022) using `vision.py` to get an array of years and an array of pixel counts.
  * Pass those arrays to `model.py` to get the `depletion_year`.
  * Display a massive red warning using `st.error()`: `"🚨 Estimated Total Depletion: Year [depletion_year]"`.
  * Draw a line chart using `st.line_chart` mapping the historical pixel decay.
  * **The Magic Trick (Wizard of Oz):** Create a slider labeled `"Visualize Future Depletion"` with options mapping to the future files (e.g., Step 1 maps to `assets/future/future1.jpeg`, Step 2 to `future2.jpeg`, etc.).
  * Display the selected future image below the slider to show the visceral impact.

* **Step 5: The Takeaway (Call to Action)**
  * Add an `st.divider()`.
  * Create a section titled `"Intervention"`.
  * Provide a generated text summary: `"At the current rate of decay, this body of water is losing significant surface area annually. Immediate policy intervention is required before [depletion_year]."`
  * Add a dummy `st.download_button` labeled `"Download Projection Report for Local Policy Distribution"`.