# Limitations of PF PredictX

This document outlines the key limitations of the PF PredictX project, which focuses on forecasting power factor (PF) using machine learning models (Random Forest and LSTM) to enhance energy efficiency. Understanding these limitations is crucial for interpreting the model’s performance and planning future improvements.

## 1. Household-Centric Dataset
The dataset used for PF PredictX, sourced from the Kaggle Electric Power Consumption Data Set, contains over 2 million records of household power consumption over four years. While this provides a robust sample for residential scenarios, it does not include data from commercial or industrial settings, such as large firms or energy-intensive facilities. This limitation restricts the model’s exposure to diverse scenarios, such as:

- High-power inductive loads (e.g., heavy machinery, large motors) common in industrial plants.
- Complex load profiles in commercial buildings or data centers.
- Grid-level dynamics in utility-scale power systems.

As a result, the model may not generalize well to non-residential environments where PF patterns differ due to varying equipment, load imbalances, or operational schedules.

## 2. Absence of Weather Features
The dataset does not include weather-related features, such as temperature, humidity, or seasonal variations, which are known to impact power factor. For example:

- High temperatures can increase air conditioning loads, introducing inductive components that lower PF.
- Humidity affects the performance of electrical equipment, potentially altering PF in outdoor systems.
- Seasonal changes influence power consumption patterns, such as increased heating loads in winter.

Without these features, the model cannot account for weather-driven variations in PF, limiting its predictive accuracy in scenarios where environmental conditions play a significant role. Incorporating weather data could enhance the model’s robustness, particularly for outdoor or climate-sensitive systems.

## 3. Limited Prediction Horizon
The current model is designed to forecast PF for a single day, producing predictions for 96 intervals per day (every 15 minutes). While this short-term horizon is useful for immediate energy management decisions, it restricts the model’s utility for:

- Long-term planning, such as weekly or monthly PF optimization in industrial operations.
- Strategic energy management in smart grids, where multi-day forecasts could guide resource allocation.
- Seasonal trend analysis, which requires extended prediction windows to capture cyclical patterns.

Extending the prediction horizon would require additional computational resources and potentially more complex models to maintain accuracy over longer timeframes.

## 4. Additional Limitation: Computational Complexity
The LSTM model, selected for its superior performance, has high computational requirements due to its recurrent architecture. This complexity may pose challenges for real-time deployment in resource-constrained environments, such as small-scale IoT devices or low-power edge computing systems. While resampling the dataset to 15-minute intervals reduced computational load, the model’s scalability to high-frequency predictions or large-scale systems remains limited without optimization.

## Conclusion
The PF PredictX project demonstrates strong potential for PF forecasting in household settings, but its limitations highlight areas for improvement. The household-centric dataset restricts generalizability, the lack of weather features reduces robustness, and the one-day prediction horizon limits long-term applications. Additionally, computational complexity may hinder deployment in resource-limited scenarios. Addressing these limitations through diverse datasets, weather integration, extended forecasting, and model optimization could enhance the project’s applicability and impact across various energy management contexts.