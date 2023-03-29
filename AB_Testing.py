# Import necessary libraries and data preparation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("/Users/ecemolgun/Desktop/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("/Users/ecemolgun/Desktop/ab_testing.xlsx", sheet_name="Test Group")

df_control.head()
df_test.head()

df_control = df_control.copy()
df_test = df_test.copy()

# Control and Test group data analyzing

def check_df(df, head=5):
    print("##################### Shape #####################")
    print(df.shape)
    print("##################### Types #####################")
    print(df.dtypes)
    print("##################### Head #####################")
    print(df.head())
    print("##################### Tail #####################")
    print(df.tail())
    print("##################### NA #####################")
    print(df.isnull().sum())
    print("##################### Quantiles #####################")
    print(df.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

# Combining the control and test group

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()
df.shape

# Hypothesis
# H0 : M1 = M2 (There is no difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a difference between the control group and test group purchasing averages.)

df.groupby("group").agg({"Purchase": "mean"})

# Performing Hypothesis testing

# Normality Assumption Testing
# H0: Normal distribution assumption is provided.
# H1: Normal distribution assumption is not provided.
# p-value < 0.05 (H0 REJECTED)
# p-value > 0.05 (H0 IS NOT REJECTED)

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Data visualization

import seaborn as sns

def create_displot(dataframe, col):
    sns.displot(data=dataframe, x=col, kde=True)
    plt.show()

create_displot(df_control, "Purchase")

# Variance Homogeneity
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous
# p-value < 0.05 (H0 REJECTED)
# p-value > 0.05 (H0 IS NOT REJECTED)

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Determining the statistical test appropriate to the results (Two Independent Sample T-test(Parametric test))


# H0: M1 = M2 (There is no statistically significant difference between the control group and test group purchasing averages.)
# H1: M1 != M2 (There is a statistically significant difference between the control group and test group purchasing averages.)

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"], equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#H0 IS NOT REJECTED