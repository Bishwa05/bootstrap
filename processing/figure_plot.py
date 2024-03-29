#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 17:20:54 2019

@author: i501895
"""
import chart_studio.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go

def plotRevenueRecency(tx_user):
    tx_graph = tx_user.query("Revenue < 50000 and Frequency < 2000")
    plot_data = [
        go.Scatter(
            x=tx_graph.query("Segment == 'Low-Value'")['Recency'],
            y=tx_graph.query("Segment == 'Low-Value'")['Revenue'],
            mode='markers',
            name='Low',
            marker= dict(size= 7,
                line= dict(width=1),
                color= 'blue',
                opacity= 0.8
               )
        ),
            go.Scatter(
            x=tx_graph.query("Segment == 'Mid-Value'")['Recency'],
            y=tx_graph.query("Segment == 'Mid-Value'")['Revenue'],
            mode='markers',
            name='Mid',
            marker= dict(size= 9,
                line= dict(width=1),
                color= 'green',
                opacity= 0.5
               )
        ),
            go.Scatter(
            x=tx_graph.query("Segment == 'High-Value'")['Recency'],
            y=tx_graph.query("Segment == 'High-Value'")['Revenue'],
            mode='markers',
            name='High',
            marker= dict(size= 11,
                line= dict(width=1),
                color= 'red',
                opacity= 0.9
               )
        ),
    ]
    plot_layout = go.Layout(
            yaxis= {'title': "Revenue"},
            xaxis= {'title': "Recency"},
            title='Segments'
        )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    plot(fig)
    

def plotRecencyFrequency(tx_user):
    tx_graph = tx_user.query("Revenue < 50000 and Frequency < 2000")
    plot_data = [
        go.Scatter(
            x=tx_graph.query("Segment == 'Low-Value'")['Recency'],
            y=tx_graph.query("Segment == 'Low-Value'")['Frequency'],
            mode='markers',
            name='Low',
            marker= dict(size= 7,
                line= dict(width=1),
                color= 'blue',
                opacity= 0.8
               )
    ),
        go.Scatter(
        x=tx_graph.query("Segment == 'Mid-Value'")['Recency'],
        y=tx_graph.query("Segment == 'Mid-Value'")['Frequency'],
        mode='markers',
        name='Mid',
        marker= dict(size= 9,
            line= dict(width=1),
            color= 'green',
            opacity= 0.5
           )
    ),
        go.Scatter(
        x=tx_graph.query("Segment == 'High-Value'")['Recency'],
        y=tx_graph.query("Segment == 'High-Value'")['Frequency'],
        mode='markers',
        name='High',
        marker= dict(size= 11,
            line= dict(width=1),
            color= 'red',
            opacity= 0.9
           )
    ),
    ]
    plot_layout = go.Layout(
        yaxis= {'title': "Frequency"},
        xaxis= {'title': "Recency"},
        title='Segments'
    )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    plot(fig)

def plotRevenueFrequency(tx_user):
    tx_graph = tx_user.query("Revenue < 50000 and Frequency < 2000")
    plot_data = [
    go.Scatter(
        x=tx_graph.query("Segment == 'Low-Value'")['Frequency'],
        y=tx_graph.query("Segment == 'Low-Value'")['Revenue'],
        mode='markers',
        name='Low',
        marker= dict(size= 7,
            line= dict(width=1),
            color= 'blue',
            opacity= 0.8
           )
    ),
        go.Scatter(
        x=tx_graph.query("Segment == 'Mid-Value'")['Frequency'],
        y=tx_graph.query("Segment == 'Mid-Value'")['Revenue'],
        mode='markers',
        name='Mid',
        marker= dict(size= 9,
            line= dict(width=1),
            color= 'green',
            opacity= 0.5
           )
    ),
        go.Scatter(
        x=tx_graph.query("Segment == 'High-Value'")['Frequency'],
        y=tx_graph.query("Segment == 'High-Value'")['Revenue'],
        mode='markers',
        name='High',
        marker= dict(size= 11,
            line= dict(width=1),
            color= 'red',
            opacity= 0.9
           )
    ),
    ]
    plot_layout = go.Layout(
        yaxis= {'title': "Revenue"},
        xaxis= {'title': "Frequency"},
        title='Segments'
    )
    fig = go.Figure(data=plot_data, layout=plot_layout)
    plot(fig)
