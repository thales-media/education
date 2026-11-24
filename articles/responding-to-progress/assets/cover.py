"""Render hypothetical score paths, not observational data."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path as CurvePath
from matplotlib.patches import PathPatch

OUT = Path(__file__).resolve().parent
REGULAR = FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
BOLD = FontProperties(fname='C:/Windows/Fonts/msyhbd.ttc')
plt.rcParams['svg.fonttype'] = 'path'
BG, INK = '#FAF8F2', '#263D39'
fig = plt.figure(figsize=(10, 4.25), dpi=240, facecolor=BG)
fig.text(.085, .845, '考到90分之后', fontproperties=BOLD, fontsize=29, color=INK)
fig.text(.09, .755, '先补给，再出发', fontproperties=REGULAR, fontsize=15, color='#62716A')
ax = fig.add_axes([.13, .205, .70, .47], facecolor=BG)
ax.set_xlim(-.12, 2.35)
ax.set_ylim(60, 101)
ax.set_yticks([70, 80, 90, 100])
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['上一次', '这一次', '下一次'], fontproperties=REGULAR, fontsize=12)
ax.tick_params(axis='both', colors='#8B958F', length=0, pad=10)
ax.grid(axis='y', color='#E5E7DE', linewidth=.7)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.text(-.12, 104, '分数', fontproperties=REGULAR, color='#8B958F', fontsize=9)

def curve(points, color, dashed=False):
    path = CurvePath(points, [CurvePath.MOVETO, CurvePath.CURVE4, CurvePath.CURVE4, CurvePath.CURVE4])
    patch = PathPatch(path, facecolor='none', edgecolor=color, linewidth=3.4,
                      capstyle='round', linestyle=(0, (3, 2)) if dashed else '-')
    ax.add_patch(patch)

curve([(0, 80), (.35, 80), (.65, 90), (1, 90)], INK)
ax.scatter([0, 1], [80, 90], s=58, color=INK, zorder=5, edgecolors=BG, linewidth=1.8)
ax.annotate('80', (0, 80), xytext=(0, -24), textcoords='offset points',
            ha='center', fontsize=15, fontproperties=BOLD, color=INK)
ax.annotate('90', (1, 90), xytext=(0, 13), textcoords='offset points',
            ha='center', fontsize=15, fontproperties=BOLD, color=INK)
for endpoint, color in [(95, '#CF5850'), (90, '#33846C'), (70, '#92989C')]:
    curve([(1, 90), (1.35, 90), (1.65, endpoint), (2, endpoint)], color, True)
    ax.scatter([2], [endpoint], s=58, color=color, zorder=5, edgecolors=BG, linewidth=1.8)
    ax.text(2.1, endpoint, str(endpoint), color=color, fontsize=18,
            fontproperties=BOLD, va='center')
fig.text(.09, .075, '路径示意 · 非真实学生数据 · 虚线为假设走向',
         fontproperties=REGULAR, fontsize=9, color='#90978F')
fig.savefig(OUT / 'cover.png', dpi=240, facecolor=BG)
fig.savefig(OUT / 'cover.svg', facecolor=BG)
plt.close(fig)
