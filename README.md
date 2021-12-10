# IMI_Scrapper

This repository is meant to provide an example of the code we used for scraping IMI projects for WP-1 FAIRPlus. It might be generalizable to address other projects having a different list of websites. Our aim was to create extensive list of all IMI projects for prioritization purposes. The script takes as input the LIST XXX [here also Zenodo link?] and generates an enriched output where eacxh project are profiled according with the approach described here [link of paper or of selection strategy in Zenodo].
if the starting project list is limited this can be overdone. As we started with 120+ projects we decided to automatize where possible the data extraction. The output of the present script has been used to fill the template table whcih can be found here [zenodo link] for further prioritization discussion either within the Fairplus team or with singular project data champion in order to further refine the project profiling.  


In alternative Gesa witt sent this other README

Read Me: Project selection and Prioritization Tools 
1. Collect all project information necessary to make a selection as shown exemplary in the excel sheet (file xx). It contains information about the name, start date, end data, involved partners and focus of the project. One possibility to create the project overview is to use web scraping techniques to retrieve public information. We give an example using a Python script (file xx). But also KNIME can be used to collect project information, as shown in this example (file xx).
2. Classify the project data based on the content information. This Python script (file xx) searches for a predefined list of keywords in the project information table, which subsequently allows to group projects based on the identified content. This approach is helpful for a large number of projects, but might not be needed for only a few projects that should be evaluated. 
3. Collect specific technical information using a data survey. This is an example of a data survey (file xx) that was used to understand the data structure in a given project.
3. Use all project information and apply a score card. In the given example (file xx) projects are scored based on scientific, societal and technical aspects. The total score is used to prioritize a project. 

