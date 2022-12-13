#!/usr/bin/python3

import os
import sys
import requests
import argparse
from urllib.parse import urljoin
from pprint import pprint

API_URL = 'https://api.apkdetect.com'
API_KEY = ''


class APKDetect(object):
    def __init__(self):
        self.api_url = API_URL
        self.headers = {
            'X-API-KEY': API_KEY
        }
        self.requests_session = requests.session()

    def get_task(self, analysis_id):
        """
        Fetch status of the analysis with the specified id.

        :param analysis_id: analysis id
        :return: Status
        """

        url = urljoin(self.api_url, f"/task/{analysis_id}")
        resp = self.__do_api_request(url, "GET")
        return resp.json()

    def get_user(self):
        """
        Get user account information.

        :return: User
        """

        url = urljoin(self.api_url, "/user/")
        resp = self.__do_api_request(url, "GET")
        return resp.json()

    def get_file(self, file_id):
        """
        Fetch single file with the specified id.

        :param file_id: file id
        :return: File
        """

        url = urljoin(self.api_url, f"/file/{file_id}")
        resp = self.__do_api_request(url, "GET")
        return resp.json()

    def get_analysis(self, analysis_id):
        """
        Fetch single analysis with the specified id.

        :param analysis_id: analysis id
        :return: Analysis
        """

        url = urljoin(self.api_url, f"/analysis/{analysis_id}")
        resp = self.__do_api_request(url, "GET")
        return resp.json()

    def get_analyses(self):
        """
        Fetch the list of recent analyses.

        :return: List of Analysis
        """

        url = urljoin(self.api_url, "/analyses/")
        resp = self.__do_api_request(url, 'GET')
        return resp.json()

    def download_file(self, file_id, output):
        """ 
        Download file with the specified id and save it.

        :param file_id: file id
        :param output: path where file is stored
        :return: JSON with 'status' or 'error' key
        """

        url = urljoin(self.api_url, f"/file/download/{file_id}")
        resp = self.__do_api_request(url, "GET")

        # Success, save content to file
        if resp.status_code == 200:
            self.save_file(resp.content, output)
            return {'status': 'ok'}
        else:
            return resp.json()

    def download_decrypted_dex(self, analysis_id, output):
        """
        Download decrypted DEX file from the specified analysis.

        :param analysis_id: analysis id
        :param output: path where file is stored
        :return: JSON with 'status' or 'error' key
        """

        url = urljoin(self.api_url, f"/analysis/{analysis_id}/download/dex")
        resp = self.__do_api_request(url, "GET")

        # Success, save content to file
        if resp.status_code == 200:
            self.save_file(resp.content, output)
            return {'status': 'ok'}
        else:
            return resp.json()

    def upload(self, apk_filepath, community=1, comment=None):
        """ 
        Upload the APK file for analysis.

        :param apk_filepath: path to the APK
        :param community: 0 for private analysis, 1 to share with community (default)
        :param comment: comment added to the analysis
        :return: File
        """

        # Check if file exists
        if not os.path.isfile(apk_filepath):
            return {'error': 'File not found. Cannot submit the file.'}

        submit_api_url = urljoin(self.api_url, 'analysis/')

        # Read the file and upload
        with open(apk_filepath, "rb") as sample_fd:
            new_filename = os.path.basename(apk_filepath)

            params = {"community": community}

            # Add comment
            if comment:
                params.update({'comment': comment})

            files = {"file": (new_filename, sample_fd,
                              'application/octet-stream')}

            resp = self.__do_api_request(
                submit_api_url, "POST", data=params, files=files)
            return resp.json()

    def save_file(self, content, filepath):
        """
        Save file content to the secified filepath.

        :param content: file content
        :param filepath: path where file will be stored
        :return: None
        """

        with open(filepath, "wb") as fh:
            fh.write(content)

    def reanalyze(self, file_id):
        """
        Reanalyze the file with the specified id.

        :param file_id: file id
        :return: Task
        """

        url = urljoin(self.api_url, f"/file/reanalyze/{file_id}")
        resp = self.__do_api_request(url, "POST")
        return resp.json()

    def __do_api_request(self, url, method, data=None, files=None):
        """
        Send HTTP request to the API endpoint (GET,POST)

        :param url: url
        :param method: http method (GET or POST) 
        :param data: request payload
        :param files: files data
        :return: http response or None
        """

        if method not in ['GET', 'POST']:
            return None

        resp = None

        try:
            resp = self.requests_session.request(
                method, url, headers=self.headers, data=data, files=files)
        except requests.exceptions.HTTPError as exc:
            print(f"HTTPError: {exc}")
        except requests.exceptions.RequestException as exc:
            print(f"RequestException: {exc}")
        except Exception as exc:
            print(f"Exception: {exc}")
        finally:
            return resp


def main():
    parser = argparse.ArgumentParser(add_help=True,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description="Python script to interact with Apkdetect API")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-i', '--info', action='store_true',
                       help="Get user info")
    group.add_argument('-f', '--file', action='store', dest='file_id',
                       help="Get file with hash or file id")
    group.add_argument('-a', '--analysis', action='store', dest='analysis_id',
                       help="Get analysis with id")
    group.add_argument('-aa', '--analyses', action='store_true',
                       help="Get list of latest analyses")
    group.add_argument('-t', '--task', action='store', dest='task_id',
                       help="Get status of analysis with id")
    group.add_argument('-u', '--upload', action='store',
                       help="File to be uploaded")
    group.add_argument('-d', '--download', action='store',
                       help="Download file with id")
    group.add_argument('-r', '--reanalyze', action='store',
                       help="Reanalyze file with id")
    group.add_argument('-dd', '--dex', action='store',
                       help="Download decrypted DEX file from analysis with id")

    parser.add_argument('-o', '--output', action='store',
                        help="Output filepath for downloaded file")
    parser.add_argument('-p', '--private', action='store_true',
                        help="Upload analysis as private")
    parser.add_argument('-c', '--comment', action='store',
                        help="Add comment to uploaded file")
    
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    apkdetect = APKDetect()
    response = None

    if args.info:
        response = apkdetect.get_user()

    elif args.file_id:
        response = apkdetect.get_file(args.file_id)

    elif args.analysis_id:
        response = apkdetect.get_analysis(args.analysis_id)

    elif args.analyses:
        response = apkdetect.get_analyses()

    elif args.task_id:
        response = apkdetect.get_task(args.task_id)

    elif args.upload:

        # Share with community by default
        community = 1

        # Analysis should be private
        if args.private:
            community = 0

        response = apkdetect.upload(args.upload, community, args.comment)

    elif args.download or args.dex:
        if not args.output:
            print("Please specify the output filepath with '-o' option")

        # Download file
        elif args.download:
            response = apkdetect.download_file(args.download, args.output)

        # Download decrypted DEX file
        elif args.dex:
            response = apkdetect.download_decrypted_dex(args.dex, args.output)

    elif args.reanalyze:
        response = apkdetect.reanalyze(args.reanalyze)

    if response:
        pprint(response)


if __name__ == '__main__':
    main()
