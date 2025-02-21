import numpy as np
import h5py


class Data:
    def __init__(self, path, access_name: str = "tissuetypes", prints: bool = True):
        self.path = path
        self.access_name = access_name
        self.prints = prints

        self.init_data()

    def init_data(self):
        # loading .mat file
        self.data = h5py.File(self.path, "r")
        self.keys = self.data.get(f"{self.access_name}").keys()
        if self.prints:
            print(self.data.keys(), "\n")  # -> tissuetypes
            print(self.data.get(f"{self.access_name}").keys())
            print("\n")

        data_dict = dict()
        if self.prints:
            print(f"Keys in {self.path}/{self.access_name}...")
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

            elif h5py_type == "<u4":
                for p in range(self.data.get(f"{self.access_name}/{key}").shape[0]):
                    my_string_list = list()
                    references = self.data[f"{self.access_name}/{key}"][p]
                    for r in references:
                        my_string_list.append(self.data[r][:])
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

        self.resistance = data_dict["Resistance"]
        self.reactance = data_dict["Reactance"]
        self.phase = data_dict["Phi"]
        self.magnitude = data_dict["Magnitude"]
        self.cutpats = data_dict["Cutpats"]
        self.lesion_assessment = data_dict["LesionAssessment"]
