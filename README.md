# Machine Learning Foundations

This repository consolidates several of my earlier machine learning and data-processing repositories into a single, topic-based structure.

The projects were originally created as separate repositories while I was learning different parts of the machine learning workflow, including data preprocessing, regression, classification, clustering, model evaluation, visualization, web data collection, and PySpark.

The original repositories are preserved for reference:

* [LearningMachineLearningFromScratch](https://github.com/BipinRana/LearningMachineLearningFromScratch)
* [PreprocessingBasics](https://github.com/BipinRana/PreprocessingBasics)
* [PySpark](https://github.com/BipinRana/PySpark)

## Repository Structure

```text
.
├── 01-data-preprocessing/
├── 02-regression-and-regularization/
├── 03-classification/
├── 04-clustering/
├── 05-model-evaluation/
├── 06-pyspark/
├── 07-data-collection-and-visualization/
├── assets/
├── datasets/
```

## Contents

### 01 — Data Preprocessing

Exercises and notes covering foundational preprocessing tasks, including:

* data cleaning
* missing-value handling
* encoding
* feature scaling
* pandas operations
* basic preprocessing workflows

### 02 — Regression and Regularization

Implementations and experiments involving:

* simple and multiple linear regression
* decision-tree regression
* ridge regression
* lasso regression
* regularization from scratch
* coefficient sparsity
* linear and logistic regression fundamentals

### 03 — Classification

Classification exercises and implementations covering:

* logistic regression
* perceptrons
* k-nearest neighbors
* support vector machines
* decision trees
* entropy and Gini impurity
* class weighting
* comparisons between custom implementations and scikit-learn models

### 04 — Clustering

Contains introductory clustering work, including a two-cluster K-means example.

### 05 — Model Evaluation

Experiments focused on understanding model behavior and evaluation, including:

* cross-validation
* feature-scaling effects
* decision-tree complexity
* decision-boundary visualization

### 06 — PySpark

Introductory work with Apache Spark and PySpark, including:

* Spark DataFrames
* missing-value handling
* filtering
* aggregation
* logistic regression using PySpark ML

### 07 — Data Collection and Visualization

Exercises involving:

* Matplotlib
* REST APIs
* OpenWeather API
* web scraping

## Datasets

Reusable datasets have been consolidated under `datasets/` instead of being duplicated across individual exercises.

```text
datasets/
├── housing_test.csv
├── housing_train.csv
├── sample_employee_missing_values.csv
├── sample_people.csv
├── social_network_ads.csv
└── titanic.csv
```

## Assets

Supporting images and other non-code resources are stored under `assets/`.

## Consolidation Notes

This repository was created by combining three earlier learning repositories and reorganizing their contents by subject rather than by chronological filenames such as `Day1`, `Day2`, and `Day3`.

Where possible, filenames were also renamed to describe the actual implementation or experiment contained in each file.

The original repositories remain available separately so that their earlier structure and development history can still be referenced.

## Purpose

This repository primarily contains learning exercises, small experiments, and implementations created while developing a practical understanding of machine learning and data processing.

It is intended to show progression across the core workflow:

**data preparation → modeling → evaluation → experimentation → larger-scale processing**
