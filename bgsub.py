import csv
import os
import sys
from collections import namedtuple
from matplotlib import pyplot as plt
import re

DEFAULT_PATH = "/home/danielle/Documents/LMCE"

SpectrumData = namedtuple("SpectrumData", ['X', 'Y', 'info'])

def load_file(filename):
    """Loads file from directory ** needs input to be a fully qualified file path
    Returns a new list of tuples (x,y) containing points where x = wavenums and y = intensities"""

    data = None

    if filename.endswith(".txt"):

        # Read in files row by row
        with open(filename, 'r') as csvfile:
            numreader = csv.reader(csvfile, delimiter='\t')
            curr_wavenums = []
            curr_intens = []
            for row in numreader:
                curr_wavenums.append(float(row[0]))
                curr_intens.append(float(row[1]))

            # Create a list of points (x,y) where x = wavenumbers and y = intensities
            data = zip(curr_wavenums, curr_intens)

    # Find bigX and bigY in the file name, append them to SpectrumData object
    matches = re.findall('[+-]?[XY]_.[0-9]+\.[0-9]+', filename)

    X = None
    Y = None

    for match in matches:
        if "X_" in match:
            X = match

        if "Y_" in match:
            Y = match

    return SpectrumData(X, Y, data)

def filter_negative(data):
    """Filters out negative data from spectrum data
    Returns original data without negative values"""
    # return [elem for elem in data if elem > 0]
    return SpectrumData(data.X, data.Y, [elem for elem in data.info if elem > 0])

def plot_spectrum(data):
    """Creates x-y scatter plot of the spectrum data"""
    plt.scatter(*zip(*data))
    plt.show()

def bg_subtract(data):
    """Returns background subtracted data set"""
    # TODO: from the horizontal line slider
    for i in range(len(data.info)):
        y_val = data.info[i][1]
        for j in range(i + 1, len(data.info)):
            if y_val == data.info[j][1]:
                return [(x, y - y_val) for x, y in data.info]
    min_y = min(data.info, key=lambda tup: tup[1])[1]
    return SpectrumData(data.X, data.Y, [(x, y - min_y) for x, y in data.info])

def trapezoidal_sum(data):
    """Calculates the area under the curve by trapezoidal method
    Two adjacent points in the data set are used to create a trapezoid and calculate its area
    Continues for all other points in the set and sums areas together,
    returning total area"""
    # TODO: check if points are within user inputted range
    total_area = 0

    # Iterates over all points in data set
    for index in range(len(data.info)-1):

        # Next adjacent point to current point
        next_point = data.info[index + 1]

        # Change in x between the points
        dx = next_point.info[0] - data.info[index][0]
        r_y = data.info[index][1]
        t_y = next_point.info[1] - r_y

        # Area of current trapezoid
        area = (r_y * dx) + (0.5 * dx * t_y)
        total_area += area

    return total_area

def specific_peak(w_num1, w_num2, data):

    culled_data = []

    for point in data.info:
        if w_num1 <= point[0] <= w_num2:
            culled_data.append(point)

def create_heatmap():
    pass

def main(path):
    file_list = sorted(os.listdir(path))
    os.chdir(path)
    spectra = []
    for each in file_list:
        print(each)
        spectrum = load_file(each)
        spectrum.info.sort(key=lambda tup: tup[0])
        spectrum = filter_negative(spectrum.info)
        spectrum = bg_subtract(spectrum.info)
        spectra.append(spectrum)
    plot_spectrum(spectra[-1])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH)