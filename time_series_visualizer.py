import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import warnings
warnings.filterwarnings('ignore')

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col= ["date"], parse_dates=["date"])

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025))&
        (df["value"] <= df["value"].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig,ax = plt.subplots()
    ax.plot(df.index,df["value"], color= "darkred")
    ax.set_xlabel('Date' , fontsize = 20)
    ax.set_ylabel('Page Views', fontsize = 20)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize = 25)
    ax.set_xticklabels(ax.get_xmajorticklabels(),fontsize=15)
    ax.set_yticklabels(ax.get_ymajorticklabels(),fontsize=15)
    fig.set_figwidth(24)
    fig.set_figheight(8)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    df["year"] = df.index.year
    df["month"] = df.index.month
    df_bar = df.groupby(["year","month"]).mean().reset_index()
    df_bar["month"] = pd.to_datetime(df_bar["month"],format='%m').dt.month_name()
    df_bar["month"] = pd.Categorical(df_bar["month"], categories=ordered_months, ordered=True)
    df_bar = df_bar.pivot(index = "year", columns="month", values = "value")
    print(df_bar)
    
    # Draw bar plot
    ax = df_bar.plot.bar(stacked=False, figsize=(8, 6), grid=False)
    fig = ax.get_figure()
    plt.ylabel('Average Page Views')
    plt.xlabel('Years')
    plt.tight_layout()
    plt.legend(title="Month") 

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

#draw_line_plot()
draw_bar_plot()