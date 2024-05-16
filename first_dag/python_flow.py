from __future__ import annotations

import logging
import os
import json
import subprocess

from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import is_venv_installed

from SteamScraper.data_clean import clean_data
from SteamScraper.data_analysis import analyze_clean_data

log = logging.getLogger(__name__)

download_dir = os.getcwd() + '/dags/SteamScraper/Project'
save_path = os.path.normpath(os.path.join(download_dir, 'Data'))

if not is_venv_installed():
    log.warning("The tutorial_taskflow_api_virtualenv example DAG requires virtualenv, please install it.")
else:
    @dag(schedule=None, 
         start_date=datetime(2021, 1, 1), 
         catchup=False, 
         tags=["big_data"])

    def CS4540_Test_Dag():
        """
        ### TaskFlow API example using virtualenv

        This is a simple data pipeline example which demonstrates the use of the TaskFlow API using three simple tasks for Extract, Transform, and Load.
        """

        @task.virtualenv(
            use_dill=True,
            system_site_packages=False,
            requirements=["funcsigs"],
        )

        

        def extract_from_steam():
            """
            #### Extract task

            A simple Extract task to get data ready for the rest of the data pipeline. In this case, getting data is simulated by reading from a hardcoded JSON string.
            """

            print("Data has been extracted from Steam")

            return True
            

        @task()
        def data_clean(isT1Success):
            """
            #### Data cleaning task
            A simple clean_data task which cleans the data in the pipeline.
            """

            try:
                new_dir = subprocess.check_output(["ls"], text=True)
                print(new_dir)
            except:
                print("IDK")


            if isT1Success:
                clean_data(save_path)
                return True
            else:
                return False

        @task()
        def analyze_data(isT2Success):
            """
            #### Load task
            A simple Load task which takes in the result of the Transform task and instead of saving it to end user review, just prints it out.
            """

            if isT2Success:
                print("Idk what to put here, but this loads the result of the analyze task")
                print("T2 was a Success")
                analyze_clean_data(save_path)
                return True
            else:
                print("Unsuccessful T2")
                return False

        @task()
        def visualize_data(isT3Success):
            if isT3Success:
                print("We will visualize data")
            else:
                print("Check on the previous tasks")

        t1success = extract_from_steam()
        t2success= data_clean(t1success)
        t3success = analyze_data(t2success)
        visualize_data(t3success)

    python_demo_dag = CS4540_Test_Dag()