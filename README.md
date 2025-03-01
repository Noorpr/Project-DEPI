# Project-DEPI
a DEPI Project 
# What is the Power Factor?
Power Factor (PF) is <span style="color: red">*the ratio of real power (measured in watts, W) to apparent power (measured in volt-amperes, VA) in an AC electrical system*</span>. It tells us how efficiently electrical power is being converted into useful work.


## ***Formula:***

\[
PF = \frac{\text{Real Power} (W)}{\text{Apparent Power} (VA)}
\]


Since real power (W) is the actual usable power and apparent power (VA) is the total power supplied, a **power factor of 1 (or 100%)** means perfect efficiency, while a **lower power factor** indicates wasted energy.



## **Why is it important?**

- A high PF (close to 1) means better efficiency.
- A low PF (<1) causes increased power losses and higher electricity costs.
- Industries correct PF using **capacitors** to avoid penalties and improve efficiency.



# Factors Affecting Power Factor in general (PF)


Several factors can influence the **Power Factor (PF)** in an AC electrical System:

## 1. Type of Load
- **Resistive Loads (PF ≈ 1)**  
     - Devices like heaters, incandescent bulbs, and resistors have a power factor close to **1** since they consume only real power.
   - **Inductive Loads (PF < 1, lagging)**  
     - Motors, transformers, fans, and solenoids cause a **lagging power factor** due to inductive reactance.
   - **Capacitive Loads (PF < 1, leading)**  
     - Devices like capacitor banks and synchronous motors can cause a **leading power factor**.


## **2. Presence of Inductive Components**
   - Inductive components store energy temporarily and return it to the source, reducing the power factor.
   - Examples: **Electric motors, fluorescent lighting ballasts, transformers**.

## **3. Voltage Variations**
   - Voltage fluctuations can change the behavior of reactive components, impacting PF.

## **4. Harmonics in the System**
   - Non-linear loads (e.g., **rectifiers, variable frequency drives, electronic devices**) generate harmonics, which distort the current waveform and reduce PF.

## **5. Load Imbalance**
   - Unequal distribution of loads across three-phase systems can cause an unbalanced current, lowering PF.

## **6. Power Factor Correction (PFC) Methods**
   - **Capacitor Banks**: Installed in parallel to inductive loads to improve PF.
   - **Synchronous Condensers**: Used in industrial setups to provide reactive power support.
   - **Active Power Factor Correction (APFC) Devices**: Electronics that automatically adjust PF.



# **Questions before working on any dataset:**

 - **Do you have Apparent Power (kVA) values?** If not, do you want an approximation?

 - **What time range does your dataset cover?** Hourly, daily, or monthly?

 # **Additional Sources**  
-  https://github.com/abdelazizrashed/Energy-Management-API
