import subprocess
import pandas as pd, re
import requests
import json
import psutil
import re

def ollama_model_list():
    # Command to run in the command prompt
    command = "Ollama list"  # Replace with your command

    # Run the command
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Print the output and errors
    # print("Output:\n", stdout.decode())
    if stderr:
        print("Errors:\n", stderr.decode())

    ollama_mdl_df = pd.DataFrame(
        [
            re.sub(r"\s{2,}", ",", vl.strip()).split(",")
            for vl in stdout.decode().splitlines()
        ]
    )

    # Make the first row the header
    ollama_mdl_df.columns = ollama_mdl_df.iloc[0]
    ollama_mdl_df = ollama_mdl_df[1:]

    # Reset the index
    ollama_mdl_df.reset_index(drop=True, inplace=True)

    # print("completed without error")

    # Display the DataFrame
    return ollama_mdl_df["NAME"].values.tolist()

def ollama_active_model_list():
    # Command to run in the command prompt
    command = "Ollama ps"  # Replace with your command

    # Run the command
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # return stdout.decode()

    # Print the output and errors
    # print("Output:\n", stdout.decode())
    if stderr:
        print("Errors:\n", stderr.decode())

    ollama_mdl_df = pd.DataFrame(
        [re.split(r'\s{2,}', row.strip()) for row in stdout.decode().splitlines() if row]
    )

    # Make the first row the header
    ollama_mdl_df.columns = ollama_mdl_df.iloc[0]
    ollama_mdl_df = ollama_mdl_df[1:]

    # Reset the index
    ollama_mdl_df.reset_index(drop=True, inplace=True)

    # print("completed without error")

    # Display the DataFrame
    return ollama_mdl_df["NAME"].values.tolist()

def ollama_unload_models(mdl_nm = None):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": mdl_nm,
            "keep_alive": 0
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return {mdl_nm:True}
    except Exception as e:
        return{mdl_nm:str(e)}
    
def stop_ollama(name_pattern = '.*ollama.*'):
    # Regex pattern to match process names
    pattern = re.compile(name_pattern, re.IGNORECASE)

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if process name matches the pattern
            if pattern.search(proc.info['name']):
                proc.terminate()
                proc.wait(timeout=5)
                print(f"Successfully stopped process with PID: {proc.info['pid']} and Name: {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
            print(f"Failed to stop process {proc.info['name']} with PID {proc.info['pid']}. Error: {e}")