## Docker Desktop安装与简单使用

### Window下Docker Desktop安装

安装包下载地址：https://hub.docker.com/editions/community/docker-ce-desktop-windows

Docker依赖于已存在并运行的Linux内核环境，对于部分版本的Win10系统，可以选择安装Hyper-V满足环境依赖，参考：https://www.runoob.com/docker/windows-docker-install.html



安装完成后启动Docker Desktop，遇到WSL2未完全安装的错误，选择更新并配置WSL2

更新WSL2 Linux kernel：https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package

以管理员权限打开一个PowerShell窗口

输入并重启：dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

输入并重启：dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

输入并重启：wsl --set-default-version 2



打开Microsoft Store，选择偏好的Linux分发版，这里选择Ubuntu

获取后启动，遇到The attempted operation is not supported for the type of object referenced（参考的对象类型不支持尝试的操作）

以管理员身份运行CMD

输入并重启：netsh winsock reset

随后正常启动Docker Desktop，运行“docker run hello-world”测试





### MacOS下Docker Desktop安装





