# 感恩节文章发布说明

## 文件用途

- `index.md`：完整正文，10个重点单词及2句表达均附美式音标；发音链接对应本地WAV。
- `read-and-listen.html`：浏览器可播放版。音频全部内嵌，不依赖网络或浏览器语音库。支持逐词播放、慢速、10词连读与停止。请用浏览器打开完整文件；文件预览器可能不执行播放脚本。
- `wechat-copy.html`：公众号排版稿。用浏览器打开后，复制文章内容到公众号编辑器。音频位置标为【在此插入音频：文件名】，须在后台换成真正的音频组件。
- `audio/01-…` 至 `audio/12-…`：10个词、2句话的独立发音文件。
- `audio/00-vocabulary-all.wav`：10词连读音频，每词之间留出约1秒停顿。
- `thanksgiving-publish-kit.zip`：上述正文、排版稿、播放页、音频及本说明的打包版本。

## 封面

`assets/cover.png` 是本次用内置 imagegen 生成的横版封面，可上传至公众号封面位置。生成提示词保存在 `assets/cover.prompt.txt`。每个词配有一张表达词义的独立插画，放在 `assets/vocabulary/`，正文显示为64×64像素，发布用小图文件为192×192像素（`*-small.png`），适合高清屏。原始生成图片保留在工作目录，发布包仅收录小图。所有小插画由内置 imagegen 生成，提示词保存在该目录的 `prompts.json`。

## 在公众号内保留播放功能

1. 打开 `wechat-copy.html`，复制文章到公众号后台的新建图文正文。
2. 上传 `assets/vocabulary/` 中文件名以 `-small.png` 结尾的10张PNG插画，按文件名替换对应的图片位置，宽度约64像素；从本地网页复制不能保证图片会自动传入公众号素材库。
3. 在后台的音频入口上传 `audio/` 中需要的文件（以账号实际支持的格式、容量及组件数量为准）。
4. 按正文中的文件名逐个插入原生音频组件，再删除相应的【在此插入音频】提示。每段音频上方保留“发音：对应单词”，下方的分隔线表示当前词条结束；上传音频时也建议把标题设为对应单词。
5. 给手机发送预览，检查音频与单词一一对应，并逐个点击试听。
6. 检查时间表述、标题和排版后发布。

如果账号的单篇音频组件数量不足，可以插入一条 `00-vocabulary-all.wav`，同时将逐词播放版部署到可访问的HTTPS地址，并按账号可用能力设置“阅读原文”入口；这时读者进入播放页后才能逐词点读。当前交付的是本地文件，尚未部署或发布到公众号。

**复制HTML正文不会把自定义JavaScript按钮变成公众号播放器。** 因此，排版稿只保留清楚的音频插入提示，真正的播放组件要在公众号后台添加。

后台插入音频的参考：[壹伴：公众号音频插入方式](https://yiban.io/blog/36841)。后台界面和账号权限可能不同，以实际编辑器为准。

## 正文引用格式

正文使用 `[1]`、`[2]` 等编号，置于句末标点之前（例如“日期已固定[1]。”），文末“参考文献”列出书目与完整URL。排版稿中的文献地址为纯文本，不含可点击的超链接。

## 英文来历与书摘

来历使用简短英文，并附中文参考。书摘选自亲历者 Edward Winslow 的书信，收于 *Mourt’s Relation*（伦敦，1622年），第61页。正文逐字摘录22词，采用 Pilgrim Hall Museum 提供的现代拼写版本。英文来历概述是据史料编写的补充说明，与原文摘录分开标识。

核查链接：[Pilgrim Hall Museum 的原文及现代拼写转录](https://www.pilgrimhall.org/thanksgiving-national-day-of-mourning/the-first-thanksgiving/)；[耶鲁大学出版社文章的书目脚注](https://yalebooks.yale.edu/2014/11/27/the-evolution-of-thanksgiving/)。亲历者记录仅代表殖民者视角，正文保留了对当代原住民不同看法的简短说明。

## 发音说明

采用 Windows 自带的 Microsoft Zira Desktop（en-US）合成语音，非真人录音，非剑桥词典原声。音频已生成，可直接使用。音标采用常见美式读法，不逐一标记美式闪音等语音细节；整句提供参考音标，实际朗读可能存在弱读差异。

词汇参考：[剑桥词典](https://dictionary.cambridge.org/)。日期参考：[美国人事管理局2026年节假日表](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/)。

## 重新生成

在仓库根目录运行：

```powershell
& .\articles\thanksgiving\export-small-pictures.ps1
python articles/thanksgiving/build.py --prepare
& .\articles\thanksgiving\generate-audio.ps1
python articles/thanksgiving/build.py
node --check articles/thanksgiving/player-check.js
```

生成脚本会检查独立音频可读取、时长合理且并非全静音。重新生成需要Windows的System.Speech和Microsoft Zira Desktop语音。
