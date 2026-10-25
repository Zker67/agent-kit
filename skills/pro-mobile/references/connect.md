# 连接设备

mobile-mcp 和命令路线都要先让电脑看到设备。USB 调试和无线调试是同一条真机路线：连好后在 `adb devices` 中都表现为一个序列号，USB 是设备序列号，无线是 `<ip>:<port>`，后续用法完全相同。

开启开发者选项、在手机上点授权、输入配对码这些步骤由用户在手机上完成；AI 说明步骤、运行检查命令。

## 检查

```bash
adb devices -l
```

| 状态 | 含义 | 处理 |
|---|---|---|
| `device` | 已连接且已授权 | 可以使用 |
| `unauthorized` | 手机上还没允许这台电脑调试 | 请用户解锁手机，在“允许 USB 调试吗？”对话框中点允许；没弹出时拔插一次或在开发者选项中撤销授权后重连 |
| `offline` | 连接异常 | 重新插拔或重连；仍不行时 `adb kill-server` 后再 `adb devices` |
| 列表为空 | 没有识别到设备 | 按下面对应方式检查 |

`adb` 不在 PATH 中时，请用户安装 Android SDK Platform Tools 并把目录加入 PATH，新开终端后再检查。

## 开启开发者选项（Android 共用）

1. 设置 → 关于手机 → 连续点“版本号”7 次。不同厂商位置不同，可在设置里搜索“版本号”。
2. 返回设置，进入“开发者选项”（常在“系统”或“更多设置”中）。

## USB 调试

1. 开发者选项中打开“USB 调试”。部分国产系统还需打开“USB 安装”“USB 调试（安全设置）”，否则无法安装 App 或模拟点击。
2. 用支持数据传输的线连接电脑，USB 模式选“文件传输”时更容易被识别。
3. 手机弹出授权对话框时点允许，可勾选“始终允许”。
4. `adb devices -l` 显示 `device` 即完成。

Windows 上仍识别不到时，通常是缺少手机厂商的 USB 驱动（Google 设备用 Google USB Driver）。

## 无线调试（Android 11 及以上，推荐）

电脑和手机须在同一局域网。

1. 开发者选项中打开“无线调试”，进入其详情页。
2. 点“使用配对码配对设备”，记下弹窗中的 `<ip>:<配对port>` 和六位配对码。
3. 在电脑上配对（只需一次）：

   ```bash
   adb pair <ip>:<配对port> <配对码>
   ```

4. 连接。注意这里用的是“无线调试”详情页主界面显示的 `<ip>:<port>`，与配对弹窗中的 port 不同：

   ```bash
   adb connect <ip>:<port>
   ```

5. `adb devices -l` 显示 `<ip>:<port>  device` 即完成。

已配对的设备在同一网络下有时会通过 mDNS 自动连上，可用 `adb mdns services` 查看。

### 掉线与重连

- 手机休眠、关闭无线调试、切换网络或重启后，连接会断开，port 也可能变化。重新进入“无线调试”详情页看当前 `<ip>:<port>`，再 `adb connect`；已配对过不需要重新 pair。
- 操作中报找不到设备时先重新 `adb devices`，序列号变了就用新的序列号。
- 用完可 `adb disconnect <ip>:<port>`，并在手机上关闭无线调试。

### 安全

- 只在可信的局域网中开启无线调试，公共 Wi-Fi 下不用。
- 不再使用的电脑可在手机“无线调试 → 已配对的设备”中移除。

## 无线调试（Android 10 及以下）

先用 USB 连接并授权，然后：

```bash
adb tcpip 5555
adb connect <手机 ip>:5555
```

之后可以拔线。这种方式不经过配对，监听会一直保持到手机重启，只在可信网络中使用；用完运行 `adb usb` 切回 USB 模式。

## Android 模拟器

```bash
emulator -list-avds
emulator -avd <名称>
```

也可以在 Android Studio 的 Device Manager 中启动。启动后在 `adb devices` 中显示为 `emulator-5554` 一类序列号。`emulator` 位于 Android SDK 的 `emulator/` 目录，不在 PATH 中时用完整路径或从 Android Studio 启动。

## iOS（仅 macOS）

- 模拟器：`xcrun simctl list devices` 查看，`xcrun simctl boot "<设备名>"` 启动，`open -a Simulator` 显示窗口。
- 真机：用 USB 连接，在手机上点“信任此电脑”；iOS 16 及以上还需在“设置 → 隐私与安全性”中打开“开发者模式”。`xcrun devicectl list devices` 可查看已连接设备。
- Windows 与 Linux 无法连接 iOS 设备进行调试。
