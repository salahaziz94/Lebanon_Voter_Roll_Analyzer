# Lebanon Voter Roll Analyzer
  #### Video Demo:  <https://youtu.be/jHg4I4DT1-k>
  #### Description:
  A command-line tool that analyzes registered-voter counts in Lebanon by
religion and sect, comparing the 2018 and 2022 voter rolls for a given
electoral district (or the whole country) and projecting the trend forward
to 2028. It reads a CSV file, cleans it, calculates how each group changed,
and saves charts.

Note: the data counts **registered voters**, not the population. The rolls
include people who live abroad and exclude people under 21, so they should
not be read as a census. The data is also from Informational International,
of which was manually collected into CSV files myself.

## Usage
    python project.py 'csv-file', e.g., python project.py Beirut_I.csv

Install the requirements first: `pip install -r requirements.txt`

## Data
The CSV files of Nationwide Data and the two Beirut Districts (I and II) were compiled
by hand from Information International's PDF publication (see provided PDF file). Each CSV file has the columns
`Religion`, `Sect`, `No. of voters 2022`, `No. of voters 2018`, and
`Difference` and `Percentage %`. The totals rows were excluded for analysis.

## What it produces
- A bar chart of registered voters by sect (2018-2022)
- A bar chart of percent change by sect, 2018-2022
- A grouped bar chart of voters by religion, 2018 vs 2022
- A bar chart of percent change by religion
- A line chart of each religion's 2018 and 2022 counts and a projected
  2028 value
- `General_Desc_Stats.csv`, a table of summary statistics based on Nationwide data

## Files
- `project.py`: the main program
  - `plot_settings()` is a time-saving function that collects plt
    settings to be run when generating plots in memory.
  - `cleaning()` loads the CSV, converts the counts to integers, and
    adds a percent-change column
  - `general_stats()` writes the summary stats and makes the charts
  - `train_model()` fits a linear regression for each religion and
    projects 2028
- `test_project.py`: pytest tests.
- `requirements.txt`: the packages used

### In-Depth Notes on the Functions
  ## project.py
  ### cleaning()
  - After the data recieves information from the command-line argument,
  the cleaning function parses out any given commas in the columns that
  we want cleaned. The manual data may also have str objects, so we turn
  those into integers to prepare for the analyses. Some district-data
  does not have percentages in the columns, so there is code to make
  that data as well. We have a boilerplate command to turn off
  scientific notation, and we remove the row of total since that will
  skew our future analyses.
  ### general_stats()
  - This function takes the cleaned data passed from cleaning() and
  runs the method of .describe() from pandas. This function generates
  general information of descriptive data like mean, freq, etc. This
  data is then saved as 'General_Desc_Stats.csv'.
  ### plots()
  - Here the plots for general data is performed, where data is NOT
  grouped yet. We plot voter information generally, then percentage changes.
  ### group_religion_by_vote()
  - In this function, we use .groupby() on our incoming data by religion,
  keeping only the columns of 2018 and 2022 voter rows. This is plotted.
  ### group_religion_by_percent()
  - This is nearly identical to the previous function but groupby() only
  stratifies by percentage.
  ### def train_model()
  - This is an exploratory function using the scikit-learn module.
  This uses Linear Regression to project how many voters each religious group
  will have in 2028, and generates a line chart to visualize past trends and
  future predictions. Here, we aggregate the data by religion, correct the
  proper calculation for percentages. We create our trained data of X and Y,
  where X is an array of the 2018 and 2022 data that we have. The Y data is
  made by loops through each row (religion) in the Pandas DataFrame (data).

  For model fitting, I used model.fit(X_train, y_train) to draw a straight line
  (trend line) connecting the 2018 voter count and the 2022 voter count.
  The prediction: model.predict(np.array([[2028]])) extends that straight line
  forward to the year 2028 to estimate the new voter count.

  ## test_project.py
  ### sample_data()
  - Mockup sample data to work with.
  ### test_cleaning()
  - In this function, we test our data hygiene pipeline. We insert dummy summary
  rows like "Ignore" or "Total" and verify that they are correctly filtered out,
  voter count columns are properly cast to integer data types, and required
  calculated fields like "Percentage %" are generated.
  ### test_general_stats()
  - In this function, we test the descriptive statistics module. Using monkeypatch
  to isolate file operations, we confirm that the original dataset is returned
  unmodified while successfully exporting summary statistics to General_Desc_Stats.csv.
  ### test_plot_settings()
  - In this function, we verify the plot configuration helper utilities. It ensures
    that chart formatting settings are correctly applied and saved to disk using the
   expected naming pattern (test Voters.png).
  ### test_plots()
  - We validate the end-to-end visualization pipeline. It tests that input data passes
  through unchanged while generating the required output charts for voter counts
  (test No. of voters 2018-2022.png) and percentage distributions (test Percentage %.png).
## Limitations
- With only two data points per group, the projection is a straight line
  through 2018 and 2022 carried forward. It describes a trend in the rolls,
  not a prediction of election results.
- Registered voters are not the population. Rolls can include people who
  have died or emigrated, and registration follows family registry rules.
- The CSVs were entered by hand, so typos are possible.
