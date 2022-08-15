# onedrive-action

利用OneDrive API，将你的内容推送到OneDrive。  
仅支持世纪互联。  
支持GitHub Actions。

## 用法说明

`python ./upload.py file /path/file -c client_id -r redirect_uri -s client_secret -t refresh_token -u upload_path`  
`python ./upload.py folder /path/folder -c client_id -r redirect_uri -s client_secret -t refresh_token -u upload_path`

## file

**/path/file**  
`上传文件的绝对路径，只支持单文件上传。`

## folder

**/path/folder**  
`上传文件夹的绝对路径，会连着文件夹本身一起上传。例如：/demo_upload/demo_upload_folder`

## 公有参数

**-c client_id**  
`应用程序(客户端) ID`

**-r redirect_uri**  
`重定向 URI`

**-s client_secret**  
`证书和密码 - 值`  
`注意：一旦离开创建成功页面，将无法获取到此值，请在创建时务必记牢。`

**-t refresh_token**  
`通过OneDrive API文档获取`

```
# 获取code
scope = "offline_access files.readwrite.all"
response_code = (
    f"https://login.partner.microsoftonline.cn/common/oauth2/v2.0/authorize?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}")
print(response_code)
# 然后访问本网址，登陆成功后，URL里面会有code=xxxxx，很长的字符串。

# 随后获取refresh_token
# 文档：https://docs.microsoft.com/zh-cn/onedrive/developer/rest-api/getting-started/graph-oauth?view=odsp-graph-online
# 需要替换成世纪互联网址。

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'client_secret': client_secret,
    'code': code,
    'grant_type': 'authorization_code',
}
response = requests.post(
    "https://login.partner.microsoftonline.cn/common/oauth2/v2.0/token", data=data, headers=headers)
refresh_token = response.json()['refresh_token']
```

**-u upload_path**  
`upload_path/ 上传的OneDrive目标文件夹路径。例如:/demo/demo_folder/`
