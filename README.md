## Information
All the data used in passport training is present in the ultimus google drive folder. API Code is present [here](#github-repo).



## Attributes
**Model** | **Description**
:---- | ----
|Scaled YOLOv4|trained in the google colab, all scripts are there|
|Annotation Tool|CVAT online tool|
|Augmentation Script | Present in the google drive |
|API + Code Base | Present [here](#github-repo) |
|DL Model Training Script| Only Present on Google Drive (Ultimus) |

:::danger
Data is only present in email and on psdev04
:::

:::important
Issues were encountered while installing **tesseract**
:::

# Github Repo

Find github repo. at

```
https://github.com/TalhaUsuf/passport_ocr.git
```
For cloning via ssh:

```
git@github.com:TalhaUsuf/passport_ocr.git
```

# For Running the API

Run :
```
python run_app_debug.py
```

Go to following URL to access docs.
```
http://127.100.100.1:8000/docs
```

Two URLs are accessible:

 - For byte-array files (in case which image is saved as a byte-array string)
    - http://127.100.100.1:8000/ocr/byte_array/<file-path.bin>
 - For base64 image string file (in case image has been converted to base64 string and that string is in file)
   - http://127.100.100.1:8000/ocr/base64/<file-path.bin>

:::important
Image Must be JPG.
:::
