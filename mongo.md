# 如何在 wsl 中连接 windows 中的 mongodb

1. 确认 wsl 的 ip 地址，打开 powershell，执行命令

```
ipconfig
```

找到 `wsl` 所对应的 `ip` 地址，在我的电脑中是 `172.19.160.1`

此时可以尝试在 `wsl` 中

```
ping 172.19.160.1
```

若 ping 不通，则需要修改防火墙，防火墙修改包括两个部分

**1**
打开 Windows Defender 防火墙 设置。
点击左侧的 启用或关闭 Windows Defender 防火墙。
临时关闭防火墙后，测试是否可以从 WSL 连接到 Windows。

**2**
允许 ICMP 请求：ping 使用的是 ICMP 协议，Windows 防火墙可能阻止了 ICMP 请求。你可以临时允许 ICMP 请求（用于 ping 测试）：
打开 Windows Defender 防火墙。
点击左侧的 高级设置。
在入站规则中，找到 文件和打印共享（回显请求 - ICMPv4-In） 规则，启用该规则。


后再 powershell 中执行

```
net stop LxssManager
net start LxssManager
```

可以访问后，需要在 wsl 中安装 mongo-client，可以通过官网安装 https://www.mongodb.com/try/download/shell

下载后执行

```
tar -xvzf <downloaded_file>.tgz
sudo mv <extracted_folder>/bin/mongosh /usr/local/bin/
```

查看版本
```
mongosh --version
```

### 在 windows 修改 mongod 配置 bindip

找到 mongod.conf 文件，并修改 bindip，我的 mongod.conf 文件位于 `C:\Program Files\MongoDB\Server\7.0\bin\mongod`

确保它允许外部连接

```
net:
  bindIp: 0.0.0.0
  port: 27017
```

修改该文件后需要重启 `mongodb` 服务，在 `powershell` 中执行

```
net stop MongoDB
net start MongoDB
```

以上修改完毕后，尝试在 `wsl` 中执行

```
mongosh --host 172.19.160.1 --port 27017
```

即可在 wsl 中访问 windows 中的 mongodb 服务