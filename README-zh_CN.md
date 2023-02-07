# SmartAppToHelpSeniorsAPI
[![License](https://img.shields.io/github/license/youngzm339/SmartAppToHelpSeniorsAPI)](https://github.com/youngzm339/SmartAppToHelpSeniorsAPI/blob/master/LICENSE)
[![Issues](https://img.shields.io/github/issues/youngzm339/SmartAppToHelpSeniorsAPI)](https://github.com/youngzm339/SmartAppToHelpSeniorsAPI/issues)
[![Stars](https://img.shields.io/github/stars/youngzm339/SmartAppToHelpSeniorsAPI)](https://github.com/youngzm339/SmartAppToHelpSeniorsAPI)

![SmartAppToHelpSeniorsAPI](https://azurecomcdn.azureedge.net/cvt-342af4abf51292fe470c0f54c8b878f696465f7b08177b0a21f80ffab347bd93/images/page/home/december-hero-desktop.webp)

README of supported languages: [English](./README.md)  |  [简体中文](./README-zh_CN.md)

## 基于Azure AI平台的AI实现
本项目基于Azure AI 平台做了许多AI的实现。在使用之前，请确保已经正确引入了KEY和其它参数，请查阅代码以了解你可能需要的参数。

在使用这个项目之前，您可能需要阅读[Azure Cognitive Services documentation](https://learn.microsoft.com/en-us/azure/cognitive-services/)，以便对其功能有一个大致了解。

## 开发者原则
这是为参与2023年微软创新杯所做的项目的一部分。

在使用这个项目时，你应该确保遵循MIT许可，并且不要使用这个项目来参加2023年的微软创新杯。

# ###
# ###
## 接口
baseURL: example.com

# #########
### Speech to Text 语音转文字
#### 请求地址：
https://example.com/api/speech/speech2text

#### 请求方式：
POST ; enctype='multipart/form-data'

|key|vaule|
|---|---|
|audio_input|[audiofile](.mp3 or .wav)|

#### 请求实例:
audio_input:[123.wav]

#### 响应的返回实例:
```
{
    "code": "200",
    "msg": "成功",
    "data": "这是语音生成的内容。"
}
```

# #########
### Text to Speech 文字转语音
#### 请求地址：
https://example.com/api/speech/text2speech
#### 请求方式：
POST ; enctype='multipart/form-data'

|key|vaule|
|---|---|
|text_input|"str"|

#### 请求实例:
text_input:"语音生成"

#### 响应的返回实例:
[5123123213.wav]


# #########
### Customized Q&A
#### 请求地址：
https://example.com/api/speech/talk

#### 请求方式：
POST ; enctype='multipart/form-data'

|key|vaule|
|---|---|
|text_input|"str"|

#### 请求实例:
text_input:"支付宝怎么打开健康码"

#### 响应的返回实例:

```
{
    "code": "200",
    "msg": "成功",
    "input": "怎么打开健康码",
    "data": "首先打开【支付宝】客户端，然后在上方搜索栏搜索“健康码”，点击上方的【出示健康码】按钮，接着点击下方的【立即查看】按钮，申领电子健康卡后，点击上方的【电子健康卡】位置，进入【居民电子健康码】页面，再点击右上角的【…】图标，在弹出的选项栏点击【添加到桌面】选项，最后点击【立即添加】按钮即可。"
}
```

# #########
### Customized Q&A Audio
#### 请求地址：
https://example.com/api/speech/talk_audio

#### 请求方式：
POST ; enctype='multipart/form-data'

|key|vaule|
|---|---|
|text_input|"str"|

#### 请求实例:
text_input:"支付宝怎么打开健康码"

#### 响应的返回实例:
[5123123213.wav]


# #########
### Image Analysis 图像分析
#### 请求地址：
https://example.com/api/cv/image4analysis

#### 请求方式：
POST ; enctype='multipart/form-data'

|key|vaule|
|---|---|
|img_input|图像文件|

#### 响应的返回实例:

```
{
    "code": "200",
    "msg": "成功",
    "caption": "a sign on a pole",
    "caption-cn": "杆子上的标志",
    "tags": [
        "text",
        "outdoor",
        "sky",
        "sign",
        "street"
    ]
}
```
