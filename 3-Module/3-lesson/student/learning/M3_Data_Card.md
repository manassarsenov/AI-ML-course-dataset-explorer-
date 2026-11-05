# M3 Data Card — Telco customer churn

One row describes one customer. `customerID` is a raw identifier and never a model input. `Churn` (Yes/No) is the known answer used to train the model and check validation predictions. The question is whether a customer leaves; use only information available before that outcome.

| Field | Meaning |
|---|---|
| `tenure` | Months with the company |
| `MonthlyCharges` | Charge for one month |
| `TotalCharges` | Total recorded charge so far; blank means unknown, not zero |
| `PhoneService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies` | `Yes` means active; `No` and applicable `No ... service` values mean inactive |
| `InternetService` | `DSL` and `Fiber optic` mean active; `No` means inactive |

`num_services` counts these eight fields. Values outside the confirmed mapping must be checked and cause an error; they are never silently counted as zero. For a derived division, a missing numerator stays missing even if the denominator is zero; otherwise a zero denominator yields 0, and a missing denominator stays missing. One-hot encoding is fit on train; an unseen validation category is safely ignored for that field's encoded columns.

The source CSV is preserved unchanged. Stable raw IDs and the M3C1 split card set the same stratified 60% train / 20% validation / 20% final-test groups, with seed 42. The final test is reserved and excluded from working frames and every comparison. Imputation, scaling and one-hot categories fit on train only; validation receives transform only.

Source: IBM Telco Customer Churn dataset, pinned course copy at https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv . License: Apache License 2.0; see `IBM_LICENSE.txt`.