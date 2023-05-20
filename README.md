<h1 style="text-align:center;">ChatGPT-CLI</h1>
<h3 style="text-align:center;">基于OpenAI API开发的命令行工具</h3>
<div style="text-align:center">
  <img src="./static/cover.png" alt="cover">
</div>


### 主要功能
· 文字聊天  
· 图片生成  
· 音频转文字  
· 一键启动  
· 聊天记录保存  
· 异步调用，快速响应
· 自动调整上下文，对话次数无限制
· 支持DIY参数

### 启动之前
1. 准备好你的 [OpenAI API Key](https://platform.openai.com/account/api-keys)
2. 在系统环境变量中新增一条变量```OPENAI_API_KEY```，变量值为你的[OpenAI API Key](https://platform.openai.com/account/api-keys)

### 启动项目
1. 下载项目到本地  
2. 安装依赖库 ```pip install -r requirements.txt```
3. 启动项目 ```python.exe main.py```

### CMD快速启动  
如果你需要在 CMD 中使用 chat 命令来快速启动项目，你需要进行如下操作：

1. 修改项目中的chat.bat文件，根据本地情况修改python的解释器目录和main.py文件目录
```angular2html
@echo off
D:\code\ChatGPT-CLI\Virtualenv\Scripts\python.exe D:\code\ChatGPT-CLI\main.py
PAUSE
```
2. 在系统环境变量PATH中新增chat.bat的地址，即可在cmd中输入chat命令快速启动项目 
<div style="text-align:center">
  <img src="./static/cmd_run.png" alt="cmd_run">
</div>

### PowerShell快速启动  
如果你需要在 PowerShell 中使用 chat 命令，你需要进行如下操作：

1. 打开 PowerShell，输入 ```$PROFILE```，按回车键。如果提示 “文件未找到”，那么你需要创建 PowerShell 配置文件。 创建一个新的配置文件，输入```New-Item $PROFILE –type file –force```。
建议右键运行 PowerShell 作为管理员。  
2. 用任意文本编辑器打开 PowerShell 配置文件(第一步创建的文件)
3. 将以下命令添加到文件末尾：```function chat {python.exe D:\code\ChatGPT-CLI\main.py}```,注意根据本地情况修改python解析器路径和main.py文件路径
4. 保存文件并关闭文本编辑器。

现在你可以在 PowerShell 中使用 chat 命令来快速运行该项目了。
<div style="text-align:center">
  <img src="./static/powershell_run.png" alt="powershell_run">
</div>

### 如何使用
该系统共有六个选项```chat``` ```file``` ```save``` ```image``` ```audio```，当程序提示```Next```时即可输入选项并进入对应的模式，输入```quit```可以退出该程序，也可以直接关闭程序:D，接下来将分别介绍各个选项的作用：  
#### ```chat```
进入文字聊天模式，如果没有选择对话记录文件，默认创建一个新的对话和对应的记录文件，输入```quit```返回主菜单
#### ```all```
打印当前系统保存的所有对话记录文件
#### ```set <file name>```
设置当前的对话记录文件，如果文件存在，则会缓存对话记录 
#### ```save```
保存当前的对话记录，通常不需要手动调用，因为对话会自动保存,保存路径为当前用户的Documents\chat_logs目录中，文件名为当前日期，文件名可以手动修改
#### ```image <prompt>```
输入图片描述，返回图片的url，该图片和url不会自动保存，需要用户手动下载保存
#### ```audio <file name>```
输入音频文件的**完整路径**，返回该音频翻译的文字内容

### DIY参数
修改conf/config.json文件来定制化你的聊天机器人:D
```json
{
  "ChatCompletionConfig": {
    "model": "gpt-3.5-turbo",
    "temperature": 1,
    "n": 1,
    "stream": true,
    "stop": "",
    "max_tokens": 2048,
    "presence_penalty": 0,
    "frequency_penalty": 0
  },
  "ImageConfig": {
    "n": 1,
    "size": "1024x1024",
    "response_format": "url"
  },
  "TranscriptionsConfig": {
    "model": "whisper-1",
    "response_format": "json"
  },
  "max_context_size": 5,
  "auto_modify_cons": true
}
```
```max_context_size``` 代表系统每次发送请求携带的上下文数量
```auto_modify_cons``` 代表系统在运行过程是否自动调整```conversations```的大小  
其余参数的具体含义参考[OpenAI API官网](https://platform.openai.com/docs/api-reference)

### 使用截图
<div style="text-align:center">
  <img src="./static/example1.png" alt="example1">
</div>
<div style="text-align:center">
  <img src="./static/example2.png" alt="example2">
</div>  
<div style="text-align:center">
  <img src="./static/example3.png" alt="example3">
</div>  
