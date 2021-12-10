# -*- coding: utf-8 -*-

"""Keyword mapping and searching code."""

import en_core_sci_md
import os
import pandas as pd
from fuzzywuzzy import fuzz
from tqdm import tqdm

from constants import DATA_DIR


def get_fair_mapping():
    """Method to map the description to FAIR vocab terms"""
    fair_df = pd.DataFrame(
        columns=[
            'Project',
            'ShortDescription_CountNeurodegenerative',
            'ShortDescription_CountAMR',
            'ShortDescription_CountChronic',
            'ShortDescription_CountAging',
            'ShortDescription_CountDisease',
            'Keywords_CountNeurodegenerative',
            'Keywords_CountAMR',
            'Keywords_CountChronic',
            'Keywords_CountAging',
            'Keywords_CountDisease',
            'Summary_CountNeurodegenerative',
            'Summary_CountAMR',
            'Summary_CountChronic',
            'Summary_CountAging',
            'Summary_CountDisease',
            'ShortDescription_Neurodegenerative',
            'ShortDescription_AMR',
            'ShortDescription_Chronic',
            'ShortDescription_Aging',
            'ShortDescription_Disease',
            'Keywords_Neurodegenerative',
            'Keywords_AMR',
            'Keywords_Chronic',
            'Keywords_Aging',
            'Keywords_Disease',
            'Summary_Neurodegenerative',
            'Summary_AMR',
            'Summary_Chronic',
            'Summary_Aging',
            'Summary_Disease'
        ]
    )

    data_df = pd.read_csv(
        os.path.join(DATA_DIR, 'imi2_project_list.tsv'),
        sep='\t',
        usecols=[
            'Project Acronym',
            'ShortDescription',
            'Keywords',
            'Summary'
        ]
    )

    vocab_df = pd.read_csv(
        os.path.join(DATA_DIR, 'fair_ontology.tsv'),
        sep='\t'
    )

    vocab_groups = vocab_df['category'].unique().tolist()
    vocab_dict = {
        term: category
        for term, category in vocab_df.values
    }

    for row in tqdm(data_df.values, desc='Mapping to ontology', total=data_df.shape[0]):
        (
            project_name,
            description,
            keywords,
            summary
        ) = row
        nlp = en_core_sci_md.load()

        # Short description mapping
        doc = nlp(description)

        short_desc_dict = {
            name: set()
            for name in vocab_groups
        }

        for entity in doc.ents:
            entity = entity.text

            for word in vocab_dict:
                distance = fuzz.ratio(entity, word)

                if distance > 80:
                    short_desc_dict[vocab_dict[word]].add(entity)

        # Keyword mapping
        doc = nlp(keywords)

        keywords_dict = {
            name: set()
            for name in vocab_groups
        }

        for entity in doc.ents:
            entity = entity.text

            for word in vocab_dict:
                distance = fuzz.ratio(entity, word)

                if distance > 80:
                    keywords_dict[vocab_dict[word]].add(entity)

        # Summary mapping
        doc = nlp(summary)

        summary_dict = {
            name: set()
            for name in vocab_groups
        }

        for entity in doc.ents:
            entity = entity.text

            for word in vocab_dict:
                distance = fuzz.ratio(entity, word)

                if distance > 70:
                    summary_dict[vocab_dict[word]].add(entity)

        tmp_df = pd.DataFrame({
            'Project': project_name,
            'ShortDescription_CountNeurodegenerative': len(short_desc_dict['Neurodegenerative']),
            'ShortDescription_CountAMR': len(short_desc_dict['AMR']),
            'ShortDescription_CountChronic': len(short_desc_dict['Chronic']),
            'ShortDescription_CountAging': len(short_desc_dict['Aging']),
            'ShortDescription_CountDisease': len(short_desc_dict['Disease']),
            'Keywords_CountNeurodegenerative': len(keywords_dict['Neurodegenerative']),
            'Keywords_CountAMR': len(keywords_dict['AMR']),
            'Keywords_CountChronic': len(keywords_dict['Chronic']),
            'Keywords_CountAging': len(keywords_dict['Aging']),
            'Keywords_CountDisease': len(keywords_dict['Disease']),
            'Summary_CountNeurodegenerative': len(summary_dict['Neurodegenerative']),
            'Summary_CountAMR': len(summary_dict['AMR']),
            'Summary_CountChronic': len(summary_dict['Chronic']),
            'Summary_CountAging': len(summary_dict['Aging']),
            'Summary_CountDisease': len(summary_dict['Disease']),
            'ShortDescription_Neurodegenerative': ', '.join(short_desc_dict['Neurodegenerative']),
            'ShortDescription_AMR': ', '.join(short_desc_dict['AMR']),
            'ShortDescription_Chronic': ', '.join(short_desc_dict['Chronic']),
            'ShortDescription_Aging': ', '.join(short_desc_dict['Aging']),
            'ShortDescription_Disease': ', '.join(short_desc_dict['Disease']),
            'Keywords_Neurodegenerative': ', '.join(keywords_dict['Neurodegenerative']),
            'Keywords_AMR': ', '.join(keywords_dict['AMR']),
            'Keywords_Chronic': ', '.join(keywords_dict['Chronic']),
            'Keywords_Aging': ', '.join(keywords_dict['Aging']),
            'Keywords_Disease': ', '.join(keywords_dict['Disease']),
            'Summary_Neurodegenerative': ', '.join(summary_dict['Neurodegenerative']),
            'Summary_AMR': ', '.join(summary_dict['AMR']),
            'Summary_Chronic': ', '.join(summary_dict['Chronic']),
            'Summary_Aging': ', '.join(summary_dict['Aging']),
            'Summary_Disease': ', '.join(summary_dict['Disease'])
        }, index=[0])
        fair_df = pd.concat([fair_df, tmp_df], ignore_index=True)

    fair_df.to_csv(
        os.path.join(DATA_DIR, 'imi2_project_group.tsv'),
        sep='\t',
        index=False
    )
