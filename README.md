# CamCamNeed 看看你的
Automatically generate a screenshot with information for color grading as a watermark based on file properties.
自动生成截图并加上调色相关的信息作为“相机水印”效果，基于文件属性自动识别。

# 安装
请将 CamCamNeed.py 拷贝至达芬奇指定的脚本存放目录下
macOS: /Users/{你的用户名}/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
Windows: C:\Users{你的用户名}\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts

请使用 v18.5 及更高版本
在菜单：工作区(Workspace) > 脚本(Scripts) 中即可找到
仅支持在达芬奇内使用，不支持在外部运行

用法
- 找到合适的一帧，打开此工具，填好必要的信息，按下快门即可生成
- 通过文件属性自动识别机型和色彩空间，当然会有很多不能识别的情况，此时可以手动进行选择
- 色彩空间和机型，手动选择其一会自动匹配另一个，毕竟它们几乎不可能混搭出现
- 其他内容可根据需要自行修改

需要
本工具仅支持 达芬奇18.5 及更高版本
本工具需要第三方库 Pillow，具体安装方式请参考网上各路教程