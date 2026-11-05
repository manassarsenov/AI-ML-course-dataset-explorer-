# M3 Data Card — What the table words mean

One row is one customer. Read the field before you change a value.

| Field | Plain meaning | Keep in mind |
|---|---|---|
| `customerID` | Customer number | Keep it private. Do not send it to AI. |
| `Churn` | Whether the customer left: Yes or No | Keep this answer unchanged today. |
| `tenure` | Time with the company, in months | 24 months is 2 years. |
| `MonthlyCharges` | Charge for one month | It is not the total bill. |
| `TotalCharges` | Total charge recorded so far | An empty-looking value is unknown, not zero. |

## A few other field names

`Contract` and `PaymentMethod` describe the plan and payment choice. `InternetService` and `OnlineSecurity` describe services. `Partner` and `Dependents` describe household details. You do not need to study every field today.

## Source and reuse note

Dataset source: https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv

License: Apache-2.0 (Apache License 2.0). License name: Apache License 2.0.
