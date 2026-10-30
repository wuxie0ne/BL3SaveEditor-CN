# BL3SaveEditor-CN

[简体中文](#简体中文) | [English](#english)

## 简体中文

BL3SaveEditor-CN 是 [FromDarkHell/BL3SaveEditor](https://github.com/FromDarkHell/BL3SaveEditor) 的简体中文版本，用于编辑《无主之地 3》的角色存档和个人档案。本项目在原版基础上提供中文界面、部分游戏名称和部件说明，以及 Windows 便携版构建。

### 下载与使用

1. 从本项目的 [Releases](https://github.com/wuxie0ne/BL3SaveEditor-CN/releases) 下载 `BL3SaveEditor-Portable.exe`，或下载并解压 `BL3SaveEditor-Portable.zip`。
2. 在 Windows 上运行程序。程序需要 .NET Framework 4.7.2 或兼容版本。
3. 点击“打开”，选择角色存档（通常为数字命名的 `.sav` 文件）或个人档案 `profile.sav`。
4. 修改后点击“保存”或“另存为”。**编辑前请先备份存档。**

当前部分游戏名称、部件代码、原始存档字段和第三方控件文本仍显示英文。受福说明中的“（数值）”是游戏动态填充的占位符，不代表实际数值。汉化来源、覆盖范围和维护方式见[游戏名称汉化说明](docs/game-names-zh-CN.md)。

**自动更新提示仍指向原版项目，可能引导下载英文版。** 请从本项目的 Releases 页面获取中文版更新。

### 构建与发布

在 GitHub Actions 中手动运行 `Build portable executable`，可以构建并下载便携版 artifact。发布时，先将指向目标提交的 Git tag 推送到 GitHub，再手动运行 `Release portable executable` 并填写该 tag；工作流会构建该版本并发布 EXE 和 ZIP。已有同名 Release 不会被覆盖；如果上传或发布失败，请检查是否留下 Release 草稿。

### 致谢与许可

感谢 [FromDarkHell](https://github.com/FromDarkHell) 和 [BL3SaveEditor 原项目](https://github.com/FromDarkHell/BL3SaveEditor)的所有贡献者，为本版本提供基础。感谢 [gibbed](https://github.com/gibbed) 提供的 [Borderlands3Dumps](https://github.com/gibbed/Borderlands3Dumps) 与 [Borderlands3Protos](https://github.com/gibbed/Borderlands3Protos)，以及 [apocalyptech](https://github.com/apocalyptech)、[AdonisUI](https://github.com/benruehl/adonis-ui)、[Extended WPF Toolkit](https://github.com/xceedsoftware/wpftoolkit) 和原项目的其他贡献者。

本项目使用 GNU General Public License v3.0；详见 [LICENSE](LICENSE)。

## English

BL3SaveEditor-CN is a Simplified Chinese edition of [FromDarkHell/BL3SaveEditor](https://github.com/FromDarkHell/BL3SaveEditor), a desktop editor for Borderlands 3 character saves and profiles. This fork adds a Chinese interface, translations for some game names and item parts, and Windows portable builds.

### Download and use

1. Download `BL3SaveEditor-Portable.exe` from this project's [Releases](https://github.com/wuxie0ne/BL3SaveEditor-CN/releases), or download and extract `BL3SaveEditor-Portable.zip`.
2. Run it on Windows with .NET Framework 4.7.2 or a compatible version installed.
3. Select “打开” (Open), then choose a character save (usually a numbered `.sav` file) or `profile.sav`.
4. Select “保存” (Save) or “另存为” (Save As) when finished. **Back up your saves before editing.**

Some game names, part identifiers, raw save fields, and third-party control text remain in English. “（数值）” in anointment descriptions is a placeholder for a value supplied by the game, not an actual value. See the [game name localization notes](docs/game-names-zh-CN.md) for sources, coverage, and maintenance details; the notes are in Chinese.

**The built-in update prompt still points to the original project and may offer the English version.** Download Chinese edition updates from this project's Releases page.

### Build and release

Run `Build portable executable` manually in GitHub Actions to build and download a portable artifact. To publish a release, push a Git tag pointing to the target commit, then run `Release portable executable` manually with that tag. The workflow builds the tagged source and publishes an EXE and ZIP. It does not overwrite an existing release for the same tag; check for a leftover draft if uploading or publishing fails.

### Credits and license

Thanks to [FromDarkHell](https://github.com/FromDarkHell) and all contributors to the original [BL3SaveEditor](https://github.com/FromDarkHell/BL3SaveEditor) for the foundation of this edition. Thanks also to [gibbed](https://github.com/gibbed) for [Borderlands3Dumps](https://github.com/gibbed/Borderlands3Dumps) and [Borderlands3Protos](https://github.com/gibbed/Borderlands3Protos), [apocalyptech](https://github.com/apocalyptech), [AdonisUI](https://github.com/benruehl/adonis-ui), [Extended WPF Toolkit](https://github.com/xceedsoftware/wpftoolkit), and the other contributors to the original project.

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
