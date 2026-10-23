"""
Lebanon Voter Roll Analyzer
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

path = sys.argv[1]
NAME = path.removesuffix(".csv")

def main():
    data, filename = cleaning(path)
    data, filename = general_stats(data, filename)
    data, filename = plots(data, filename)
    group_religion_by_vote(data)
    group_religion_by_percent(data)
    train_model(data)

# this is to be utilized after running .plot()
def plot_settings(NAME, TYPE):
    plt.xlabel(f"{TYPE}")
    plt.ticklabel_format(style="plain", axis="x")
    plt.tight_layout()
    plt.savefig(f"{NAME} {TYPE}.png", dpi=300)
    plt.close()  # Cleans up memory

def cleaning(path):

    # using with open is redundant, we can just immedediatly read and store the csv in a dataframe.
    data = pd.read_csv(path)

    # identify the columns that will need to be cleaned.
    cols = ["No. of voters 2022", "No. of voters 2018", "Difference"]

    # replace the columns that have commas and are strings to integers to prep for data analysis.
    data[cols] = data[cols].replace({",": ""}, regex=True).astype(int)

    # The district CSV files originally did not contain percentage data, so I construed it manually.
    if "Percentage %" not in data:
        data["Percentage %"] = data["Difference"] / data["No. of voters 2018"] * 100

    # turn off scientific notation
    pd.set_option("display.float_format", lambda x: "%.2f" % x)

    # filter out the total row, since it is skewing values.
    data = data[data["Religion"] != "Ignore"]

    return data, path

def general_stats(data, filename):

    # run .describe() on the basic csv.stats
    general_desc_stats = pd.DataFrame.describe(data, include="all")
    general_desc_stats_new = general_desc_stats.drop(index=general_desc_stats.index[-1])
    general_desc_stats_new.to_csv("General_Desc_Stats.csv", index=True)

    return data, filename

def plots(data, filename):

    # built-in plot wrapper from pandas. Plotting the original graph here

    # PLOT NUMBER ONE: VOTERS GENERALLY
    data.set_index("Sect")[["No. of voters 2018", "No. of voters 2022"]].plot(
        kind="barh", title=f"Voters by Sect 2018-2022 {NAME}"
    )
    TYPE = "No. of voters 2018-2022"
    plot_settings(NAME, TYPE)

    # PLOT NUMBER TWO: PERCENTAGE DIFFERENCES GENERALLY
    data.set_index("Sect")["Percentage %"].plot(
        kind="barh", title=f"Changes in Voters, 2018-2022 {NAME}"
    )

    TYPE = "Percentage %"

    plot_settings(NAME, TYPE)

    return data, filename

# When I run these two functions and pass the data, it actually screws up the data for the scikit-learn def. I should change the passed arguments.

def group_religion_by_vote(data):

    # create a new df that groups all the sects by their corresponding 'Religion' using .groupby(), and sum the values inside it.
    grouped_data = data.groupby("Religion")[
        ["No. of voters 2018", "No. of voters 2022"]
    ].sum()
    
    grouped_data = grouped_data.sort_values(by="No. of voters 2018", ascending=False)

    # THIRD PLOT: GROUPED BY RELIGION VOTERS
    grouped_data.plot(kind="barh", title=f"Voters by Religion 2018-2022 {NAME}")

    TYPE = "No. of voters"
    # modifying the plot using plt
    plot_settings(NAME, TYPE)

def group_religion_by_percent(data):

    df_grouped2 = data.groupby("Religion")[["Percentage %"]].sum()

    # FOURTH PLOT: GROUPED BY RELIGION PERCENTAGE
    df_grouped2.plot(
        kind="barh",
        title=f"Voters by Religion % Change 2018-2022 {NAME}",
    )

    TYPE = "Grouped Percentage %"

    plot_settings(NAME, TYPE)

def train_model(data):

    data = data.groupby("Religion").agg(
        {"No. of voters 2018": "sum", "No. of voters 2022": "sum", "Difference": "sum"}
    )

    data["Percentage %"] = data["Difference"] / data["No. of voters 2018"] * 100

    # Save a copy so you can inspect the aggregated data
    data.to_csv("Debugging_data.csv")

    X_train = np.array([[2018], [2022]])

    predictions = {}

    for religion, row in data.iterrows():

        # Voter counts for this religion in 2018 and 2022
        y_train = np.array([row["No. of voters 2018"], row["No. of voters 2022"]])

        # Create the linear regression model
        model = LinearRegression()

        # Give the model the years and voter counts
        model.fit(X_train, y_train)

        # Predict the number of voters in 2028
        prediction = model.predict(np.array([[2028]]))

        # Round because we can't have a fraction of a voter
        predictions[religion] = round(prediction[0])

    data["Predicted 2028"] = data.index.map(predictions)

    data["Projected Growth %"] = (
        (data["Predicted 2028"] - data["No. of voters 2022"])
        / data["No. of voters 2022"]
        * 100
    )

    years = [2018, 2022, 2028]

    plt.figure(figsize=(12, 7))

    for religion, row in data.iterrows():

        voter_counts = [
            row["No. of voters 2018"],
            row["No. of voters 2022"],
            row["Predicted 2028"],
        ]

        plt.plot(years, voter_counts, marker="o", linewidth=2, label=religion)

    plt.xlabel("Year")
    plt.ylabel("Number of Voters")
    plt.title("Lebanese Elections: Voter Counts by Religion")
    plt.xticks(years)
    plt.legend(title="Religion")
    plt.grid(alpha=0.3)

    plt.tight_layout()

    # Save graph
    plt.savefig(f"scikit-learn {NAME}", dpi=300)

if __name__ == "__main__":
    main()
