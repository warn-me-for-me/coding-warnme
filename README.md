# Inter-Annotator Agreement (IAA.ipynb)

This Jupyter Notebook is designed to perform interannotator agreement analysis on a dataset of coded annotations, specifically emergency alert emails as a part of Clery Act compliance. It calculates Fleiss' kappa, a statistical measure for assessing the reliability of agreement between multiple annotators, and selects the highest agreement codes for each data point.

## Features

- Calculates Fleiss' kappa for a given set of columns (annotators) in a DataFrame.
- Selects the highest agreement code and optionally the second highest agreement code for each item/document.
- Provides utility functions for grouping columns by annotator, getting unique codes, and more.

## Usage

1. Import the necessary Python libraries and utility functions.
2. Load the dataset into a Pandas DataFrame.
3. Specify the columns (annotators) for which you want to calculate Fleiss' kappa.
4. Calculate Fleiss' kappa using the `calculate_fleiss_kappa` function.
5. Select the highest agreement codes using the `select_highest_agreement_code` function.

# Coded Document Analysis (analysis.ipynb)
This Jupyter Notebook analyzes the coded documents by looking at a case study of a particular regex phrase as well as some basic quantitative frequency analysis. It relies on the CSV output of ```IAA.ipynb```.

## Features
- Complete soon. 

## Usage 
1. Import the necessary Python libraries and utility functions.
2. Load the dataset into a Pandas DataFrame.
3. Complete soon. 

## Dependencies

```pandas```,```numpy```,```sklearn```,```itertools```,```pathlib```

## References

- Aprilliant, A. 2021. [Cohen’s Kappa and Fleiss’ Kappa— How to Measure the Agreement Between Raters](https://audhiaprilliant.medium.com/cohens-kappa-and-fleiss-kappa-how-to-measure-the-agreement-between-raters-9ec12edef121)
- Kraemer, H. C. 1980. [Extension of the kappa coefficient](https://pubmed.ncbi.nlm.nih.gov/7190852/). Biometrics, 36(2), 207–16.
