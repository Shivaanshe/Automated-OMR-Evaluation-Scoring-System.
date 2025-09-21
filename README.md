
Automated OMR Evaluation & Scoring System

🎯 Goal

robust Automated OMR (Optical Mark Recognition) System that:

* Reads scanned/photographed answer sheets (even if skewed, rotated, or unevenly lit).
* Detects filled bubbles reliably.
* Evaluates answers against predefined keys (Set A / Set B).
* Produces **per-question analysis, subject-wise scores, and total percentage**.
* Outputs results in **JSON, CSV, and annotated debug images**.

---

     Methodology

 1. Image Preprocessing

* Convert to grayscale.
* Apply Gaussian blur (noise reduction).
* Adaptive thresholding (robust under variable lighting).
* Morphological operations (remove specks, refine bubbles).

---

 2. Paper Detection & Warping

* Detect the **largest 4-point contour** (sheet boundary).
* Apply **perspective transform** → normalize skew/rotation.
* Guarantees consistent layout across random scans and photos.

---

 3. Template-based Bubble ROI Extraction

* Divide warped sheet into **5 blocks × 20 rows × 4 options (A–D)**.
* Each bubble ROI is defined as a **percentage of sheet width/height**.
* Scale-invariant: works across **different scan sizes & resolutions**.

---

 4. Bubble Fill Detection

Compute fill fraction:

  ```text
  fill_fraction = (black pixels in ROI) / (total ROI pixels)
  ```

Decision logic:

  * Valid if `fill ≥ 0.35`.
  * Only **darkest bubble** is chosen per question (unless multiple correct answers exist).
  * Fallback → if no bubble passes, pick max-filled bubble above safety margin.

---

5. Circle Track Method (Debug Overlay)

* Debug mode uses **circle tracking visualization** to validate detection.
* Steps:

  * Detect contours resembling bubbles.
  * Draw circles over each candidate.
  * Annotate with fill fractions and colors:

    * 🟢 Green = correct + marked
    * 🔴 Red = wrong + marked
    * 🔵 Blue = missed correct answer
    * ⚪ Gray = empty/unmarked

 This makes the system transparent and tunable — you can visually check if detection is aligned with real bubbles.

---

 6. Answer Evaluation

* Supports Set A and Set B keys.

* Strict set comparison:

  * If detected answers == key answers → ✅ Correct
  * Else → ❌ Incorrect

* Subject groups:

  * Python → Q1–20
  * EDA → Q21–40
  * SQL → Q41–60
  * Power BI → Q61–80
  * Statistics → Q81–100

---

7. Outputs

* **JSON**: per-question details (detected vs correct).
* **CSV**: structured results for analysis.
* **Debug image**: with bounding boxes + circle overlays.

---

 Robustness Against Random Scans

* ✅ Perspective correction → fixes skew/rotation.
* ✅ Adaptive thresholding → handles shadows & brightness changes.
* ✅ ROI template → resolution independent.
* ✅ Circle tracking → easy validation & fine-tuning.

---

Unique Features

* Works reliably on **random scans & mobile photos**.
* Provides **subject-wise analytics** in addition to total score.
* Batch results export (Excel download).
* **Circle track debug mode** = strong visual trust factor.

---

Example Usage

```python
from theme_1_omr_system import evaluate_image_path

result = evaluate_image_path(
    "samples/omr_sample1.jpg",
    version="A",
    debug=True  # saves debug overlay image
)

print("JSON saved at:", result["json_path"])
print("CSV saved at:", result["csv_path"])
print("Debug image saved at:", result["debug_path"])
```

Output:

* `omr_outputs/omr_sample1_xxxx.json`
* `omr_outputs/omr_sample1_xxxx.csv`
* `omr_outputs/omr_sample1_xxxx_debug.jpg`

---

Project Structure

```
📦 OMR-System
 ┣ 📜 app.py                 # Flask backend
 ┣ 📜 theme_1_omr_system.py  # Core OMR evaluator
 ┣ 📂 frontend               # HTML/CSS/JS frontend
 ┣ 📂 omr_outputs            # Results (JSON, CSV, Debug images)
 ┗ 📜 README.md              # Documentation
```
