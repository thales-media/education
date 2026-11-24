# 教育与成长

结合研究文献、数据与家庭实践，记录关于学习和教育的思考。

## 文章目录

| 日期 | 文章 | 状态 |
| --- | --- | --- |
| 2026-11-24 | [孩子渐渐长大，我想开始写写教育](articles/introduction/index.md) | 草稿 |
| 2026-11-24 | [孩子从80多分考到90分，先别急着要求95分](articles/responding-to-progress/index.md) | 草稿 |

## 文件组织

每篇文章使用独立目录，正文统一命名为 `index.md`，配图放在同目录的 `assets/` 中。

```text
articles/
  introduction/
    index.md
    assets/
      cover.png
      cover.prompt.txt
  responding-to-progress/
    index.md
    editorial-notes.md
    assets/
      cover.png
      cover.svg
      cover.py
      boss-rest-and-recover-v2.png
      dragon-outcomes.png
      ...
```

- 正文通过相对路径引用配图，例如 `![配图说明](assets/cover.png)`。
- 图片、数据和其他随文资料与文章一起保存，便于迁移和同步。
- 多篇文章共用的标识等资源，后续可另放根目录的 `assets/`。
- 涉及自家孩子时使用“中学”等宽泛表述，不写具体年级、学校、班级、分数排名及可识别的照片；案例只保留讨论所需的背景，避免组合细节识别出个人。
- `editorial-notes.md` 记录查证和编辑过程，不随文章正文发布。
- AI 配图保留生成提示词，并在发布时说明其为生成插画。
