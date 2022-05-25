# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/5/25 19:24
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

    uploads.set_defaults(handle=handle_result)

    uploads_folder = subparsers.add_parser('folder', help='文件夹上传')
    args = parser.parse_args()
    if hasattr(args, 'handle'):
        print(args)
        args.handle(args)
    else:
        parser.print_help()


def handle_result(args):
    headers_token = {'Content-Type': 'application/x-www-form-urlencoded'}
    client_id = args.cid
    redirect_uri = args.uri
    client_secret = args.pwd
    refresh_token = args.rt
    payload_token = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    # 获取token
    response_token = requests.post("https://login.partner.microsoftonline.cn/common/oauth2/v2.0/token",
                                   headers=headers_token, data=payload_token)
    access_token = response_token.json()['access_token']
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    # 获取文件信息
    file = args.file_path
    file_name = os.path.split(file)[1]
    upload_path = args.uppath
    # 获取上传临时url
    url_session = f"https://microsoftgraph.chinacloudapi.cn/v1.0/{client_id}/me/drive/root:{upload_path}{file_name}:/createUploadSession"
    response_session = requests.post(url_session, headers=headers, data=None)
    upload_url = response_session.json()['uploadUrl']
    # 上传文件
    with open(file, "rb") as f:
        f_bytes = f.read()
        f_bit = len(f_bytes)  # 需要单文件大小小于60MiB
        headers_upload = {
            "Content-Length": str(f_bit),
            "Content-Range": "bytes 0-" + str(f_bit - 1) + "/" + str(f_bit),
        }
        response = requests.request("PUT", upload_url, data=f_bytes, headers=headers_upload)
    print(response.text)


if __name__ == '__main__':
    cli()
