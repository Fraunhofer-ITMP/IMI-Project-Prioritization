# Project selection and Prioritization Tools 

## Process overview
1. Collect all project information necessary to make a selection as shown exemplary in the [excel file](data/IMI2_Projects_Abstracts.xlsx). It contains information about the name, start date, end data, involved partners, and focus of the projects. In order to retrieve additional public information on the projects, one possibility is to use web scraping techniques. Here, we give an example using a [Python script](src/scrapper.py). Note that other techniques can be used to collect this information, such as a KNIME workflow - see "[FAIRplus: D1.2 Selection criteria and guidelines for data sources from IMI projects and EFPIA internal databases](https://zenodo.org/record/3596024)" for more information on the KNIME workflow and the selection procedure.


3. Classify the project data based on the content information. This [Python script](src/fair_vocab_mapping.py) searches for a predefined list of disease keywords (present in the [ontology file](data/fair_ontology)) in the project content text, which subsequently allows grouping projects based on the disease keywords. This automated approach is helpful when dealing with large number of projects, but may not be needed for evaluating a few projects. The list of disease keywords can be adapted to fulfill specific needs.


5. Collect specific technical information using a data survey. This is a document containing an example of a [data survey](https://zenodo.org/record/3274230#.YbNVK7nMJgA) that was used to understand the data structure in a given project.


7. Use all project information and apply a score card. In this [document](https://zenodo.org/record/3596024#.YbNVQLnMJgA), projects are scored based on scientific, societal, and technical aspects. The total score is used to prioritize the projects. 


## Loading the script

#### Getting the code locally

Clone the GitHub repository locally using the following command in your terminal:
```
git clone https://github.com/Fraunhofer-ITMP/IMI-Project-Prioritization
```

Alternatively, you can also use [GitHub Desktop](https://desktop.github.com/) to clone the repository.

#### Creating a virtual environment
1. Go to the location of your cloned local repository via the terminal and get into the IMI-Project-Prioritization folder using the following command: 
```python
cd IMI-Project-Prioritization
```

2.  Create a virtual environment. If you are using conda, you can use the following commands:
```python
conda create --name virtualenv python=3.9
```

3. Activate your virtual environment:
```python
conda activate virtualenv
```

4. Install all the requirements into your virtual environment:
```python
pip install -r requirements.txt
```

5. Install the model used for the analsyis into your virtual environment:
```python
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_md-0.4.0.tar.gz
```

#### Pre-requisite installations

Data files:
1. [Project information file](https://github.com/Fraunhofer-ITMP/IMI-Project-Prioritization/blob/main/data/IMI2_Projects_Abstracts.xlsx) - File containing basic information of the project that can later be used for scraping from public domains.
2. [Vocabulary file](https://github.com/Fraunhofer-ITMP/IMI-Project-Prioritization/blob/aba71c7c664623ac5a179444576f9c71866b4c36/data/fair_ontology.tsv) - TSV file with mapping of terms with their classes.

Prior to running the scripts, please ensure that you manually download and install the [chromedriver](https://chromedriver.chromium.org/downloads) based on your Google Chrome version and change the path to the executable file in [constants.py](src/constants.py).

For Linux and Mac users, an additional step to add chromedriver to the path has to be done using the following command in your terminal:
```
mv chromedriver /usr/local/bin
sudo xattr -d com.apple.quarantine /usr/local/bin/chromedriver (For Mac M1 users)
```
For Mac user, be sure to authorize the execution of the binary in the System -> Preferences -> Security&Privacy -> General Tab

Note that you need to have admin rights on your computer or laptop for doing this.

## Running the script
Run the [main.py](src/main.py) file from the Python terminal as follows:
```python
python src/main.py
```

## Output
Upon running the code, you will get two files as outputs:
1. `imi2_project_list.tsv ` - This is a TSV file with all the information scrapped from the IMI website relevant to the project of interest.
2. `imi2_project_group.tsv` - This is a TSV file with the keyword-enriched information for the given project data found in the previous file. 
