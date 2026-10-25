# 命令路线（不装 MCP）

用户不想装 mobile-mcp、宿主没有项目级 MCP 配置，或只需一两条命令时，直接用 `adb`（Android）或 `xcrun simctl`（iOS 模拟器，仅 macOS）。设备连接见 [连接设备](./connect.md)。

## 通用约定

- 有多台设备时每条命令都带 `-s <序列号>`，或先 `export ANDROID_SERIAL=<序列号>`。下文省略 `-s`。
- 设备上的临时文件放在 `/sdcard/` 下，拉回电脑后删除设备上的副本。
- 拉回电脑的截图、界面树、录屏放在系统临时目录或用户指定位置，不随手写进项目目录。

## 看界面

截图：

```bash
adb exec-out screencap -p > screen.png
```

Windows PowerShell 5 的 `>` 会损坏二进制内容，改用：

```powershell
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png
adb shell rm /sdcard/screen.png
```

界面元素树（相当于 mobile-mcp 的元素列表）：

```bash
adb shell uiautomator dump /sdcard/ui.xml
adb pull /sdcard/ui.xml
adb shell rm /sdcard/ui.xml
```

XML 中每个节点有 `text`、`content-desc`、`resource-id` 和 `bounds="[x1,y1][x2,y2]"`；点击坐标取中心 `((x1+x2)/2, (y1+y2)/2)`。界面在动画中时 dump 可能失败，稍等重试。

当前前台 App 和页面：

```bash
adb shell dumpsys activity activities | grep -E "topResumedActivity|mResumedActivity"
```

## 操作

```bash
adb shell input tap <x> <y>
adb shell input swipe <x1> <y1> <x2> <y2> 300      # 最后一个参数是毫秒，同一点长按也用它
adb shell input text "hello%sworld"                 # 空格写成 %s；不支持中文
adb shell input keyevent KEYCODE_BACK               # 还有 KEYCODE_HOME、KEYCODE_ENTER、KEYCODE_APP_SWITCH
```

中文或长文本可先写入剪贴板再粘贴，或改用 mobile-mcp 的 `mobile_type_keys`。每次操作后重新 dump 或截图确认结果。部分国产系统需在开发者选项中打开“USB 调试（安全设置）”后 `input` 才生效。

## App

```bash
adb install -r app-debug.apk                                     # -r 保留数据覆盖安装
adb shell pm list packages | grep <关键词>
adb shell monkey -p <包名> -c android.intent.category.LAUNCHER 1   # 不知道 Activity 名时启动 App
adb shell am start -n <包名>/<Activity>
adb shell am start -a android.intent.action.VIEW -d "<deep link 或 URL>"
adb shell am force-stop <包名>
```

以下会丢失数据，真机上先说明影响并取得同意：

```bash
adb uninstall <包名>
adb shell pm clear <包名>
```

## 日志与崩溃

```bash
adb logcat --pid=$(adb shell pidof -s <包名>)   # 只看该 App；App 重启后 pid 会变
adb logcat "*:E"                                 # 只看错误
adb logcat -b crash                              # 崩溃缓冲区
adb logcat -d -t 500 > logcat.txt                # 导出最近 500 行后退出
```

`adb logcat` 会持续输出，在宿主中运行时加 `-d`（输出后退出）或用后台任务并限时，避免卡住会话。

## 本地开发服务器映射到手机

让手机上的 `localhost:<port>` 访问电脑上的开发服务器，USB 和无线连接都适用：

```bash
adb reverse tcp:8081 tcp:8081      # React Native Metro；Vite 等换成对应 port
adb reverse --list
adb reverse --remove-all
```

之后可在手机浏览器打开 `http://localhost:<port>`，或让 App 连接本机接口。

## 录屏

```bash
adb shell screenrecord --time-limit 30 /sdcard/demo.mp4
adb pull /sdcard/demo.mp4
adb shell rm /sdcard/demo.mp4
```

单次最长 180 秒；录屏可能包含隐私，保存位置先确认。

## iOS 模拟器（仅 macOS）

```bash
xcrun simctl list devices booted
xcrun simctl io booted screenshot screen.png
xcrun simctl install booted <App.app 路径>
xcrun simctl launch booted <bundle id>
xcrun simctl terminate booted <bundle id>
xcrun simctl openurl booted "<URL 或 deep link>"
xcrun simctl spawn booted log stream --predicate 'process == "<App 名>"'
```

`simctl` 没有点击和读取元素树的命令；iOS 需要界面交互时使用 mobile-mcp。iOS 真机构建与安装交给 Xcode 或项目框架（如 `flutter run`、`npx expo run:ios`）。
