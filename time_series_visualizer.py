import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
months=['January','February','March','April','May','June','July','August','September','October','November','December']
months_abv =['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]

# Clean data
print(df.count(numeric_only=True))
def draw_line_plot():
    # Draw line plot
    fig, axs = plt.subplots(figsize=(20, 10))
    plt.plot(df.index, df["value"], linewidth=1, color='blue')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    df_bar['month'] = df.index.month
    df_bar['year'] = df.index.year
    df_bar = df_bar.groupby(["year", "month"])['value'].mean()
    df_bar = df_bar.unstack()
    # Draw bar plot
    plt.style.use('tableau-colorblind10')
    fig = df_bar.plot(kind="bar", legend=True, figsize=(15, 10)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(labels = months)
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # %b is the shorten version of month names
    # Draw box plots (using Seaborn)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))
    fig.set_figwidth(20)
    fig.set_figheight(10)

    ax1 = plt.subplot(1,2,1)
    sns.boxplot(x=df_box['year'], y=df_box['value'])
    ax1.set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")


    ax2 = plt.subplot(1,2,2)
    sns.boxplot(x=df_box['month'], y=df_box['value'], order=months_abv)
    ax2.set(xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
