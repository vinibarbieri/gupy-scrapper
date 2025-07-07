import pandas as pd
import os
from .job_application import JobApplication


class CSVLogger:

    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['Company', 'Job Title', 'Job URL', 'Date Applied'])
            df.to_csv(file_path, index=False)

    def log(self, application: JobApplication):
        df = pd.read_csv(self.file_path)
        new_entry = {
            'Company': application.company,
            'Job Title': application.job_title,
            'Job URL': application.job_url,
            'Date Applied': application.date_applied
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
