
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("df.csv")
# Clean data
df = df[df['Price (AED)'] < 3e6].dropna()
df = df.sort_values('Date')
# Calculate Exponentially Weighted Moving Average (EWM)
df['Price EWM'] = df['Price (AED)'].ewm(span=10, adjust=False).mean()

df['Date'] = pd.to_datetime(df['Date'])

# Create temporary DatetimeIndex
temp_df = df.set_index('Date')

# Calculate 1-year shifted values
shifted_ewm = temp_df['Price EWM'].shift(freq=pd.DateOffset(years=1))
# Merge back and calculate percentage change
df = pd.merge_asof(df, shifted_ewm.rename("EWM_1Y_ago").reset_index(), on="Date")
df['Price EWM 1Y Change (%)'] = (df['Price EWM'] / df['EWM_1Y_ago'] - 1) * 100

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# First plot: Scatter plot with EWMA line
sns.scatterplot(
    data=df,
    x='Date',
    y='Price (AED)',
    hue='Contract Status',
    palette='viridis',
    s=100,
    alpha=0.7,
    ax=ax1
)

sns.lineplot(
    data=df,
    x='Date',
    y='Price EWM',
    color='red',
    linewidth=2,
    label='Price EWM',
    ax=ax1
)

ax1.set_title('Property Price Evolution in Downtown Dubai (3 Years)')
ax1.set_ylabel('Price (AED)')
ax1.grid(True)
ax1.legend(title='Contract Status', bbox_to_anchor=(1.05, 1), loc='upper left')

# Second plot: 1-year rate of change (%) of EWMA
sns.lineplot(
    data=df,
    x='Date',
    y='Price EWM 1Y Change (%)',
    color='blue',
    linewidth=2,
    label='1Y Rate of Change (%)',
    ax=ax2
)

ax2.set_title('1-Year Rate of Change (%) of EWMA')
ax2.set_ylabel('Rate of Change (%)')
ax2.grid(True)
ax2.legend(loc='upper left')

# Format x-axis to reduce number of ticks
ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

