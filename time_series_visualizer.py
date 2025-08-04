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
    
    df_bar = df.copy()
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar = df_bar.groupby(["year","month"]).mean().reset_index()
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
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box["month"] = pd.Categorical(df_box["month"], categories=ordered_months, ordered=True)    
    print(df_box)
    # Draw box plots (using Seaborn)
    flier_properties = dict(marker='d', 
                        markersize=1)


    fig, (ax1, ax2) = plt.subplots(ncols = 2, figsize = (15,5))
    sns.boxplot(data = df_box, 
                x=df_box["year"], 
                y= df_box["value"], 
                ax=ax1,
                palette="tab10",
                flierprops = flier_properties)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")


    sns.boxplot(data = df_box, 
                x=df_box["month"], 
                y= df_box["value"], 
                ax=ax2, 
                palette= "husl",
                flierprops = flier_properties)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_line_plot()
draw_bar_plot()
draw_box_plot()