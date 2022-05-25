# !/usr/bin/env python
# -*- coding: utf-8 -*-
# cython:language_level=3
# @Time    : 2022/5/25 14:26
# @Author  : subjadeites
# @File    : upload.py
import requests

import argparse


def cli():
    parser = argparse.ArgumentParser(description='Upload to onedrive_cn')
    subparsers = parser.add_subparsers(metavar='子命令')

    # 添加子命令
    uploads = subparsers.add_parser('uploads', help='上传')
    # 参数(简写，全称，类型，是否必填，帮助说明)
    uploads.add_argument('-c', '--cid', type=str, required=True, help='client_id')
    uploads.add_argument('-r', '--uri', type=str, required=True, help='redirect_uri')
    uploads.add_argument('-s', '--pwd', type=str, required=True, help='client_secret')
    uploads.add_argument('-t', '--rt', type=str, required=True, help='refresh_token')
    uploads.add_argument('-n', '--name', type=str, required=True, help='file_name')
    uploads.add_argument('-p', '--path', type=str, required=True, help='file_path，最后的/不要')
    uploads.add_argument('-u', '--uppath', type=str, required=True, help='upload_path，最后的/不要')

    uploads.set_defaults(handle=handle_result)

    # 解析命令
    args = parser.parse_args()
    # 1.第一个命令会解析成handle，使用args.handle()就能够调用
    if hasattr(args, 'handle'):
        # 1.1.其他参数会被解析成args的属性，以命令全称为属性名
        args.handle(args)
    # 2.如果没有handle属性，则表示未输入子命令
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
    file_name = args.name
    file_path = f"{args.path}/{file_name}"
    upload_path = args.uppath
    # 获取上传临时url
    url_session = f"https://microsoftgraph.chinacloudapi.cn/v1.0/{client_id}/me/drive/root:{upload_path}{file_name}:/createUploadSession"
    response_session = requests.post(url_session, headers=headers, data=None)
    upload_url = response_session.json()['uploadUrl']
    # 上传文件
    with open(file_path, "rb") as f:
        f_bytes = f.read()
        f_bit = len(f_bytes)
        headers_upload = {
            "Content-Length": str(f_bit),
            "Content-Range": "bytes 0-" + str(f_bit - 1) + "/" + str(f_bit),
        }
        response = requests.request("PUT", upload_url, data=f_bytes, headers=headers_upload)
    print(response.text)
if __name__ == '__main__':
    cli()

# # 获取code
# scope = "offline_access files.readwrite.all"
# response_code = (
#     f"https://login.partner.microsoftonline.cn/common/oauth2/v2.0/authorize?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}")
# print(response_code)


