from __future__ import annotations

import numpy as np
import pandas as pd
import requests
from huggingface_hub.hf_api import SpaceInfo

url = 'https://docs.google.com/spreadsheets/d/1XH7Jo3LXXfbSJ14z-QrSIQs21ArJMiV6_hMSAwY85PU/edit#gid=0'
csv_url = url.replace('/edit#gid=', '/export?format=csv&gid=')

class ModelList:
    def __init__(self):
        self.table = pd.read_csv(csv_url)
        self._preprocess_table()

        self.table_header = '''
            <tr>
                <td width="20%">Model Name</td>
                <td width="10%">Type</td>
                <td width="10%">Year</td>
                <td width="10%">Paper</td>
                <td width="10%">Code on Github</td>
                <td width="10%">Weights on 🤗</td>
                <td width="10%">Other Weights</td>
            </tr>'''

    def _preprocess_table(self) -> None:
        self.table['name_lowercase'] = self.table.name.str.lower()
        self.table['year'] = self.table['year'].apply(str)

        rows = []
        for row in self.table.itertuples():
            paper = f'<a href="{row.paper}" target="_blank">Paper</a>' if isinstance(
                row.paper, str) else ''
            github = f'<a href="{row.github}" target="_blank">GitHub</a>' if isinstance(
                row.github, str) else ''
            hf_model = f'<a href="{row.hub}" target="_blank">Hub Model</a>' if isinstance(
                row.hub, str) else ''
            other_model = f'<a href="{row.other}" target="_blank">Other Weights</a>' if isinstance(
                row.other, str) else ''
            data_type = f'{row.data_type}' if isinstance(
                row.data_type, str) else ''
            base_model = f'{row.base_model}' if isinstance(
                row.base_model, str) else ''
            year = f'{row.year}' if isinstance(
                row.year, str) else ''
            row = f'''
                <tr>
                    <td>{row.name}</td>
                    <td>{data_type}</td>
                    <td>{year}</td>
                    <td>{paper}</td>
                    <td>{github}</td>
                    <td>{hf_model}</td>
                    <td>{other_model}</td>
                </tr>'''
            rows.append(row)
        self.table['html_table_content'] = rows

    def render(self, search_query: str, 
            case_sensitive: bool,
            filter_names: list[str],
            data_types: list[str],
            years: list[str],
            #model_types: list[str]
              ) -> tuple[int, str]:
        df = self.table
        if search_query:
            if case_sensitive:
                df = df[df.name.str.contains(search_query)]
            else:
                df = df[df.name_lowercase.str.contains(search_query.lower())]
        has_paper = 'Paper' in filter_names
        has_github = 'Code' in filter_names
        has_model = 'Model Weights' in filter_names
        df = self.filter_table(df, has_paper, has_github, has_model, data_types, years)
        #df = self.filter_table(df, has_paper, has_github, has_model, data_types, model_types)
        return len(df), self.to_html(df, self.table_header)

    @staticmethod
    def filter_table(df: pd.DataFrame, has_paper: bool, has_github: bool,
                     has_model: bool,
                     data_types: list[str],
                     years: list[str],
                     #model_types: list[str]
                    ) -> pd.DataFrame:
        if has_paper:
            df = df[~df.paper.isna()]
        if has_github:
            df = df[~df.github.isna()]
        if has_model:
            df = df[~df.hub.isna() | ~df.other.isna()]
        df = df[df.data_type.isin(set(data_types))]
        #df = df[df.base_model.isin(set(model_types))]
        df = df[df.year.isin(set(years))]
        return df

    @staticmethod
    def to_html(df: pd.DataFrame, table_header: str) -> str:
        table_data = ''.join(df.html_table_content)
        html = f'''
        <table>
            {table_header}
            {table_data}
        </table>'''
        return html