import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# SAMPLE DATA 
np.random.seed(42)
data = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "sales": np.random.randint(50, 150, 6),
    "profit": np.random.randint(20, 100, 6)
})

#  LINE PLOT
plt.figure(figsize=(7, 4))
plt.plot(data["month"], data["sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.savefig("line_plot.png")
plt.close()

#BAR CHART
plt.figure(figsize=(7, 4))
sns.barplot(x="month", y="profit", data=data)
plt.title("Monthly Profit Comparison")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.savefig("bar_chart.png")
plt.close()

# HISTOGRAM
plt.figure(figsize=(7, 4))
plt.hist(data["sales"], bins=5)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.savefig("histogram.png")
plt.close()

# HEATMAP
plt.figure(figsize=(5, 4))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("heatmap.png")
plt.close()

print("All visualizations created successfully!")

