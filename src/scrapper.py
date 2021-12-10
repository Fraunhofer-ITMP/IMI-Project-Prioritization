# -*- coding: utf-8 -*-

"""IMI Web Scraping code"""

import logging
import os
import pandas as pd
import time
from tqdm import tqdm

from constants import DATA_DIR, chrome_driver_path

# Selenium specific settings
try:
    from selenium import webdriver
except ImportError:
    raise ValueError("please install selenium before running this script")

from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

logger = logging.getLogger('__name__')

# Replace path to chrome driver (https://sites.google.com/a/chromium.org/chromedriver/home)
driver = webdriver.Chrome(
    options=chrome_options,
    executable_path=chrome_driver_path,
)


# function to take care of downloading file
def _enable_download_headless(
    browser,
    download_dir
):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


# function to handle setting up headless download
_enable_download_headless(driver, DATA_DIR)


def load_file():
    """Loads the project file"""
    df = pd.read_excel(
        os.path.join(DATA_DIR, 'IMI2_Projects_Abstacts+Participants.xlsx'),
        sheet_name='Abstract',
    )

    return df


def get_metadata():
    """Scape IMI website for information"""
    df = load_file()

    new_df = pd.DataFrame(
        columns=[
            'Project Acronym',
            'Member of the FAIRplus Fellowship program?',
            'FAIRplus: responsible public partner',
            'FAIRplus: responsible EFPIA partner',
            'EFPIA project lead',
            'Project Status Group (based on End Date)',
            'StartDate',
            'EndDate',
            'IMIProgram',
            'IMICall',
            'Societal Impact (Group based on FAIRplus keyword search)',  # Do not know yet
            'ShortDescription',  # title from df
            'Keywords',
            'TypeOfAction',
            'GrantAgreementNo',
            'IMIFunding',
            'EFPIAFunding',
            'OtherFunding',
            'TotalCost',
            'Summary',
            'EFPIAcompanies',
            'Univerisities',
            'SMEs',
            'PatientOrganisations',
            'Associated Partners',
            'ThirdParties',
            'ProjectWebsite',
            'FAIRification',  # Do not know
            'ContactFromColmsList',  # Cannot find it
            'Project Coordinator Name',  # Do not know yet
            'Project Coordinator Institute',
            'Project Contact email'  # Do not know yet
        ]
    )

    for row in tqdm(df.values, desc='Extracting data from IMI'):
        (
            grant_number,
            project_name,
            start_date,
            end_date,
            short_desc,
            summary,
            project_coordinator
        ) = row

        if project_name == 'IB4SD-TRISTAN':
            name = 'TRISTAN'
        elif project_name == 'GetReal Initiative':
            name = 'GetReal-Initiative'
        elif project_name == 'WEB-RADR 2':
            name = 'WEB-RADR-2'
        elif project_name == 'GNA NOW':
            name = 'GNA-NOW'
        elif project_name == 'Trials@Home':
            name = 'TrialsHome'
        elif project_name == 'INNODIA HARVEST':
            name = 'INNODIA-HARVEST'
        elif project_name == 'MAD-CoV 2':
            name = 'MAD-CoV-2'
        elif project_name == 'HARMONY PLUS':
            name = 'HARMONY-PLUS'
        elif len(project_name.split()) > 1:
            name = ''.join(project_name.split())
        else:
            name = project_name

        url = f'https://www.imi.europa.eu/projects-results/project-factsheets/{name.lower()}'
        driver.get(url)

        time.sleep(2)

        project_status = driver.find_element_by_xpath(
            '/html/body/div/div/div/section/div/article/div/div[2]/div[2]/div[2]/em/span[1]'
        ).text

        imi_program = driver.find_element_by_xpath(
            '/html/body/div/div/div/section/div/article/div/div[2]/div[2]/div[2]/em/span[2]'
        ).text

        keywords = ''
        for word in driver.find_elements_by_class_name('project-keyword'):
            if word.text:
                keywords += word.text + ','
        keywords = keywords.rsplit(',', 1)[0]

        imi_call = driver.find_element_by_xpath(
            '/html/body/div/div/div/section/div/article/div/div[2]/div[1]/div[2]/div/table[1]/tbody/tr[3]/td[2]'
        ).text.split()[-1]

        action = driver.find_element_by_xpath(
            '/html/body/div/div/div/section/div/article/div/div[2]/div[1]/div[2]/div/div'
        ).text

        # Finance-related table
        finance_table = driver.find_element_by_xpath(
            '/html/body/div/div/div/section/div/article/div/div[2]/div[1]/div[2]/div/table[2]/tbody'
        )
        imi_funding = ''
        empia_funding = ''
        other_funding = ''
        total_cost = ''
        for row in finance_table.find_elements_by_tag_name('tr'):
            data = row.find_elements_by_tag_name('td')
            if data[0].text == 'IMI Funding':
                imi_funding = ''.join(data[1].text.split())

            elif data[0].text == 'EFPIA in kind':
                empia_funding = ''.join(data[1].text.split())

            elif data[0].text == 'Other':
                other_funding = ''.join(data[1].text.split())

            elif data[0].text == 'Total Cost':
                total_cost = ''.join(data[1].text.split())

        try:
            project_link = driver.find_element_by_xpath(
                '/html/body/div/div/div/section/div/article/div/div[2]/div[1]/div[3]/div/p[1]/a'
            ).text
        except NoSuchElementException:
            project_link = ''

        project_contact = driver.find_element_by_class_name(
            'project-contact'
        ).text.split('\n')[1]

        # Participant-related data
        efpia_companies = ''
        universities = ''
        sme_companies = ''
        patient_orgs = ''
        associated_partners = ''
        third_party_companies = ''
        participants_list = driver.find_elements_by_class_name('project-participants-category')
        for element in participants_list:
            title = element.find_element_by_tag_name('h5').text

            data = ''
            for name in element.find_elements_by_class_name('text-capitalize'):
                data += name.text + ','

            if title == 'EFPIA companies':
                efpia_companies = data

            elif title == 'Universities, research organisations, public bodies, non-profit groups':
                universities = data

            elif title == 'Small and medium-sized enterprises (SMEs) and mid-sized companies (<€500 m turnover)':
                sme_companies = data

            elif title == 'Third parties':
                third_party_companies = data

            elif title == 'Patient organisations':
                patient_orgs = data

            elif title == 'Associated partners':
                associated_partners = data

        efpia_companies = efpia_companies.rsplit(',', 1)[0]
        universities = universities.rsplit(',', 1)[0]
        sme_companies = sme_companies.rsplit(',', 1)[0]
        patient_orgs = patient_orgs.rsplit(',', 1)[0]
        associated_partners = associated_partners.rsplit(',', 1)[0]
        third_party_companies = third_party_companies.rsplit(',', 1)[0]

        tmp_df = pd.DataFrame({
            'Project Acronym': project_name,
            'Member of the FAIRplus Fellowship program?': '',
            'FAIRplus: responsible public partner': '',
            'FAIRplus: responsible EFPIA partner': '',
            'EFPIA project lead': '',
            'Project Status Group (based on End Date)': project_status,
            'StartDate': start_date,
            'EndDate': end_date,
            'IMIProgram': imi_program,
            'IMICall': imi_call,
            'Societal Impact (Group based on FAIRplus keyword search)': '',  # Do not know yet
            'ShortDescription': short_desc,
            'Keywords': keywords,
            'TypeOfAction': action,
            'GrantAgreementNo': grant_number,
            'IMIFunding': imi_funding,
            'EFPIAFunding': empia_funding,
            'OtherFunding': other_funding,
            'TotalCost': total_cost,
            'Summary': summary,
            'EFPIAcompanies': efpia_companies,
            'Univerisities': universities,
            'SMEs': sme_companies,
            'PatientOrganisations': patient_orgs,
            'Associated Partners': associated_partners,
            'ThirdParties': third_party_companies,
            'ProjectWebsite': project_link,
            'FAIRification': '',  # Do not know
            'ContactFromColmsList': '',  # Cannot find it
            'Project Coordinator Name': project_contact,  # Do not know yet
            'Project Coordinator Institute': project_coordinator,
            'Project Contact email': ''  # Do not know yet
        }, index=[0])

        new_df = pd.concat([new_df, tmp_df], ignore_index=True)

    new_df.to_csv(
        os.path.join(DATA_DIR, 'imi2_project_list.tsv'),
        sep='\t',
        index=False
    )

    driver.close()
