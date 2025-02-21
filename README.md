# TBME-Clinical-Data
Open source data and code for electrical impedance spectroscopy clinical study 

## Example

**Reading in the `.mat` data**

There is an [example code](load-data.ipynb) to load the data in Python.

If you want to load the data without the [Jupyter](https://jupyter.org/) environment, install the required packages using 

    pip install -r requirements.txt

and start Python.

Therefore import the provided `Data_mat` class

    from util import Data_mat

and set the path to the `.mat` file and the lesion information `.csv` file.

    path_mat = "data/mat/TBME_case_data.mat"
    lesion_path = "data/mat/TBME_Data_lesion_info.csv"

To finally load the data initialize the class and paste the path arguments into it.

    data = Data_mat(path_mat, lesion_path, prints=False)

You can access the following information by `data.<information-name>`.

- Case $\rightarrow$ `data.case`
- Category $\rightarrow$ `data.category`
- Cutpats $\rightarrow$ `data.cutpats`
- Longpats $\rightarrow$ `data.longpats`
- Magnitude $\rightarrow$ `data.magnitude`
- Phi $\rightarrow$ `data.phase`
- Reactance $\rightarrow$ `data.reactance`
- Resistance $\rightarrow$ `data.resistance`
- Sample $\rightarrow$ `data.sample`
- LesionAssessment $\rightarrow$ `data.lesion_assessment`
- LesionLoc $\rightarrow$ `data.lesion_loc`

**Reading in the `.npz` data**

For the potential use of each documented individual patient, the data samples were also [converted](data/mat_to_npz.ipynb) in `.npz` files.

The syntax for loading a single `.npz` file is

    import numpy as np

    file_path = "data/npz/data_sample_0000.npz"
    data = np.load(file_path, allow_pickle=True)

To list the available information inside the `data` variable use `print(data.files)`.
To access for example the LesionAssessment information, use `data['LesionAssessment']`.