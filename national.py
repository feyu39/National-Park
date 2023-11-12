import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def process_species_data():
    # Read in the species data to analyze
    species_data = pd.read_csv("species.csv")
    conservation_status_data = species_data['Conservation Status']

    # Get total threatened species for each park, grouped by park
    threatened_status = conservation_status_data.isin(
        ['Endangered', 'Threatened', 'Under Review', 'Species of Concern', 'In Recovery'])
    threatened_species_count = species_data[threatened_status].groupby(
        'Park Name').size()

    # Calculate the ratio of threatened species per park
    total_species_count_per_park = species_data.groupby('Park Name').size()
    threatened_ratio = threatened_species_count / total_species_count_per_park
    # Convert to a percentage, rounded to 2 decimal places
    threatened_percentage = (threatened_ratio * 100).round(2)
    # Convert to a data frame for seaborn bar plot
    threatened_percentage_df = threatened_percentage.reset_index(
        name="Percentage of Threatened Species")
    # Get the mean of all parks threatened percentage
    mean_threatened_percentage = (threatened_percentage.mean()).round(2)
    print("Finished data processing!")

    return (mean_threatened_percentage, threatened_percentage_df)


def graph_species_data(mean_threatened_percentage, threatened_percentage_df):
    # Set size of the plot to be larger
    plt.figure(figsize=(10, 16))

    # Adjust location of plot
    plt.subplots_adjust(left=0.2, bottom=0.053, right=0.902,
                        top=0.952, wspace=0.2, hspace=0.2)

    # Pick color scheme: blue if normal, orange if above the mean
    graph_colors = ['#4895ef' if float(value) <
                    mean_threatened_percentage else '#ff4122' for value in threatened_percentage_df['Percentage of Threatened Species']]

    # Plot ratio of threatened species to total species within each park
    graph = sns.barplot(threatened_percentage_df, x="Percentage of Threatened Species",
                        y="Park Name", palette=graph_colors)
    # Plot the mean percentage as a line for reference
    graph.axvline(mean_threatened_percentage, color='green',
                  linestyle='--', label=f'Mean: {mean_threatened_percentage}')

    # Get current x-axis labels
    labels = [item.get_text() for item in graph.get_yticklabels()]
    # Remove national park from abbreviation
    shortened_labels = [label.split(' National')[0] for label in labels]
    # Set x-axis labels again
    graph.set_yticklabels(shortened_labels)
    # Show the legend for the mean percentage
    graph.legend()
    plt.show()
    print("Finished plotting plot!")


def main():
    print("Beginning data processing...")
    processed_species_data = process_species_data()
    graph_species_data(processed_species_data[0], processed_species_data[1])


if __name__ == "__main__":
    main()
