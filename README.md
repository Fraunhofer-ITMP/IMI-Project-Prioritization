# Project selection and Prioritization Tools 

## Process overview
1. Collect all project information necessary to make a selection as shown exemplary in the [excel file](data/IMI2_Projects_Abstracts.xlsx). It contains information about the name, start date, end data, involved partners, and focus of the projects. In order to retrieve additional public information on the projects, one possibility is to use web scraping techniques. Here, we give an example using a [Python script](src/scrapper.py). Other techniques, such as KNIME workflow can be used to collect this information.
2. Classify the project data based on the content information. This [Python script](src/fair_vocab_mapping.py) searches for a predefined list of disease keywords (present in the [ontology file](data/fair_ontology)) in the project content text, which subsequently allows grouping projects based on the disease keywords. This automated approach is helpful when dealing with large number of projects, but may not be needed for evaluating a few projects. The list of disease keywords can be adapted to fulfill specific needs.
3. Collect specific technical information using a data survey. This is a document containing an example of a [data survey](https://zenodo.org/record/3274230#.YbNVK7nMJgA) that was used to understand the data structure in a given project.
4. Use all project information and apply a score card. In this [document](https://zenodo.org/record/3596024#.YbNVQLnMJgA), projects are scored based on scientific, societal, and technical aspects. The total score is used to prioritize the projects. 


## Running the script
- Clone the GitHub repository locally using the following command in your terminal:
```
git clone https://github.com/Fraunhofer-ITMP/IMI-Project-Prioritization
```
Alternatively, you can also use [GitHub Desktop](https://desktop.github.com/) to clone the repository.

- Go to the location of your cloned local repository via the terminal and get into the IMI-Project-Prioritization folder using the following command:
```python
cd IMI-Project-Prioritization
```
-  Create a virtual environment. If you are using conda, you can use the following commands:
```python
conda create --name virtualenv python=3.9
```
Activate your virtual env:
```python
conda activate virtualenv
```
- Install all the requirements into your virtual environment:
```python
pip install -r requirements.txt
```
Additional, ensure that you install the following manually:
1. en_core_sci_md model based on the installation shown [here](https://github.com/allenai/scispacy).
1. [chromedriver](https://chromedriver.chromium.org/downloads) based on your Google Chrome version and change the path to the executable file in [constants.py](src/constants.py).

For Linux and Mac users, an additional step to add chromedriver to the path has to be done using the following command in your terminal:
   ```
   mv chromedriver /usr/local/bin
   ```
For Mac user, be sure to authorize the execution of the binary in the System -> Preferences -> Security&Privacy -> General Tab
- Run the [main.py](src/main.py) file from the python terminal as follows:
```python
python src/main.py
```
