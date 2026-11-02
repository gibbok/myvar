+++
title = 'Guide to Machine Learning Classification Metrics'
date = 2026-11-01T15:30:45.066352
draft = false
tags = ['machine-learning-classification-metrics-f1-score']
description = 'Evaluate model performance using accuracy precision recall and f1 score. Learn key machine learning concepts.'
+++

## Overview
Classification metrics quantify model performance across distinct error types. **Accuracy**, **Precision**, **Recall**, and **F1-Score** evaluate different aspects of prediction quality, balancing overall correctness against false positives and false negatives.

## Key Insights
* **Accuracy** measures overall correct predictions but yields misleading evaluations on imbalanced datasets.
* **Precision** measures target accuracy among positive predictions, minimizing **False Positives**.
* **Recall** measures target identification completeness among actual positive cases, minimizing **False Negatives**.
* **F1-Score** calculates the harmonic mean of Precision and Recall, establishing a reliable baseline for imbalanced data.

## Technical Details

### The Confusion Matrix Base
All primary classification metrics rely on the four outcomes of a **Confusion Matrix**:

* **True Positive (TP):** Model correctly identifies a positive instance.
* **True Negative (TN):** Model correctly identifies a negative instance.
* **False Positive (FP):** Model incorrectly identifies a negative instance as positive (Type I Error).
* **False Negative (FN):** Model incorrectly identifies a positive instance as negative (Type II Error).

### Formulas and Use Cases

#### Accuracy
Calculates the proportion of correct predictions relative to total predictions.
$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}$$
* **Primary Use Case:** Datasets with evenly distributed classes.

#### Precision
Calculates the proportion of true positives among all instances predicted as positive.
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$
* **Primary Use Case:** Environments where False Positives incur high costs (e.g., spam filtering, content moderation).

#### Recall (Sensitivity)
Calculates the proportion of true positives identified out of all actual positive instances.
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
* **Primary Use Case:** Environments where False Negatives incur critical risks (e.g., disease diagnostics, fraud detection).

#### F1-Score
Calculates the harmonic mean of Precision and Recall to balance both metrics in a single score.
$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
* **Primary Use Case:** Class-imbalanced datasets requiring an optimized trade-off between Precision and Recall.

---

### Basic Example: Medical Screening Test

A binary classification model screens **100 patients** for a target condition. 

#### Dataset Distribution
* **Actual Positives (Diseased):** 10 patients
* **Actual Negatives (Healthy):** 90 patients

#### Model Outputs
* **TP:** 8 (Diseased patients correctly diagnosed)
* **TN:** 85 (Healthy patients correctly identified)
* **FP:** 5 (Healthy patients incorrectly diagnosed as diseased)
* **FN:** 2 (Diseased patients incorrectly identified as healthy)

#### Calculated Metrics

* **Accuracy:** 
  $$\frac{8 + 85}{100} = 93.0\%$$
* **Precision:** 
  $$\frac{8}{8 + 5} = \frac{8}{13} \approx 61.5\%$$
* **Recall:** 
  $$\frac{8}{8 + 2} = \frac{8}{10} = 80.0\%$$
* **F1-Score:** 
  $$2 \times \frac{0.615 \times 0.800}{0.615 + 0.800} \approx 69.5\%$$

#### Evaluation
The high **Accuracy** ($93.0\%$) presents a false sense of model capability caused by the dominant negative class ($TN = 85$). **Recall** ($80.0\%$) reveals that the model fails to detect $20\%$ of infected patients. **Precision** ($61.5\%$) highlights a high false-alarm rate. The **F1-Score** ($69.5\%$) provides the accurate system performance summary by combining these two limitations.