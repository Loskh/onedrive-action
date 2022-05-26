# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/5/27 01:00
# @Author  : subjadeites
# @File    : upload.py
import argparse
import os

import requests


def cli():
    parser = argparse.ArgumentParser(description='Upload to onedrive_cn')
    subparsers = parser.add_subparsers(metavar='子命令')

    uploads = subparsers.add_parser('file', help='单文件上传')
    uploads.add_argument('file_path', metavar='file_path', type=str, help='/file_path/file_name')
    # 参数(简写，全称，类型，是否必填，帮助说明)
    uploads.add_argument('-c', '--cid', type=str, required=True, help='client_id')
    uploads.add_argument('-r', '--uri', type=str, required=True, help='redirect_uri')
    uploads.add_argument('-s', '--pwd', type=str, required=True, help='client_secret')
    uploads.add_argument('-t', '--rt', type=str, required=True, help='refresh_token')
    uploads.add_argument('-u', '--uppath', type=str, required=True, help='upload_path/')
    uploads.set_defaults(handle=handle_file)

    uploads_folder = subparsers.add_parser('folder', help='将文件夹上传到Onedrive')
    uploads_folder.add_argument('folder_path', metavar='file_path', type=str, help='/folder_path/folder')
    uploads_folder.add_argument('-c', '--cid', type=str, required=True, help='client_id')
    uploads_folder.add_argument('-r', '--uri', type=str, required=True, help='redirect_uri')
    uploads_folder.add_argument('-s', '--pwd', type=str, required=True, help='client_secret')
    uploads_folder.add_argument('-t', '--rt', type=str, required=True, help='refresh_token')
    uploads_folder.add_argument('-u', '--uppath', type=str, required=True, help='upload_path/')
    uploads_folder.set_defaults(handle=handle_folder)

    args = parser.parse_args()
    if hasattr(args, 'handle'):
        print(args)
        args.handle(args)
    else:
        parser.print_help()


def handle_file(args):
    client_id = args.cid
    redirect_uri = args.uri
    client_secret = args.pwd
    refresh_token = args.rt
    path = args.file_path
    upload_path = args.uppath
    handle_upload(client_id, redirect_uri, client_secret, refresh_token, upload_path, path)


def handle_folder(args):
    client_id = args.cid
    redirect_uri = args.uri
    client_secret = args.pwd
    refresh_token = args.rt
    path = args.folder_path
    upload_path = args.uppath
    handle_upload(client_id, redirect_uri, client_secret, refresh_token, upload_path, path, is_folder=True)


def handle_upload(client_id, redirect_uri, client_secret, refresh_token, upload_path, path, is_folder: bool = False):
    headers_token = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload_token = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    # 获取token
    access_token = requests.post("https://login.partner.microsoftonline.cn/common/oauth2/v2.0/token",
                                 headers=headers_token, data=payload_token).json()['access_token']
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    # 获取文件信息
    if is_folder:
        folder_name = os.path.split(path)[1]  # 获取文件夹名
        if path[0] == '.':
            raise ("请使用绝对路径！")
        elif path != os.path.abspath(__file__).strip(os.path.basename(__file__)):  # 如果不是脚本当前目录
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if dirpath == path:  # 处理根目录
                        temp_upload_path = os.path.join(dirpath.replace(path, r'/'), filename)
                    else:
                        temp_upload_path = os.path.join(dirpath.replace(os.path.join(path, ""), r'/'), filename)
                    # 获取上传临时url
                    url_session = f"https://microsoftgraph.chinacloudapi.cn/v1.0/{client_id}/me/drive/root:{upload_path}{folder_name}{temp_upload_path}:/createUploadSession"
                    upload_url = requests.post(url_session, headers=headers, data=None).json()['uploadUrl']
                    # 上传文件
                    upload_file(os.path.join(dirpath, filename), upload_url)

        else:
            raise Exception("不能上传脚本所在文件夹")
    else:
        file_name = os.path.split(path)[1]
        # 获取上传临时url
        url_session = f"https://microsoftgraph.chinacloudapi.cn/v1.0/{client_id}/me/drive/root:{upload_path}{file_name}:/createUploadSession"
        upload_url = requests.post(url_session, headers=headers, data=None).json()['uploadUrl']
        # 上传文件
        upload_file(path, upload_url)


def upload_file(file_path, upload_url):
    with open(file_path, "rb") as f:
        f_bytes = f.read()
        f_bit = len(f_bytes)  # 需要单文件大小小于60MiB
        headers_upload = {
            "Content-Length": str(f_bit),
            "Content-Range": "bytes 0-" + str(f_bit - 1) + "/" + str(f_bit),
        }
        response = requests.request("PUT", upload_url, data=f_bytes, headers=headers_upload)
    print(response)


if __name__ == '__main__':
    cli()
