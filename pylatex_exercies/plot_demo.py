#! coding: utf-8

from pylatex import Document, Plot, Axis, TikZ


# Define the function to plot
def f(x):
    return x**2


def f2(x):
    return x**3


if __name__ == '__main__':
    # Create a document
    doc = Document()

    # Create an axis object
    axis = Axis()

    # Create a plot object
    plot = Plot(
        name="my_plot",  # Optional name for the plot
        func=f,  # Function to plot
        coordinates=[[x, f(x)] for x in range(1, 11)],
        )

    plot2 = Plot(
        name="my_plot",  # Optional name for the plot
        func=f2,  # Function to plot
        coordinates=[[x, f2(x)] for x in range(1, 11)],
    )

    # Add the plot to the axis
    axis.append(plot)
    axis.append(plot2)

    # Create a TikZ environment to include the axis
    tikz_environment = TikZ()
    tikz_environment.append(axis)

    # Add the TikZ environment to the document
    doc.append(tikz_environment)

    # Build and save the document
    doc.generate_pdf('example_plot', clean_tex=False)