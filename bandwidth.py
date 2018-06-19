#!/usr/bin/env python3

import requests
from getpass import getpass
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt
import common


def plot_average(df, nanopi_names=None, plot_name='average_bandwidth.svg',
                 title='Average Bandwidth by Location', chart_width=10):
    """Produces a bar graph depicting average bandwidth for each nanopi for each direction"""
    averages = df.loc[:, 'bandwidth'].groupby(['nanopi', 'direction']).mean().unstack()
    labels = []
    for nanopi_id in averages.index:
        labels.append(nanopi_names.get(nanopi_id))
    ax = averages.plot(kind='bar')
    ax.set(xlabel='Location', ylabel='Bandwidth (Mbit/s)', title=title)
    if nanopi_names:
        ax.set_xticklabels(labels, rotation=0)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clf()


def plot_24h_average(df, plot_name='24h_average_bandwidth.svg',
                     title="Average Bandwidth by Hour (Aggregate)"):
    """Produces two graphs depicting average aggregate bandwidth for all nanopis by hour of day, up and down"""
    by_hour = df.loc[:, 'bandwidth'].unstack().groupby(by=(lambda x: x[0].hour)).mean()
    ax = by_hour.plot()
    ax.set(xlabel='Hour of Day', ylabel='Bandwidth (Mbit/s)', title=title)
    fig = ax.get_figure()
    fig.savefig(plot_name)
    fig.clf()


def plot_24h(df, nanopi_names=None, plot_name='24h_bandwidth.svg',
             title="Average Bandwidth by Hour (Individual)", chart_width=10):
    """Produces a graph showing the average hourly bandwidth for each individual nanopi"""
    by_hour = df.loc[:, 'bandwidth'].unstack().unstack().groupby(by=(lambda x: x.hour)).mean()
    # up
    ax = by_hour.loc[:, 'up'].plot()
    up_title = title + ' (Up)'
    ax.set(xlabel='Hour of Day', ylabel='Bandwidth (Mbit/s)', title=up_title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_hour.loc[:, 'up'].columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.savefig('up_' + plot_name)
    fig.clf()
    # down
    ax = by_hour.loc[:, 'down'].plot()
    down_title = title + ' (Down)'
    ax.set(xlabel='Hour of Day', ylabel='Bandwidth (Mbit/s)', title=down_title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_hour.loc[:, 'down'].columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.savefig('down_' + plot_name)
    fig.clf()


def plot_dow_average(df, plot_name='dow_average_bandwidth.svg',
                     title="Average Bandwidth by Day of Week (Aggregate)", chart_width=10):
    """Produces a graph showing the average aggregated bandwidth for all nanopis by day of week"""
    by_dow = df.loc[:, 'bandwidth'].unstack().groupby(by=(lambda x: x[0].dayofweek)).mean().reindex(range(7))
    ax = by_dow.plot()
    dows = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ax.set_xticklabels(dows, rotation=0)
    ax.set(xlabel='Day of Week', ylabel='Bandwidth (Mbit/s)', title=title)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig(plot_name)
    fig.clf()


def plot_dow(df, nanopi_names=None, plot_name='dow_bandwidth.svg',
             title="Average Bandwidth by Day of Week (Individual)", chart_width=10):
    """Produces a graph depicting the average individual bandwidth for each nanopi by day of week"""
    by_dow = df.loc[:, 'bandwidth'].unstack().unstack().groupby(by=(lambda x: x.dayofweek)).mean()
    # the _ is not shown because 0th element goes at origin but there is no xtick at origin
    dows = ['_', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # up
    ax = by_dow.loc[:, 'up'].plot()
    ax.set_xticklabels(dows, rotation=0)
    up_title = title + ' (Up)'
    ax.set(xlabel='Day of Week', ylabel='Bandwidth (Mbit/s)', title=up_title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_dow.loc[:, 'up'].columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig('up_' + plot_name)
    fig.clf()
    # down
    ax = by_dow.loc[:, 'down'].plot()
    ax.set_xticklabels(dows, rotation=0)
    down_title = title + ' (Down)'
    ax.set(xlabel='Day of Week', ylabel='Bandwidth (Mbit/s)', title=down_title)
    if nanopi_names:
        labels = []
        for nanopi_id in by_dow.loc[:, 'down'].columns:
            labels.append(nanopi_names.get(nanopi_id))
        ax.legend(labels)
    fig = ax.get_figure()
    fig.set_size_inches(chart_width, 6)
    fig.savefig('down_' + plot_name)
    fig.clf()


if __name__ == '__main__':

    username = input("API Username: ")
    password = getpass(prompt="API Password: ")
    auth = requests.auth.HTTPBasicAuth(username, password)

    nanopis = requests.get(common.NANOPI_URL, auth=auth).json()
    nanopi_names = {nanopi.get('id'):nanopi.get('location_info') for nanopi in nanopis}

    df = common.get_bandwidth_dataframe(auth)
    plot_average(df, nanopi_names=nanopi_names)
    plot_average(df, nanopi_names=nanopi_names)
    plot_24h_average(df)
    plot_24h(df, nanopi_names=nanopi_names)
    plot_dow_average(df)
    plot_dow(df, nanopi_names=nanopi_names)

#    df_wo_demetrios = df.loc[(slice(None), [11, 12, 13, 14, 17], slice(None)), :]
#    plot_average(df_wo_demetrios, nanopi_names, plot_name='average_bandwidth_wo_demetrios.svg',
#                 title='Average Bandwidth by Location (without Demetrios)')
#    plot_24h_average(df_wo_demetrios)
#    plot_24h(df_wo_demetrios, nanopi_names=nanopi_names)
