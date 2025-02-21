import h5py
import numpy as np
import pandas as pd

from .functions import trim_spaces


class Data_mat:
    def __init__(
        self,
        path_mat: str,
        lesion_path: str = None,
        access_name: str = "filteredPatients",
        prints: bool = True,
    ):
        self.path_mat = path_mat
        self.lesion_path = lesion_path
        self.access_name = access_name
        self.prints = prints

        self.init_data()

    def init_data(self):

        data_dict = dict()

        if self.path_mat != None:
            # loading .mat file
            self.data = h5py.File(self.path_mat, "r")
            self.keys = self.data.get(f"{self.access_name}").keys()
            if self.prints:
                print(self.data.keys(), "\n")  # -> tissuetypes
                print(self.data.get(f"{self.access_name}").keys())
                print("\n")

            if self.prints:
                print(f"Keys in {self.path_mat}/{self.access_name}...")
            for key in self.keys:
                h5py_type = str(
                    self.data[self.data[f"{self.access_name}/{key}"][0, 0]]
                ).split('"')[-2]

                if self.prints:
                    print(f"\t- {key=}, {h5py_type=}")
                data_list = list()

                if h5py_type == "<u2":
                    for p in range(self.data.get(f"{self.access_name}/{key}").shape[0]):
                        my_string_list = list()
                        references = self.data[f"{self.access_name}/{key}"][p]
                        for r in references:
                            my_string_list.append(
                                "".join(chr(c.item()) for c in self.data[r][:])
                            )
                        data_list.append(my_string_list)
                    data_dict[key] = np.concatenate(data_list)

                elif h5py_type == "<f8":
                    ref_array = self.data.get(f"{self.access_name}/{key}")[:, 0]
                    for ref in ref_array:
                        obj = self.data[ref]
                        if isinstance(obj, h5py.Dataset):
                            data_list.append(obj[:])
                    try:
                        data_list = np.squeeze(data_list)
                    except BaseException:
                        data_list = np.concatenate(data_list)
                    data_dict[key] = data_list

                self.data_dict = data_dict
            self.case_mat = data_dict["Case"]  # for check
            self.category = data_dict["Category"]
            self.longpats = data_dict["Longpats"]
            self.resistance = data_dict["Resistance"]
            self.reactance = data_dict["Reactance"]
            self.phase = data_dict["Phi"]
            self.magnitude = data_dict["Magnitude"]
            self.sample = data_dict["Sample"]
            self.cutpats = data_dict["Cutpats"]

        if self.lesion_path != None:
            # read lesion data
            if self.prints:
                print(f"Load lesion data fro {self.lesion_path}.")

            df = pd.read_csv(self.lesion_path)
            df = pd.DataFrame(df)
            df = df.replace({" ": "None"})
            self.df = df

            self.case_txt = df["Case"]  # for check
            LesionLoc = trim_spaces(df[" LesionLoc"])
            LesionAssessment = trim_spaces(df[" LesionAssessment"])

            self.data_dict["LesionAssessment"] = LesionAssessment
            self.lesion_assessment = LesionAssessment
            self.data_dict["LesionLoc"] = LesionLoc
            self.lesion_loc = LesionLoc

        if self.lesion_path != None and self.path_mat != None:
            self.case_txt = np.array(self.case_txt, dtype=int)
            self.case_mat = np.array(self.case_txt, dtype=int)
            assert (
                self.case_txt == self.case_mat
            ).all(), "please check the Case alignment in both files."
            self.case = self.case_txt
            self.n_entries = len(self.case)
            del self.case_txt, self.case_mat
