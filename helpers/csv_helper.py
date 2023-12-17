from __future__ import annotations
import pandas as pd
import logging
logging.basicConfig(level=logging.WARN)

class CSVManager:
    def __init__(self, csv_path: str, columns: list[str] = []):
        self.csv_path = csv_path
        self.columns = columns

    def load_previous_csv(self) -> pd.DataFrame:
        try:
            previous_df = pd.read_csv(self.csv_path)
        except FileNotFoundError:
            previous_df = pd.DataFrame(columns=self.columns)
        return previous_df

    def save_df_to_csv(self, df) -> None:
        df.to_csv(self.csv_path, index=False)        

    def save_jobs(self, job_data: dict):
        previous_df = self.load_previous_csv()
        current_df = pd.DataFrame(data=job_data)
        current_df['notified'] = False
        merged_df = pd.concat([current_df, previous_df])
        merged_df = (merged_df
                     .drop_duplicates(subset=['url'], keep='last')
                     .reset_index(drop=True))
        new_jobs = len(merged_df) - len(previous_df)
        if new_jobs > 0:
            logging.warning(f' {new_jobs} new jobs found\n')
        else:
            logging.warning(' No new jobs found')
        self.save_df_to_csv(merged_df)
        return merged_df
