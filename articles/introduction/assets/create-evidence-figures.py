"""Create original method diagrams and a clearly labelled fictional data example."""
import csv
from pathlib import Path
from statistics import mean
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

OUT = Path(__file__).resolve().parent
REG = FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
BOLD = FontProperties(fname='C:/Windows/Fonts/msyhbd.ttc')
BG, INK, TEAL, MUTED = '#FAF8F2', '#263D39', '#33846C', '#75847B'
plt.rcParams['svg.fonttype'] = 'path'

def label(ax, x, y, text, size=14, color=INK, bold=False, **kwargs):
    return ax.text(x, y, text, fontproperties=BOLD if bold else REG,
                   fontsize=size, color=color, **kwargs)

fig = plt.figure(figsize=(10, 4.6), dpi=240, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
label(ax, .065, .85, '用文献支撑观点', size=27, bold=True)
label(ax, .067, .75, '从家长的具体问题出发，让依据可以被查阅', size=13, color=MUTED)
steps = [
    (.065, '01', '提出问题', '孩子遇到了什么？', '先把问题说清楚'),
    (.375, '02', '查阅文献', '读原文 · 看方法', '比较不同研究的结论'),
    (.685, '03', '说明依据', '标出处 · 讲条件', '分清研究与个人经验'),
]
for x, number, title, line1, line2 in steps:
    ax.add_patch(FancyBboxPatch((x, .23), .25, .41, boxstyle='round,pad=0.008,rounding_size=0.023',
                               facecolor='#FFFFFF', edgecolor='#DDE5DB', linewidth=1.1))
    ax.add_patch(Circle((x+.042, .565), .027, facecolor=TEAL, edgecolor='none'))
    label(ax, x+.042, .565, number, size=10, color='white', bold=True, ha='center', va='center')
    label(ax, x+.022, .455, title, size=20, bold=True)
    label(ax, x+.022, .355, line1, size=12)
    label(ax, x+.022, .285, line2, size=11, color=MUTED)
for start in [.326, .636]:
    ax.add_patch(FancyArrowPatch((start, .43), (start+.035, .43), arrowstyle='-|>',
                                mutation_scale=16, linewidth=1.7, color=TEAL))
label(ax, .067, .10, '看研究对象，也看研究方法与适用范围', size=12, color=MUTED)
fig.savefig(OUT/'literature-evidence.png', dpi=240, facecolor=BG)
fig.savefig(OUT/'literature-evidence.svg', facecolor=BG)
plt.close(fig)

groups = {'A': [], 'B': []}
with (OUT/'statistics-example.csv').open(encoding='utf-8', newline='') as source:
    for row in csv.DictReader(source):
        groups[row['group']].append(float(row['score']))
assert mean(groups['A']) == mean(groups['B']) == 80
fig = plt.figure(figsize=(10, 4.8), dpi=240, facecolor=BG)
fig.text(.065, .845, '用统计分析看清差异', fontproperties=BOLD, fontsize=27, color=INK)
fig.text(.067, .75, '两组虚构分数，平均值都是80分', fontproperties=REG, fontsize=14, color=MUTED)
ax = fig.add_axes([.16, .28, .76, .34], facecolor=BG)
ax.set_xlim(54, 106); ax.set_ylim(-.45, 1.45)
ax.set_yticks([1, 0]); ax.set_yticklabels(['示例A', '示例B'], fontproperties=BOLD, fontsize=14, color=INK)
ax.set_xticks([60, 70, 80, 90, 100]); ax.tick_params(axis='both', length=0, pad=10, labelsize=12, colors=MUTED)
for s in ax.spines.values(): s.set_visible(False)
ax.grid(axis='x', color='#E0E5DC', linewidth=.8)
ax.set_axisbelow(True)
ax.axvline(80, color='#C78B43', linestyle=(0, (3, 3)), linewidth=1.8, zorder=2)
for group, y, color in [('A', 1, TEAL), ('B', 0, '#657F9C')]:
    scores=groups[group]
    ax.plot([min(scores), max(scores)], [y, y], linewidth=2, color=color, alpha=.45, zorder=3)
    ax.scatter(scores, [y]*len(scores), s=105, color=color, edgecolors=BG, linewidth=1.3, zorder=4)
ax.text(80, 1.47, '平均值 80', fontproperties=BOLD, color='#B47A33', fontsize=11, ha='center')
fig.text(.067, .135, '同样的平均值，可能对应很不一样的分布。', fontproperties=REG, fontsize=13, color=INK)
fig.text(.067, .055, '虚构数据 · 每组5个数值 · 仅演示统计方法，不代表真实学生或研究结果',
         fontproperties=REG, fontsize=9, color=MUTED)
fig.savefig(OUT/'statistics-distribution.png', dpi=240, facecolor=BG)
fig.savefig(OUT/'statistics-distribution.svg', facecolor=BG)
plt.close(fig)
