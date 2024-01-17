import time
import numpy as np
import pandas as pd
from ctypes import *
from .config_handler import ConfigHandler
import RPi.GPIO as GPIO
import json
import os
import pickle
class Processor:
    _instance = None
    BuzzerPin = 21
    DataforReference=[]
    DataforSample=[]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Processor, cls).__new__(cls)
            GPIO.setwarnings(False)
            # BCM is 21 PIN 40
            GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
            GPIO.setup(21, GPIO.OUT)  # LED pin set as output
            # Initialization code here
        cls._instance.config_handler = ConfigHandler()
        cls._instance.samplingTimeInSeconds = cls._instance.config_handler.get_acquisition_duration_in_secs()
        cls._instance.DataforSaline = []
        cls._instance.DataforBioBurden = []

        return cls._instance


    def BuzzerSound(self):
        GPIO.output(self.BuzzerPin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.BuzzerPin, GPIO.LOW)
        time.sleep(0.1)
        pass  # GPIO logic for buzzer can be added here

    def StartTestForReference(self):
        self.BuzzerSound()
        SampleCSVFilepath = os.path.abspath(self.config_handler.get_current_experiment_path()+"/ref.csv")
        os.makedirs(os.path.dirname(SampleCSVFilepath), exist_ok=True)
        with open(SampleCSVFilepath,"w") as fp:
            fp.write("")
        print("Check this out",SampleCSVFilepath)
        libCalc = CDLL("./timedAcq_new.so")
        for i in range(0, len(SampleCSVFilepath)):
            libCalc.path(ord(SampleCSVFilepath[i]), 0)
        libCalc.path(ord('\0'), 1)
        libCalc.main(self.samplingTimeInSeconds)
        self.BuzzerSound()
        

    def ReferenceAnalysis(self):
        data = pd.read_csv(self.config_handler.get_current_experiment_path()+"/ref.csv")
        print(self.config_handler.get_current_experiment_path())
        print(data)
        datacounts, bins = np.histogram(data['tof'], bins=np.arange(0, 100, 0.2))
        datacounts = self.removeOffset(datacounts)
        self.DataforReference.append(max(datacounts))
        self.DataforReference.append(self.GetTotalCounts(datacounts, bins))

    def StartTestForSample(self):
        self.BuzzerSound()
        SampleCSVFilepath = os.path.abspath(self.config_handler.get_current_experiment_path()+"/sam.csv")
        os.makedirs(os.path.dirname(SampleCSVFilepath), exist_ok=True)
        with open(SampleCSVFilepath,"w") as fp:
            fp.write("")
        libCalc = CDLL("./timedAcq_new.so")
        for i in range(0, len(SampleCSVFilepath)):
            libCalc.path(ord(SampleCSVFilepath[i]), 0)
        libCalc.path(ord('\0'), 1)
        libCalc.main(self.samplingTimeInSeconds)
        self.BuzzerSound()
        

    def SampleAnalysis(self):
        data = pd.read_csv(self.config_handler.get_current_experiment_path()+"/sam.csv")
        print(self.config_handler.get_current_experiment_path())
        print(data)
        datacounts, bins = np.histogram(data['tof'], bins=np.arange(0, 100, 0.2))
        datacounts = self.removeOffset(datacounts)
        self.DataforSample.append(max(datacounts))
        self.DataforSample.append(self.GetTotalCounts(datacounts, bins))

    def GetTotalCounts(self, data, bins):
        CountStart = 10            # START TIME AND END TIME FOR AREA UNDER CURVE
        CountStop = 15
        sum = 0
        for i in range(len(data)):
            if ((bins[i] > CountStart) and (bins[i] < CountStop)):
                sum = sum + data[i]
        return sum
    def removeOffset(self,data):
        DecayIdleTailDurationNs = 20
        HistbinInterval = 0.2
        tailLen = int(np.floor(DecayIdleTailDurationNs/HistbinInterval))
        return data - np.mean(data[-tailLen:])

    def Result(self):
        self.ReferenceAnalysis()
        self.SampleAnalysis()
        MODEL_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "../model/BioburdenDetector_v1.0.sav")
        model = pickle.load(open(MODEL_FILE_PATH, 'rb'))
        output_file = self.config_handler.get_current_experiment_path() + "/results.json"
        print(output_file)
        x1 = (self.DataforSample[0] - self.DataforReference[0]) / self.DataforReference[0]
        x2 = (self.DataforSample[1] - self.DataforReference[1]) / self.DataforReference[1]
        X1 = (x1 - self.config_handler.get_mu1()) / self.config_handler.get_std1()
        X2 = (x2 - self.config_handler.get_mu2()) / self.config_handler.get_std2()
        X1 = np.array([X1])
        X2 = np.array([X2])
        XOUT = np.hstack((X1.reshape(-1, 1), X2.reshape(-1, 1)))
        try:
            bioburden_present = model.predict(XOUT)
            # Determine the result
            if (bioburden_present == 1):
                result_status = "Positive"
            else:
                result_status = "Negative"

            # Construct the data to be written to JSON
            data = {
                "refPeakCount": self.DataforReference[0],
                "refTotalCount": self.DataforReference[1],
                "samPeakCount": self.DataforSample[0],
                "samTotalCount": self.DataforSample[1],
                "bioBurden": result_status,
                "acquisitionDurationInSecs": self.config_handler.get_acquisition_duration_in_secs(),
                "mu1": self.config_handler.get_mu1(),
                "mu2": self.config_handler.get_mu2(),
                "std1": self.config_handler.get_std1(),
                "std2": self.config_handler.get_std2()
            }

            # Write the data to the JSON file
            with open(output_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)

            return result_status
        except ValueError:
            result_status="NaN Error"
            # Construct the data to be written to JSON
            data = {
                "refPeakCount": self.DataforReference[0],
                "refTotalCount": self.DataforReference[1],
                "samPeakCount": self.DataforSample[0],
                "samTotalCount": self.DataforSample[1],
                "bioBurden": result_status,
                "acquisitionDurationInSecs": self.config_handler.get_acquisition_duration_in_secs(),
                "mu1": self.config_handler.get_mu1(),
                "mu2": self.config_handler.get_mu2(),
                "std1": self.config_handler.get_std1(),
                "std2": self.config_handler.get_std2()
            }

            # Write the data to the JSON file
            with open(output_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)

            return result_status




