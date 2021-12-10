# Project selection and Prioritization Tools 
1. Collect all project information necessary to make a selection as shown exemplary in the excel file (IMI2_Projects_Abstacts+Participants.xlsx). It contains information about the name, start date, end data, involved partners and focus of the projects. In order to retrieve additional public information on the projects, one possibility is to use web scraping techniques. Here, we give an example using a Python script (main.py).
Other techniques, such as KNIME worklow can be used to collect this information.
2. Classify the project data based on the content information. This Python script (main.py) searches for a predefined list of disease keywords (fair_ontology.tsv) in the project content text, which subsequently allows to group projects based on the disease keywords. This automated approach is helpful when dealing with a large number of projects, but may not be needed for only a few projects that should be evaluated.
The list of disease keywords can be adapted to fulfill specific needs.
3. Collect specific technical information using a data survey. This is a document containing an example of a [data survey](https://zenodo.org/record/3274230#.YbNVK7nMJgA) that was used to understand the data structure in a given project.
4. Use all project information and apply a score card. In the document [here linked](https://zenodo.org/record/3596024#.YbNVQLnMJgA), projects are scored based on scientific, societal and technical aspects. The total score is used to prioritize the projects. 

