# Project scope (read this before any modeling)

PCOSense is a **portfolio / learning project**. It estimates statistical patterns associated with a historical clinic label. It is **not** a medical device, screening program, or diagnostic test.

Do:

- State uncertainty (calibration, false negatives/positives).
- Separate “questionnaire-like” features from ultrasound/lab features that often *define* the label.
- Treat published 98–100% accuracies on this dataset as a **red flag**, not a target.

Do not:

- Claim the model “detects PCOS” or replaces a clinician.
- Invent pathophysiology from SHAP plots (association ≠ causation).
- Present Kerala hospital data as globally representative.
