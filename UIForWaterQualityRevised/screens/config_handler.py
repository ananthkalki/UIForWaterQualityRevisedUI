import json
import os

class ConfigHandler:
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../utils/config.json")

    def __init__(self):
        with open(self.CONFIG_FILE_PATH, 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        with open(self.CONFIG_FILE_PATH, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_current_experiment(self):
        return self.data.get("currentExperiment")

    def get_current_experiment_path(self):
        return self.data.get("currentExperimentPath")

    def get_acquisition_duration_in_secs(self):
        return int(self.data.get("acquisitionDurationInSecs"))

    def get_mu1(self):
        return float(self.data.get("mu1"))

    def get_mu2(self):
        return float(self.data.get("mu2"))

    def get_std1(self):
        return float(self.data.get("std1"))

    def get_std2(self):
        return float(self.data.get("std2"))

    def set_current_experiment(self, value):
        self.data["currentExperiment"] = value
        self.save_data()

    def set_current_experiment_path(self, value):
        self.data["currentExperimentPath"] = value
        self.save_data()

    def set_acquisition_duration_in_secs(self, value):
        self.data["acquisitionDurationInSecs"] = int(value)
        self.save_data()


    def set_mu1(self, value):
        self.data["mu1"] = float(value)
        self.save_data()

    def set_mu2(self, value):
        self.data["mu2"] = float(value)
        self.save_data()

    def set_std1(self, value):
        self.data["std1"] = float(value)
        self.save_data()

    def set_std2(self, value):
        self.data["std2"] = float(value)
        self.save_data()
