# apkdetect-api

The Python3 client script to interact with the Apkdetect API. 

## Installation

```
pip3 install requests
```

## Usage

Add your API key in the `client.py` file. The API key is available in the Apkdetect user profile.

```python
API_KEY = '<YOUR_API_KEY>'
```

See the available options using the command:

`python client.py -h`

```
usage: client.py [-h] [-i | -f FILE_ID | -a ANALYSIS_ID | -aa | -t TASK_ID | -u UPLOAD | -d DOWNLOAD | -r REANALYZE | -dd DEX] [-o OUTPUT] [-p] [-c COMMENT]

Python script to interact with Apkdetect API

optional arguments:
  -h, --help            show this help message and exit
  -i, --info            Get user info
  -f FILE_ID, --file FILE_ID
                        Get file with hash or file id
  -a ANALYSIS_ID, --analysis ANALYSIS_ID
                        Get analysis with id
  -aa, --analyses       Get list of latest analyses
  -t TASK_ID, --task TASK_ID
                        Get status of analysis with id
  -u UPLOAD, --upload UPLOAD
                        File to be uploaded
  -d DOWNLOAD, --download DOWNLOAD
                        Download file with id
  -r REANALYZE, --reanalyze REANALYZE
                        Reanalyze file with id
  -dd DEX, --dex DEX    Download decrypted DEX file from analysis with id
  -o OUTPUT, --output OUTPUT
                        Output filepath for downloaded file
  -p, --private         Upload analysis as private
  -c COMMENT, --comment COMMENT
                        Add comment to uploaded file
```

Examples:

1. Fetch the file object with MD5/SHA1/SHA256 hash or file_id

`python client.py -f <id>`

2. Upload APK file

`python client.py -u <filepath>`

Optional arguments:
* `-p` - private analysis
* `-c <comment>` - add comment to the analysis

3. Download a file with file_id

`python client.py -d <file_id> -o <output_filepath>`

## API reference

See the tab `API Docs` under the user profile in the Apkdetect portal.

## Contact

In case you have any questions, please send an email at `info@apkdetect.com`
