import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fallPatentNumberGraph(ax, authority):
    # Load the data from the provided Excel file
    file_path = f'./data/{authority} 专利数量.xlsx'
    data = pd.read_excel(file_path)

    # Calculate the differences from the first year to the next years as increments
    data['增量'] = data['专利数量'].diff().fillna(data['专利数量'].iloc[0])

    # Starting point for each bar is the previous bar's ending point
    starting_points = [0]
    for increment in data['增量'].iloc[:-1]:
        starting_points.append(starting_points[-1] + increment)

    # Define colors for the bars
    colors = ['#599cb4' if inc < 0 else '#ef797e' for inc in data['增量']]

    # Plot bars
    for idx, (year, inc) in enumerate(zip(data['申请年份'], data['增量'])):
        ax.bar(year, inc, bottom=starting_points[idx], color=colors[idx])
        # Connect bars with a line
        if idx > 0:
            ax.plot([data['申请年份'][idx-1], data['申请年份'][idx]], [starting_points[idx], starting_points[idx]],
                        linestyle=':', linewidth=1, color='gray')
    # Annotate values at the top of the increase bars and at the bottom of the decrease bars (adjusted)
    for idx, (year, inc) in enumerate(zip(data['申请年份'], data['增量'])):
        if inc > 0:  # Increment is positive
            label_position = starting_points[idx] + inc + 0.5
            va = 'bottom'
        else:  # Increment is negative
            label_position = starting_points[idx] + inc - 0.5 # Adjusted to bottom of the bar
            va = 'top'
        # Add the text annotation
        ax.text(year, label_position, f'{int(inc)}', ha='center', va=va, color='black', fontsize=13)

    # Set the plot title and labels
    ax.set_title(f'{authority}', fontsize=15, pad=30)

    # Set x-axis ticks to display each year
    ax.set_xticks(data['申请年份'])

    # Remove all spines
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Remove x and y ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)

    # Hide the y-axis labels and only show the gridlines
    ax.set_yticklabels([])

    # Rotate x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)

def PatentNumber():
    # Create a 2x2 grid of subplots with increased horizontal and vertical spacing
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True)
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0,
                        wspace=0.1,hspace=0.5)
    # Call the fallgraph function for each authority and pass the corresponding axis
    fallPatentNumberGraph(axs[0, 0], "China")
    fallPatentNumberGraph(axs[0, 1], "United States")
    fallPatentNumberGraph(axs[1, 0], "Europe")
    fallPatentNumberGraph(axs[1, 1], "Russia")

    # Set common x and y labels
    #fig.text(0.5, 0.04, 'Year', ha='center', fontsize=14)
    #fig.text(0.04, 0.5, 'Patent Number', va='center', rotation='vertical', fontsize=14)

    # Adjust layout
    plt.tight_layout()

    # Save and show the plot
    plt.savefig("./fall/Four_Authorities_Number.png")
    #plt.show()
    

def fallINPADOCNumberGraph(ax, authority):
    # Load the data from the provided Excel file
    file_path = f'./data/{authority} 同族.xlsx'
    data = pd.read_excel(file_path)

    # Calculate the differences from the first year to the next years as increments
    data['增量'] = data['INPADOC同族专利申请数量'].diff().fillna(data['INPADOC同族专利申请数量'].iloc[0])

    # Starting point for each bar is the previous bar's ending point
    starting_points = [0]
    for increment in data['增量'].iloc[:-1]:
        starting_points.append(starting_points[-1] + increment)

    # Define colors for the bars
    colors = ['#8cd0c3' if inc < 0 else '#ba7fb5' for inc in data['增量']]

    # Plot bars
    for idx, (year, inc) in enumerate(zip(data['Year'], data['增量'])):
        ax.bar(year, inc, bottom=starting_points[idx], color=colors[idx])
        # Connect bars with a line
        if idx > 0:
            ax.plot([data['Year'][idx-1], data['Year'][idx]], [starting_points[idx], starting_points[idx]],
                        linestyle=':', linewidth=1, color='gray')
    # Annotate values at the top of the increase bars and at the bottom of the decrease bars (adjusted)
    for idx, (year, inc) in enumerate(zip(data['Year'], data['增量'])):
        if inc > 0:  # Increment is positive
            label_position = starting_points[idx] + inc + 0.5
            va = 'bottom'
        else:  # Increment is negative
            label_position = starting_points[idx] + inc - 0.5 # Adjusted to bottom of the bar
            va = 'top'
        # Add the text annotation
        ax.text(year, label_position, f'{int(inc)}', ha='center', va=va, color='black', fontsize=13)

    # Set the plot title and labels
    ax.set_title(f'{authority}', fontsize=15, pad=30)

    # Set x-axis ticks to display each year
    ax.set_xticks(data['Year'])

    # Remove all spines
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Remove x and y ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)

    # Hide the y-axis labels and only show the gridlines
    ax.set_yticklabels([])

    # Rotate x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)

def INPADOCNumber():
    # Create a 2x2 grid of subplots with increased horizontal and vertical spacing
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True)
    fig.subplots_adjust(left=0,right=1,top=1,bottom=0,
                        wspace=0.1,hspace=0.5)
    # Call the fallgraph function for each authority and pass the corresponding axis
    fallINPADOCNumberGraph(axs[0, 0], "China")
    fallINPADOCNumberGraph(axs[0, 1], "United States")
    fallINPADOCNumberGraph(axs[1, 0], "Europe")
    fallINPADOCNumberGraph(axs[1, 1], "Russia")

    # Set common x and y labels
    #fig.text(0.5, 0.04, 'Year', ha='center', fontsize=14)
    #fig.text(0.04, 0.5, 'Patent Number', va='center', rotation='vertical', fontsize=14)

    # Adjust layout
    plt.tight_layout()

    # Save and show the plot
    plt.savefig("./fall/Four_Authorities_INPADOOC.png")
    #plt.show()

PatentNumber()
INPADOCNumber()