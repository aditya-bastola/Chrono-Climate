🌍 Chrono-Climate
Translating decades of complex, raw satellite imagery into undeniable, actionable climate policy.

It is genuinely heartbreaking to watch our lakes and reservoirs vanish. The proof is right above us in satellite archives, but that data has been locked away in formats that everyday people and politicians simply cannot read. Chrono-Climate is an intensely visual and highly useful policy tool that bridges three eras of time to translate decades of complex imagery into a deeply original presentation that any legislator can understand and act on in under two minutes.

🚀 The Tech Stack
Languages: Python, TypeScript

Backend: FastAPI (REST endpoints for raw images, processed masks, future projections, and reports)

Computer Vision: OpenCV (HSV color space conversion, layered cv2.inRange masks)

Machine Learning: scikit-learn (LinearRegression)

Frontend: Next.js 16

Styling & Components: Tailwind CSS v4, Shadcn/ui

Charting: Recharts

LLM: OpenAI gpt-4o-mini

🛠️ How It Works
Unlocking the Past: The application ingests 38 years of satellite imagery (1984 through 2022) of a shrinking water body (like the Aral Sea). Custom computer vision maps and measures the exact water surface area in pixels using three additive masks to isolate water and a fourth to strip out arid land.

Predicting the Future: We feed those pixel counts into an explainable, transparent scikit-learn Linear Regression model mapped against the years to definitively project the exact year the lake will completely dry up.

Visualizing the Reality: A beautiful 5-step narrative flow renders a visceral, side-by-side historical reveal. Users watch the lake shrink decade by decade with an AI segmentation overlay, then push into the future to visualize three brutal depletion stages (2032, 2042, 2052) via an interactive decay slider.

Empowering the Present: The app automatically generates a policy brief—a concise, data-grounded paragraph written by GPT-4o-mini directly to legislators with immediate, actionable intervention steps.
