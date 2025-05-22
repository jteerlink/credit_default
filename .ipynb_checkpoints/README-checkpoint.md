# credit_default

## 1.  EDA Summary

1. Error rate could indicate irregular payment and difficulty repaying on time
2. Having a time dimension would allow for potentially weighting or have more features focused on last 30/60/90 days for those with a lot of history.  
3. Large income and asset customer with $50 advance, potential fraud?
4. Savings account transfers into checking might be interesting to explore.
5. Hypothesis: previous customers might have lower default rates,
    1.  Disproven: Rates are nearly identical
6. Features where average decile slopes with default rate.  Likely important features and should explore feature engineering using these.  Expect to see these among top feature importances
    1. current balance, overdraft total, avg monthly spend
    2. balance average, total assets , number of transactions
    3. total cash, paycheck, avg monthly income ,avg monthly discretionary spend
    4. transactions per day, negative balance
7. Small % of outlier values.  Given intended strategy to use GBM type model, prefer to include outliers to reduce extrapolation risk
8. Target slightly imbalanced though documentation shows this was sampled as such, reality is likely much more imbalanced
9. ASSUMPTION: current balance and other missing values, impute 0 and add missing indicator column


## 2 Feature Engineering

Feature engineering brainstorm - underlined will be included in feature selection

1. advance to avg income ratio
2. advance to avg balance ratio
3. income stability proxy - min monthly income/ max monthly income
4. <u>balance volitility index</u> - min bal / avg bal (ideally we would have max bal too)
5. proportion of low balance days - captured in balance above 100
6. net cash flow 60D - already net assets
7. <u>deposit to withdrawl ratio</u> - avg spend/avg income
8. is first advance
9. <u>overdrafts per 30D</u> - overdraft count/(days open/30)
10. advance request hour - 



Notes:
- advance features dont mean anything since the field is uniform
- most features listed here may be valuable but would need access to unaggregrated data

    #### Approach
1. Opted to not floor/cap any potential outliers for simplicity
2. kept new features to only 3
3. While the paycheck model used is likely not a relevant feature decided to include and see how model uses it
4. Decided to not scale any features since we will be using XGBoost, though would likely create additional variables and try different scaling approaches to help normalize some of the larger scaled features

This could have also been created as a scikit learn pipeline but seemed overkill for simple operations



## Feature Selection

#### Approach 1: RFE with random forest

Observations:
1. RFE is fairly robust but has a few weakneses: computationaly expensive for large datasets, requires some intuition on selecting the number of features, depends heavily on estimator used
2. model name encoded features are not selected, confirming previous hypothesis
   
#### Approach 2:  XGBoost Feature importance

Observations

1. Difficult to compare relative ranking since RFE does not show indvidual ranking within top 21 features.
2. similar features were eliminated using same top n feature count
3. Final choice - remove all features with zero weight

## Model Training and Tuning

#### Approach

1. Establish baseline model with default hyperparameters
2. Select which hp to tune focusing on those that prevent overfitting since we have thin data
3. run tuning using optuna
4. evaluate performance using key metrics: AUC, Gini index


    #### See summary in model validation notebook


### Model Validation Summary
The final model metrics results look promising:
- Tuned model AUC: 0.7201 (+ 0.04 over baseline)
- Tuned model Gini: 0.4401 (+0.07 over baseline)

Both AUC and Gini coeefficient provide a reasonable degree of confidence that the model is well fit on the available data, without overfitting

1. The final model appears to do an adequate job at identifying high risk populations by decile.  The lift chart and actual default rate by decile charts show that the top 3 riskiest deciles account for a good portion of the defaults
2. The distribution overlap and the lift chart still show an area of opportunity to further improve model performance.  Typically a deeper analysis in partnership with credit analysts would deep dive into these middle deciles and identify features that would help futher seperate the defualts.
3. Potential next steps could include:
- obtaining additional data
- reverting to raw transactional data to allow additional time dependent feature engineering
- class weights were not used with this example due to XGBoost robustness agains imbalanced data and 22% positive class is much higher than is typically seen in production scenarios.  Implementing with this dataset may provide some additional lift

As a one off excercise the validation below may be adequate, if experiimentation was to continue I would develop this a bit further with more comprehensive functions to allow for faster iterations


### Deployment

Ideally this model would deployed as an API endpoint to be used in a decision engine or other customer facing website where customer upload their information and have a different prepocessing function to handle the rawest form of the data.  

The model was saved as a json object so that it is backwards compatible with multiple versions and can be loaded into various deployment systems.

This model analysis used the predicted probability output for the sake of simplicity from the model to assign risk deciles.  Typically, we would calculate the logit and use a calibration function to assign a score that is then split into deciles to assigning risk tiers.  There may be hard cuts at specific risk tiers or other credit policies enforced depending on the assigned risk level.


