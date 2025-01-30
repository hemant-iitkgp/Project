import os
import numpy as np
from tabulate import tabulate

def calculate_folder_statistics(labels_to_search, folder_path):
    """
    Calculate the percentage of images in each label group within each folder.

    Args:
    - labels_to_search: A dictionary with label groups and their corresponding labels to search for.
    - folder_path: Path to the folder containing subfolders with images and their corresponding label text files.

    Returns:
    - A dictionary with folder names as keys, and a nested dictionary of label group percentages as values.
    """
    # Convert all labels to lowercase for case-insensitive comparison
    labels_to_search = {
        group: [label.lower() for label in group_labels]
        for group, group_labels in labels_to_search.items()
    }

    folder_statistics = {}

    # Process each folder
    for folder_name in os.listdir(folder_path):
        folder = os.path.join(folder_path, folder_name)

        if os.path.isdir(folder):  # Check if it's a directory
            folder_label_counts = {group: 0 for group in labels_to_search}
            total_images_in_folder = 0

            for image_name in os.listdir(folder):
                # Get the corresponding label file
                label_file = os.path.splitext(image_name)[0] + ".txt"
                label_file_path = os.path.join(folder, label_file)

                if os.path.exists(label_file_path):
                    total_images_in_folder += 1
                    with open(label_file_path, "r") as file:
                        labels = [
                            line.replace("Description:", "").strip().lower()
                            for line in file
                            if line.startswith("Description:")
                        ]

                    # Process label groups
                    for group, group_labels in labels_to_search.items():
                        if any(label in labels for label in group_labels):
                            folder_label_counts[group] += 1

            # Calculate percentages for each label group in the current folder
            folder_percentages = {
                group: (count / total_images_in_folder) * 100
                if total_images_in_folder > 0
                else 0
                for group, count in folder_label_counts.items()
            }

            folder_statistics[folder_name] = folder_percentages
    # print(folder_statistics)
    return folder_statistics



def calculate_label_statistics(labels_to_search, folder_path, total_images):
    """
    Calculate the percentage and standard deviation for each label group in the given folder.

    Args:
    - labels_to_search: A dictionary with label groups and their corresponding labels to search for.
    - folder_path: Path to the folder containing subfolders with images and their corresponding label text files.
    - total_images: Total number of images across all subfolders.

    Returns:
    - A dictionary containing the percentage and standard deviation for each label group and subdistricts.
    """
    # Convert all labels to lowercase for case-insensitive comparison
    labels_to_search = {
        group: [label.lower() for label in group_labels]
        for group, group_labels in labels_to_search.items()
    }

    # Initialize dictionaries for counts
    label_counts = {group: 0 for group in labels_to_search}
    subdistrict_counts = {group: 0 for group in labels_to_search}
    subdistrict_label_occurrences = {group: [] for group in labels_to_search}

    # List to store binary occurrences for standard deviation calculations
    image_label_occurrences = []

    # Process each folder
    for folder_name in os.listdir(folder_path):
        folder = os.path.join(folder_path, folder_name)

        if os.path.isdir(folder):  # Check if it's a directory
            folder_label_found = {group: 0 for group in labels_to_search}

            for image_name in os.listdir(folder):
                # Get the corresponding label file
                label_file = os.path.splitext(image_name)[0] + ".txt"
                label_file_path = os.path.join(folder, label_file)

                if os.path.exists(label_file_path):
                    with open(label_file_path, "r") as file:
                        labels = [
                            line.replace("Description:", "").strip().lower()
                            for line in file
                            if line.startswith("Description:")
                        ]

                    # Process label groups
                    label_found = []
                    for group, group_labels in labels_to_search.items():
                        if any(label in labels for label in group_labels):
                            label_counts[group] += 1
                            folder_label_found[group] = 1
                            label_found.append(1)  # Binary indicator
                        else:
                            label_found.append(0)

                    # Append label presence for standard deviation calculation
                    image_label_occurrences.append(label_found)

            # Count folder-level occurrences
            for group in folder_label_found:
                subdistrict_label_occurrences[group].append(folder_label_found[group])
                if folder_label_found[group]:
                    subdistrict_counts[group] += 1

    # Calculate statistics
    results = {}
    for group, count in label_counts.items():
        percentage = (count / total_images) * 100

        # Get binary presence array for images
        group_index = list(labels_to_search.keys()).index(group)
        label_presence = [image[group_index] for image in image_label_occurrences]
        std_dev = np.std(label_presence)

        # Calculate subdistrict statistics
        subdistrict_percentage = (
            subdistrict_counts[group] / len(os.listdir(folder_path)) * 100
        )
        subdistrict_std_dev = np.std(subdistrict_label_occurrences[group])

        results[group] = {
            "label_percentage": percentage,
            "label_std_dev": std_dev,
            "subdistrict_percentage": subdistrict_percentage,
            "subdistrict_std_dev": subdistrict_std_dev,
        }

    return results

# def save_results_to_file(results, folder_statistics, output_file_path):
#     """
#     Save the results to a text file in tabular form.

#     Args:
#     - results: The results dictionary containing percentage and standard deviation for each label group.
#     - folder_statistics: Folder-level label group percentages.
#     - output_file_path: The path to save the results.
#     """
#     # Prepare the data for the first table
#     table_data = [
#         [
#             group,
#             f"{result['label_percentage']:.2f}%",
#             f"{result['label_std_dev']*100:.2f}%",
#             f"{result['subdistrict_percentage']:.2f}%",
#             f"{result['subdistrict_std_dev']*100:.2f}%",
#         ]
#         for group, result in results.items()
#     ]

#     headers = [
#         "Label Group",
#         "Label Percentage (%)",
#         "Label Std Dev (%)",
#         "Subdistrict Percentage (%)",
#         "Subdistrict Std Dev (%)",
#     ]

#     # Generate the first table
#     table = tabulate(table_data, headers=headers, tablefmt="grid")

#     # Prepare the data for the second table
#     folder_table_data = []
#     for folder, percentages in folder_statistics.items():
#         row = [folder] + [f"{percentages[group]:.2f}%" for group in results.keys()]
#         folder_table_data.append(row)

#     folder_headers = ["Folder"] + list(results.keys())

#     # Generate the second table
#     folder_table = tabulate(folder_table_data, headers=folder_headers, tablefmt="grid")

#     with open(output_file_path, "w") as output_file:
#         output_file.write("Overall Statistics:\n")
#         output_file.write(table + "\n\n")
#         output_file.write("Folder-Level Statistics:\n")
#         output_file.write(folder_table)

#     print(f"Results saved to {output_file_path}")


def save_results_to_file(results, folder_statistics, tertile_results, output_file_path):
    """
    Save the results to a text file in tabular form, including tertile analysis.

    Args:
    - results: The results dictionary containing percentage and standard deviation for each label group.
    - folder_statistics: Folder-level label group percentages.
    - tertile_results: Tertile analysis results for each label group.
    - output_file_path: The path to save the results.
    """
    # Prepare the data for the first table
    table_data = [
        [
            group,
            f"{result['label_percentage']:.2f}%",
            f"{result['label_std_dev']*100:.2f}%",
            f"{result['subdistrict_percentage']:.2f}%",
            f"{result['subdistrict_std_dev']*100:.2f}%",
        ]
        for group, result in results.items()
    ]

    headers = [
        "Label Group",
        "Label Percentage (%)",
        "Label Std Dev (%)",
        "Subdistrict Percentage (%)",
        "Subdistrict Std Dev (%)",
    ]

    # Generate the first table
    table = tabulate(table_data, headers=headers, tablefmt="grid")

    # Prepare the data for the second table
    folder_table_data = []
    for folder, percentages in folder_statistics.items():
        row = [folder] + [f"{percentages[group]:.2f}%" for group in results.keys()]
        folder_table_data.append(row)

    folder_headers = ["Folder"] + list(results.keys())

    # Generate the second table
    folder_table = tabulate(folder_table_data, headers=folder_headers, tablefmt="grid")

    # Prepare the data for the tertiles table
    tertile_table_data = []
    for group, tertile_info in tertile_results.items():
        for tertile, (folders, percentage_range, mean) in tertile_info.items():
            tertile_table_data.append(
                [
                    group,
                    tertile.capitalize(),
                    ", ".join(folders),
                    f"{percentage_range[0]:.2f}% - {percentage_range[1]:.2f}%",
                    f"{mean:.2f}%",
                ]
            )

    tertile_headers = ["Label Group", "Tertile", "Subdistricts", "Range (%)", "Mean (%)"]

    # Generate the tertiles table
    tertile_table = tabulate(tertile_table_data, headers=tertile_headers, tablefmt="grid")

    with open(output_file_path, "w") as output_file:
        output_file.write("Overall Statistics:\n")
        output_file.write(table + "\n\n")
        output_file.write("Folder-Level Statistics:\n")
        output_file.write(folder_table + "\n\n")
        output_file.write("Tertile Analysis:\n")
        output_file.write(tertile_table)

    print(f"Results saved to {output_file_path}")



def calculate_tertiles(folder_statistics, labels_to_search):
    """
    Divide subdistricts (folders) into tertiles (highest, medium, and lowest percentages) 
    for each label group.

    Args:
    - folder_statistics: Dictionary with folder names as keys and label group percentages as values.
    - labels_to_search: A dictionary with label groups and their corresponding labels.

    Returns:
    - A dictionary with tertile information for each label group, including folder names, range, and mean.
    """
    tertile_results = {}

    for group in labels_to_search.keys():
        # Extract percentages for the current label group
        group_percentages = [
            (folder, percentages[group]) for folder, percentages in folder_statistics.items()
        ]
        # Sort folders by percentage in descending order
        sorted_folders = sorted(group_percentages, key=lambda x: x[1], reverse=True)

        # Divide into tertiles
        total_folders = len(sorted_folders)
        tertile_size = total_folders // 3

        highest = sorted_folders[:tertile_size]
        medium = sorted_folders[tertile_size:2 * tertile_size]
        lowest = sorted_folders[2 * tertile_size:]

        # Helper function to calculate range and mean
        def calculate_stats(tertile):
            percentages = [item[1] for item in tertile]
            folder_names = [item[0] for item in tertile]
            if percentages:
                percentage_range = (min(percentages), max(percentages))
                mean_percentage = sum(percentages) / len(percentages)
            else:
                percentage_range = (0, 0)
                mean_percentage = 0
            return folder_names, percentage_range, mean_percentage

        tertile_results[group] = {
            "highest": calculate_stats(highest),
            "medium": calculate_stats(medium),
            "lowest": calculate_stats(lowest),
        }

    return tertile_results
# Example Usage
labels_to_search = {
    "Transportation": [
        "Transportation", "Transit system", "Logistics", "Public transportation", "Highway", 
        "Railway", "Airport", "Harbor", "Shipping port", "Cargo transportation", "Freight", 
        "Urban transportation", "Subway", "Train", "Metro", "Bus station", "Bus", "Shipping container", 
        "Cargo ship", "Airplane", "Road network", "Bridge", "Tunnel", "Bicycle lane", "Pedestrian crossing", 
        "High-speed rail", "Electric vehicle", "Autonomous vehicle", "Traffic flow", "Mass transit", 
        "Cityscape", "Commuter train", "Ferry", "Truck", "Interstate", "Cargo truck", "Transportation hub", 
        "Distribution center", "Transport infrastructure", "Railroad track", "Logistics center", 
        "Shipping logistics", "Global trade", "Supply chain", "Urban mobility", "Transport network", 
        "Freight train", "Shipping industry", "Efficient transportation", "Modern transit", "Sustainable transportation"
    ],
    "Nature":  [
        "Nature", "Greenery", "Grassland", "Meadow", "Park", "Forest", "Lush vegetation", 
        "Healthy environment", "Eco-friendly", "Sustainable living", "Flora", "Wildlife", "Countryside", 
        "Open field", "Landscape", "Scenic view", "Fresh air", "Peaceful environment", "Clean environment", 
        "Outdoor recreation", "Garden", "Botanical garden", "Trees", "Flowers", "Natural beauty", 
        "Hiking trail", "Healthy lifestyle", "Serene atmosphere", "Blue sky", "Mountain range", "River", 
        "Lake", "Pasture", "Rolling hills", "Agriculture", "Orchard", "Vegetation", "Grass", "Shrubs", "Pond", 
        "Clean water", "Rural area", "Biodiversity", "Picnic spot", "Tranquility"
    ],
    "Poverty":  ["Poverty","Slum","Homelessness","Refugee","Urban decay","Underprivileged","Economic disparity","Shantytown",
    "Makeshift shelter","Dirt floor","Crowded living conditions","Rural area","Low-income housing","Substandard living",
    "Begging","Hunger","Malnutrition","Child labor","Barefoot","Dirty clothes","Hardship","Struggle","Neediness","Unemployment",
    "Inequality","Developing country","Charitable help","Relief efforts","Crisis","Flooded area","Drought",
    "Natural disaster aftermath","War-torn area","Worn-out clothes","Broken furniture","Cardboard box","Open fire","Debris",
    "Trash heap","Old tires"
]
}


folder_path = "images"  # Replace with your actual path
total_images = 480  # Update based on your dataset

results = calculate_label_statistics(labels_to_search, folder_path, total_images)
folder_statistics = calculate_folder_statistics(labels_to_search, folder_path)
tertile_results = calculate_tertiles(folder_statistics, labels_to_search)
output_file_path = "results.txt"
save_results_to_file(results, folder_statistics, tertile_results, output_file_path)
# print(tertile_results)