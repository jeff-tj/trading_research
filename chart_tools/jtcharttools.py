import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import math

def chart_mean_sd(data_df, period, h_width=0.25):
    """Plots the current data with indication of range, mean and sd

    Parameters
    ----------
    data_df : the data supplied as a pandas df with date index
    period : the period over which to calc stats
    h_width : parameter to change horizontal width of bar

    Returns
    -------
    fig : a chart object
    stats_df : summary of the different stats
    """

    temp_df = data_df.sort_index(ascending=False)[:period]
    stats = ["last", "max", "min", "ave", "ave-2sd", "ave+2sd"] #stats calc'd

    # Calc the stats output
    last = temp_df.iloc[0] #Latest data
    max_px = np.max(temp_df, axis=0)
    min_px = np.min(temp_df, axis=0)
    av_px = np.mean(temp_df, axis=0)
    sd_px = np.std(temp_df, axis=0)
    lr_px = av_px - 2 * sd_px
    hr_px = av_px + 2 * sd_px

    stats_df = pd.concat([last, max_px, min_px, av_px, lr_px, hr_px], axis=1)
    stats_df.columns = stats

    # Set up the plot
    x_labels = list(last.index.values) #Need to convert categroical to numeric range
    x_rng = range(len(x_labels))
    # Create the figure
    fig, ax = plt.subplots()

    # Plot the last data points
    ax.plot(x_rng, last.values, marker="o")

    # Plot the min-max ranges
    ax.vlines(x_rng, min_px, max_px)

    # Plot the horizontal bars (h_width used here)
    h_elems = [av_px, lr_px, hr_px] #Neater way to do this?
    x_low = [x - 0.5*h_width for x in x_rng]
    x_high = [x + 0.5*h_width for x in x_rng]
    for elem in h_elems:
        ax.hlines(elem, x_low, x_high)

    plt.xticks(x_rng, x_labels) #Remap back to numerical

    return fig, stats_df

def sfe_date(year, month):
    """Works out the SFE date - the Thu before second Fri

    Parameters
    ----------
    year - the year
    month - a number from 1-12 representing the month

    Returns
    -------
    sfe_date - returns the SFE date for the month, if not quarter returns
    the next sfe date
    """

    # Work out the month required
    sfe_month = math.ceil((month/12.0)*4) * 3

    # First day of the month
    first_day = date(year, sfe_month, 1)

    # Work out Thu before 2nd Fri
    day_week = first_day.weekday()
    if day_week <= 4:
        sfe_thu = (4 - day_week) + 7
    else:
        sfe_thu = (11 - day_week) + 7

    return date(year, sfe_month, sfe_thu)

def imm_date(year, month):
    """Works out the IMM date - 3rd Wed

    Parameters
    ----------
    year - the year
    month - a number from 1-12 representing the month

    Returns
    -------
    imm_date - returns the IMM date for the month, if not quarter returns
    the next sfe date
    """

    # Work out the month required
    imm_month = math.ceil((month/12.0)*4) * 3

    # First day of the month
    first_day = date(year, imm_month, 1)

    # Work out Thu before 2nd Fri
    day_week = first_day.weekday()
    if day_week <= 4:
        imm_wed = (2 - day_week) + 15
    else:
        imm_wed = (9 - day_week) + 15

    return date(year, imm_month, imm_wed)
