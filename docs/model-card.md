# PCOSense Model Card

## Overview

PCOSense is an educational machine-learning screening system that estimates whether a patient's provided health information resembles patterns associated with PCOS in the training dataset.

It is not a diagnostic system and must not replace consultation, testing or diagnosis by a qualified medical professional.

## Dataset

- Records: 541
- Original columns: 45
- Cleaned columns: 44
- Positive PCOS records: 177
- Negative PCOS records: 364
- Positive-class percentage: 32.72%
- Duplicate records: 0

The dataset contains demographic, lifestyle, menstrual, laboratory and ultrasound-related information.

## Selected Feature Set

The deployed screening model uses 18 inputs that do not require ultrasound measurements:

1. Age
2. BMI
3. Menstrual-cycle regularity
4. Menstrual duration
5. Pregnancy status
6. Previous abortions or pregnancy losses
7. Weight gain
8. Excess hair growth
9. Skin darkening
10. Hair loss
11. Pimples or acne
12. Fast-food consumption
13. Regular exercise
14. Pulse rate
15. Respiratory rate
16. Haemoglobin
17. Systolic blood pressure
18. Diastolic blood pressure

## Models Compared

- Dummy classifier
- Logistic regression
- Decision tree
- Random forest
- XGBoost

Models were evaluated using a stratified train/test split and stratified cross-validation.

## Selected Model

The deployed model is a tuned Random Forest using the screening feature set.

### Holdout Performance

| Metric | Score |
|---|---:|
| Accuracy | 0.862 |
| Precision | 0.800 |
| Recall | 0.778 |
| F1 score | 0.789 |
| ROC-AUC | 0.889 |
| PR-AUC | 0.808 |
| Brier score | 0.125 |

## Explainability

SHAP was used to examine overall feature importance and individual predictions.

Important model features included:

- Weight gain
- Skin darkening
- Excess hair growth
- Fast-food consumption
- Menstrual duration
- Menstrual-cycle regularity

These relationships describe patterns learned from this dataset. They do not establish medical causation.

## Limitations

- The dataset contains only 541 records.
- The positive and negative classes are imbalanced.
- Some original values were missing, invalid or implausible.
- The model has not been externally or clinically validated.
- Performance may differ for populations not represented in the dataset.
- Self-reported inputs may contain measurement or reporting errors.
- A probability produced by the model is not an individual’s medical risk or diagnosis.

## Intended Use

PCOSense is intended for:

- Machine-learning education
- Portfolio demonstration
- Exploratory screening research
- Demonstrating an end-to-end ML application

## Prohibited Use

The model should not be used for:

- Medical diagnosis
- Treatment decisions
- Emergency guidance
- Replacing professional healthcare