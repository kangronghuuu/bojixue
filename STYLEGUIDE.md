# 《薄肌学》编写规范（写作组必读）

> 这是一本**模仿大学教材体例**的减脂科普书：语气是严肃的、术语是准确的、内容是权威的，只有插图和举例是抽象的。
> 笑点来自「用学术腔讲健身房黑话」，不来自网络热梗堆砌。读者笑完要能带走可执行的知识。

---

## 0. 项目结构

```
bojixue/
├── BOOK.json              # 页面清单（Lead 维护，写作者不要动）
├── css/book.css           # 设计系统（不要动）
├── pages/
│   ├── 00-front.html      # 封面/扉页/编者/栏目/目录（Lead）
│   ├── 01-intro.html      # 绪言（Lead，样例）
│   ├── 02-ch1.html        # 第一章（Lead，**请精读，作为体例范本**）
│   ├── 03-ch2.html        # 第二章（writer-a）
│   ├── 04-ch3.html        # 第三章（writer-a）
│   ├── 05-ch4.html        # 第四章（writer-b）
│   └── 06-ch5.html        # 第五章（writer-b）
├── assets/art/*.svg       # 插图（Lead / illustrator）
├── build/build.py         # 构建脚本（可自测）
└── STYLEGUIDE.md / BLUEPRINT.md
```

**只写你自己的 page 文件。** 不要改 `css/`、`BOOK.json`、别人的页面、`build/`。

---

## 1. 文体与语气

- 教科书口吻：客观、克制、有定义、有分类、有条件限定。第二人称可用，但不要写成小红书笔记。
- 每个论断尽量带**数字 + 条件**。例如：「每周减重 0.5%–1% 体重，通常比每周 2% 更能保住肌肉（Helms et al., 2014）」。
- 幽默方式：
  - 用学术语言描述荒诞日常（「体重秤在晚间表现出显著的情绪波动性」）。
  - 严肃的图表配一句冷面图注。
  - 在「思考与讨论」里提出读者无法反驳的问题。
  - 反例：不要写「家人们谁懂啊」「狠狠拿捏」「尊嘟假嘟」这类过气热梗；不要用 emoji。
- 中文标点：引号统一用「」；破折号用「——」；数字与单位之间不空格（如 `1.6 g/kg` 单位前可留细空格，正文里写成 `1.6 g/kg` 即可）。
- 英文术语首次出现给中文解释，如「渐进超负荷（progressive overload）」。不要整段英文。
- 不要编造文献。只使用 BLUEPRINT 里给出的事实与文献简写；拿不准的数字就写得保守（「约」「通常」）。

---

## 2. 页面结构（最重要）

每章固定 **6 页**，每页是**一个 `<section class="page">`**，顺序与 `data-key` 如下：

| 页 | 内容 | data-key | 必备属性 |
|---|---|---|---|
| ① 章首页 | 章号、章标题、导语、3 条「本章线索」、章插图 | `chN` | `data-ch="第N章 章名"` |
| ② 第一节 | 节标题 + 正文 + 图/表/栏 | `chNs1` | `data-ch` + `data-sec="第一节 …"` |
| ③ 第二节 | 同上 | `chNs2` | 同上 |
| ④ 第三节 | 同上 | `chNs3` | 同上 |
| ⑤ 实验活动 | 实验活动 N—N+1 | `chNexp` | `data-sec="实验活动 N—N+1"` |
| ⑥ 整理与提升·练习 | 表格 + 小结 + 5 道练习 | `chNend` | `data-sec="整理与提升 · 练习与应用"` |

> `data-ch` / `data-sec` 会由构建脚本自动生成页脚（章名 + 节名 + 页码），不要手写页脚。
> 页码由构建脚本自动编，正文从「绪言」= 1 开始。

字符预算（正文含栏目文字，不含标题/图注）：

- 节页：**600–850 字**（有 1 张图时取低值；无图可到 1000 字）
- 实验活动页：**550–700 字** + 2 个紧凑表格
- 整理与练习页：**650–800 字** + 1 个 6 行表格 + 5 题
- 章首页：导语 120–180 字 + 3 条线索各 30–45 字

宁可少 100 字，也不要溢出。溢出页面会被脚本标出来，必须修好。

---

## 3. 组件用法（直接复制）

### 3.1 章首页
```html
<section class="page page--chapter" data-key="ch2" data-ch="第二章 能量账本">
  <div class="ch-open">
    <div class="ch-band"></div>
    <div class="ch-kicker-row">
      <span class="ch-no">第 二 章　CHAPTER 02</span>
      <span class="ch-en">The Energy Ledger</span>
    </div>
    <h2 class="ch-title">能量账本<span style="display:block;font-family:var(--sans);font-size:11pt;font-weight:400;letter-spacing:.24em;color:var(--ink-3);margin-top:5mm;">摄入与消耗之间，只剩加减法</span></h2>
    <p class="ch-lead">……120–180 字……</p>
    <div class="ch-art"><figure class="fig" data-art="ch-open-2"></figure></div>
    <div class="ch-line">
      <div class="cell"><div class="cell-h">线索 01</div><p>……</p></div>
      <div class="cell"><div class="cell-h">线索 02</div><p>……</p></div>
      <div class="cell"><div class="cell-h">线索 03</div><p>……</p></div>
    </div>
  </div>
</section>
```

### 3.2 节页
```html
<section class="page" data-key="ch2s1" data-ch="第二章 能量账本" data-sec="第一节 摄入那一栏">
  <div class="sec-head">
    <div class="sec-kicker">第 一 节</div>
    <h3 class="sec-title">摄入那一栏<span class="tail">一句话副标题，10–16 字</span></h3>
  </div>
  <p class="lead-p" style="text-indent:2em;">……一句导语……</p>
  <h4>一、小标题</h4>
  <p class="indent">……</p>
  <h4>二、小标题</h4>
  <p class="indent">……</p>
  <h4>三、小标题</h4>
  <p class="indent">……</p>
  <figure class="fig" data-art="ch2-ledger" style="width:110mm;margin:4mm auto 3mm;">
    <figcaption><span class="fignum">图 2-1</span>一句冷面图注。</figcaption>
  </figure>
  <div class="box box--tight">
    <div class="box-head"><span class="ic">法</span>方法引导 · 标题</div>
    <p>……</p>
  </div>
</section>
```

- 正文段落用 `<p class="indent">`（首行缩进）；导语用 `<p class="lead-p" style="text-indent:2em;">`。
- 小标题 `<h4>一、…</h4>`，每页 2–3 个，别超过 3 个。
- 数字强调用 `<strong>`；讽刺性强调用 `<em>`（会变珊瑚色，**慎用，每页最多 1 处**）。

### 3.3 图片（占位）
```html
<figure class="fig" data-art="ch3-plate" style="width:112mm;margin:4mm auto 3mm;">
  <figcaption><span class="fignum">图 3-1</span>……</figcaption>
</figure>
```
- **只能使用 BLUEPRINT 分配给你的 data-art 名**，不要自造，否则美术无法对应。
- `width` 建议 100–118mm（居中）或 60–64mm（右侧浮动 `class="fig fig--right"`）。
- 每页最多 1 张图。没图就用表或栏目填版面。

### 3.4 表格
```html
<table class="tbl">
  <thead><tr><th style="width:22%;">方法</th><th>要点</th><th style="width:28%;">备注</th></tr></thead>
  <tbody>
    <tr><td>……</td><td>……</td><td>……</td></tr>
  </tbody>
</table>
```
每章至少 1 个表格（节页或整理页都可以）。

### 3.5 栏目框
```html
<div class="box box--tight">
  <div class="box-head"><span class="ic">思</span>思考与讨论</div>
  <p>……</p>
</div>
```
`class` 变体：`box--warn`（注意/警示，珊瑚色）、`box--data`（数据/冷知识，橄榄色）、`box--kai`（楷体，用于引文/观察）、`box--flat`（虚线，用于研究与实践）。
`<span class="ic">` 里放 1 个汉字即可：观 测 思 法 验 注 图 练 研 冷 数。

### 3.6 边注
```html
<div class="note">
  <div class="note-h">记录条件</div>
  ……楷体短句，1–2 行……
</div>
```

### 3.7 练习
```html
<ol class="ex">
  <li>……</li>
  <li>……</li>
</ol>
```
整理页固定 5 题；题目要具体、可计算或可操作，不要「谈谈你的感受」。

### 3.8 数据条（可选，节页用）
```html
<div class="data-row">
  <div class="data-item"><div class="data-num">1.6<small>g/kg</small></div><div class="data-label">蛋白质摄入下限</div></div>
  …
</div>
```
最多 3 项，且必须紧跟解释它的正文。

---

## 4. 每章必备清单

- [ ] 章首页 1 页（含 `ch-open-N` 插图，不要写图注）
- [ ] 3 个节页（各 1 张指定插图或表格）
- [ ] 实验活动页：2 个实验（目的/材料/步骤/记录表/讨论，或适当合并）
- [ ] 整理与提升 + 练习页：1 个 6 行表 + 小结 + 5 题 + 「研究与实践」虚线框
- [ ] 至少 1 个 `box--data` 或 `box--warn`，内含真实数字 + 文献简写（如 `（Morton et al., 2018）`）
- [ ] 至少 2 处冷面幽默（图注、栏目、例句均可）
- [ ] 全章数字与 BLUEPRINT 一致；不确定的加「约」「通常」

---

## 5. 自测命令（写完必须跑）

```bash
cd bojixue
# 1) 生成预览 HTML + PDF + 溢出检查（把文件名换成你的）
~/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 build/build.py \
  --fragments pages/03-ch2.html --out build/preview-ch2.html --pdf /tmp/ch2.pdf --audit

# 2) 看页数与是否溢出（最后一列必须是 AUDIT OK）
pdfinfo /tmp/ch2.pdf | grep Pages
# 3) 把 PDF 渲染成图片，逐页自查（重点看 6 页是否都满、有没有压字）
pdftoppm -r 80 -png /tmp/ch2.pdf /tmp/ch2pg
```

`--audit` 输出里有 `AUDIT OK` 才算通过；出现 `页面序号:data-key` 说明该页内容超出版心，必须删字/删框/缩图。

> 注意：预览文件的页码从 1 开始、目录占位显示 `??`，都正常；最终合书时由 Lead 统一处理。

---

## 6. 交稿

- 完成后在共享任务里 `complete`，并给 Lead 发一条消息：写了哪些文件、每章字数、`--audit` 结果、引用了哪些文献。
- 如果时间不够：优先保证 **6 页完整 + audit OK**，宁可文字略少，不要缺页或溢出。
