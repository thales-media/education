"""Build the article and standalone audio reader using local WAV recordings."""
from pathlib import Path
import base64
import html
import json
import re
import sys
import wave
import struct
import zipfile

ROOT = Path(__file__).resolve().parent
TITLE = '感恩节英语｜10个单词，把感谢说出来'
WORDS = [
    ('Thanksgiving', 'ˌθæŋksˈɡɪvɪŋ', '感恩节', '开头的 /θ/ 要轻轻送气，别读成 /s/。'),
    ('harvest', 'ˈhɑːrvɪst', '收获；丰收', '从秋日丰收，想到一年里的成长与收获。'),
    ('turkey', 'ˈtɝːki', '火鸡', '美国感恩节餐桌上的代表性食物。'),
    ('pumpkin', 'ˈpʌmpkɪn', '南瓜', '做成南瓜派，是常见的节日甜点。'),
    ('cranberry', 'ˈkrænberi', '蔓越莓', '酸甜的蔓越莓酱，常用来搭配火鸡。'),
    ('feast', 'fiːst', '盛宴', '形容一顿丰盛的大餐。'),
    ('thankful', 'ˈθæŋkfəl', '感激的；心怀感谢的', '想到值得感谢的人和事，就可以用上它。'),
    ('grateful', 'ˈɡreɪtfəl', '感激的', '常用来表达对他人帮助的感谢。'),
    ('gratitude', 'ˈɡrætətuːd', '感激之情；感恩', '这是名词；前面两个词是形容词。'),
    ('bless', 'bles', '祝福；保佑（动词）', '为他人祈愿平安与幸福。'),
]
SENTENCES = [
    ('Happy Thanksgiving!', 'ˈhæpi ˌθæŋksˈɡɪvɪŋ', '感恩节快乐！', ''),
    ("I'm grateful for your help.", 'aɪm ˈɡreɪtfəl fər jʊr help', '谢谢你的帮助。', ''),
]
ITEMS = []
for i, (text, ipa, meaning, tip) in enumerate(WORDS + SENTENCES, 1):
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    ITEMS.append(dict(id=f'{i:02d}-{slug}', text=text, ipa=ipa, meaning=meaning, tip=tip,
                      picture=f'assets/vocabulary/{slug}-small.png',
                      file=f'audio/{i:02d}-{slug}.wav'))
(ROOT / 'audio').mkdir(exist_ok=True)
(ROOT / 'audio-manifest.json').write_text(json.dumps(ITEMS, ensure_ascii=False, indent=2), encoding='utf-8')

INTRO = [
    '感恩节，适合认识一种节日文化，也适合学着把感谢说具体。和孩子一起听一听、读一读这10个词吧。',
]
DATE = '美国感恩节定在每年11月的第四个星期四。计算时，找到11月的第一个星期四，再加21天即可，因此日期总在11月22日至28日之间。2026年是11月26日[1]。'
HISTORY = [
    'In the autumn of 1621, English settlers at Plymouth and Wampanoag people shared a harvest celebration. This gathering later became part of the story of Thanksgiving[2].',
    'The national holiday developed over time. Abraham Lincoln proclaimed a national day of thanksgiving in 1863. In 1941, a law fixed the holiday on the fourth Thursday of November[4]. For some Native people, the day is also a time for mourning and remembrance[5].',
]
HISTORY_TRANSLATION = '1621年秋，普利茅斯的英国殖民者与万帕诺亚格原住民共同庆祝丰收，这次聚会后来成为感恩节故事的一部分。全国性节日则逐步形成：1863年林肯宣布全国感恩日，1941年的法律固定了日期。对一些原住民而言，这一天也是悼念与追思之日。'
QUOTE = 'our harvest being gotten in, our governor sent four men on fowling, that so we might after a special manner rejoice together'
QUOTE_TRANSLATION = '收成入仓后，总督派出四人猎鸟，好让我们以一种特别的方式共同庆祝。'
QUOTE_SOURCE = 'Edward Winslow, “A Letter Sent from New England,” 收于 Mourt’s Relation（伦敦，1622年），第61页。采用博物馆提供的现代拼写版本，节选22词[2][3]。'
SOURCES = '以上两段英文为据史料编写的简述，并非书中原文。书信摘录仅呈现殖民者视角。'
REFERENCES = [
    '[1] U.S. Office of Personnel Management. Federal Holidays: 2026 Holiday Schedule.\nhttps://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/',
    '[2] Edward Winslow. “A Letter Sent from New England.” In Mourt’s Relation. London, 1622, p. 61. 现代拼写转录见 Pilgrim Hall Museum, The “First Thanksgiving”.\nhttps://www.pilgrimhall.org/thanksgiving-national-day-of-mourning/the-first-thanksgiving/',
    '[3] Susan Hardman Moore. The Evolution of Thanksgiving. Yale University Press, November 27, 2014. 书目脚注[i]注明上述书信的版本与页码。\nhttps://yalebooks.yale.edu/2014/11/27/the-evolution-of-thanksgiving/',
    '[4] U.S. National Archives. Congress Establishes Thanksgiving.\nhttps://www.archives.gov/legislative/features/thanksgiving',
    '[5] National Museum of the American Indian, Smithsonian Institution. The “First Thanksgiving”: How Can We Tell a Better Story?\nhttps://americanindian.si.edu/nk360/thanksgiving/',
    '[6] Cambridge University Press. Cambridge Dictionary. 单词释义及美式读音参考。\nhttps://dictionary.cambridge.org/',
]
END = [
    '今天，试着说一句具体的感谢：“谢谢你听我说完”“谢谢你今天帮了我”。你最想把这句话送给谁？',
]

def md_item(item):
    picture = f'<img src="{item["picture"]}" width="64" height="64" alt="{item["meaning"]}"> ' if item['picture'] else ''
    return f"### {picture}{item['text']} /{item['ipa']}/\n\n**{item['meaning']}** {item['tip']}\n\n[▶ {item['text']} 发音]({item['file']})\n\n---\n"

parts = ['# ' + TITLE, '![感恩节英语主题封面](assets/cover.png)', *INTRO, '## 日期怎么算？', DATE,
         '## Where did Thanksgiving come from?', *HISTORY, '**中文参考** ' + HISTORY_TRANSLATION,
         '### 从亲历者的书信读起', '> ' + QUOTE + ' …', QUOTE_TRANSLATION,
         QUOTE_SOURCE, SOURCES,
         '## 节日与餐桌', *[md_item(i) for i in ITEMS[:6]],
         '## 把感谢说出来', *[md_item(i) for i in ITEMS[6:10]],
         '## 学会两句祝福与感谢', *[md_item(i) for i in ITEMS[10:]], *END,
         '词汇释义及读音参考剑桥词典[6]。 美式音标；音频为合成语音；封面与词汇插画为AI生成。',
         '## 参考文献', *REFERENCES]
(ROOT / 'index.md').write_text('\n\n'.join(parts) + '\n', encoding='utf-8')

if '--prepare' in sys.argv:
    print('Prepared article and manifest (12 clips).')
    raise SystemExit

audio_data = {}
for item in ITEMS:
    path = ROOT / item['file']
    with wave.open(str(path), 'rb') as wav:
        assert wav.getnframes() > wav.getframerate() * .25, path
        raw = wav.readframes(wav.getnframes())
        assert wav.getsampwidth() == 2
        values = struct.unpack('<' + 'h' * (len(raw)//2), raw)
        assert max(map(abs, values)) > 500, f'Silent audio: {path}'
    audio_data[item['id']] = 'data:audio/wav;base64,' + base64.b64encode(path.read_bytes()).decode()

# An additional single audio file keeps all vocabulary available in one upload.
with wave.open(str(ROOT / 'audio/00-vocabulary-all.wav'), 'wb') as out:
    for n, item in enumerate(ITEMS[:10]):
        with wave.open(str(ROOT / item['file']), 'rb') as wav:
            if n == 0:
                out.setparams(wav.getparams())
            out.writeframes(wav.readframes(wav.getnframes()))
            out.writeframes(bytes(wav.getframerate() * wav.getnchannels() * wav.getsampwidth()))

esc = html.escape
def p(text):
    return '<p>' + esc(text) + '</p>'

def picture(item, embedded=False):
    if not item['picture']:
        return ''
    src = item['picture']
    if embedded:
        src = 'data:image/png;base64,' + base64.b64encode((ROOT / src).read_bytes()).decode()
    return f'<img src="{src}" alt="{esc(item["meaning"])}" width="64" height="64" style="width:64px;height:64px;object-fit:contain;vertical-align:middle;margin-right:10px">'

def history_html():
    return ('<h2>Where did Thanksgiving come from?</h2>' + ''.join(map(p, HISTORY))
            + '<p><strong>中文参考</strong> ' + esc(HISTORY_TRANSLATION) + '</p>'
            + '<h3>从亲历者的书信读起</h3><blockquote style="margin:18px 0;padding:12px 18px;border-left:3px solid #bc7e50;background:#faf4e9">'
            + esc(QUOTE) + ' …</blockquote>' + p(QUOTE_TRANSLATION)
            + '<p style="font-size:13px;color:#766859">' + esc(QUOTE_SOURCE) + '</p>'
            + '<p style="font-size:13px;color:#766859">' + esc(SOURCES) + '</p>')

def references_html():
    return '<h2>参考文献</h2>' + ''.join('<p style="font-size:13px;line-height:1.8;overflow-wrap:anywhere">' + esc(ref).replace('\n', '<br>') + '</p>' for ref in REFERENCES)

WORD_DIVIDER = '<hr style="border:0;border-top:1px solid #d9c7ad;height:0;margin:26px 0">'

def card(item):
    return f'''<section class="word" id="{item['id']}"><div class="wordhead"><div><h3 lang="en">{picture(item, embedded=True)}{esc(item['text'])}</h3><div class="ipa">/{esc(item['ipa'])}/</div></div><button type="button" data-id="{item['id']}" aria-label="播放 {esc(item['text'])} 的发音">▶ 听发音</button></div><p class="meaning">{esc(item['meaning'])}</p>{p(item['tip'])}</section>''' + WORD_DIVIDER

body = '<header><div class="eyebrow">亲子英语 · 感恩节</div><h1>' + esc(TITLE) + '</h1><div class="dek">10个单词 · 美式音标 · 点击听发音</div></header>'
cover_path = ROOT / 'assets/cover.png'
cover_src = 'data:image/png;base64,' + base64.b64encode(cover_path.read_bytes()).decode() if cover_path.exists() else 'assets/cover.png'
body += '<img class="cover" src="' + cover_src + '" alt="感恩节英语主题封面">' + ''.join(map(p, INTRO))
body += '<div class="toolbar"><button id="play-all" type="button">▶ 连读10个单词</button><button id="stop" type="button" class="secondary">停止</button><label>速度 <select id="rate"><option value="1">正常</option><option value="0.8">慢速</option></select></label></div><p id="status" role="status" aria-live="polite">点击单词旁的按钮，听一听，再跟读。</p>'
body += '<h2>日期怎么算？</h2>' + p(DATE)
body += history_html()
for heading, subset in [('节日与餐桌', ITEMS[:6]), ('把感谢说出来', ITEMS[6:10]), ('学会两句祝福与感谢', ITEMS[10:])]:
    body += '<h2>' + heading + '</h2>' + ''.join(map(card, subset))
body += '<h2>说一句具体的感谢</h2>' + ''.join(map(p, END))
body += '<footer>词汇释义及读音参考剑桥词典[6]。 音频为美式合成语音；封面与词汇插画为AI生成。<br>音频与图片已内嵌，可离线使用。公众号发布请参照随附说明。</footer>' + references_html()

script = '''
const clips = CLIPS;
const items = ITEMS;
const player = new Audio();
const status = document.getElementById('status');
let queue = [];
function clearActive() { document.querySelectorAll('.playing').forEach(el => el.classList.remove('playing')); }
function stop() { queue = []; player.pause(); player.currentTime = 0; clearActive(); status.textContent = '已停止。'; }
function playNext() {
  if (!queue.length) { clearActive(); status.textContent = '播放完毕，再跟读一遍吧。'; return; }
  const id = queue.shift(); const item = items.find(i => i.id === id);
  clearActive(); document.getElementById(id).classList.add('playing');
  player.src = clips[id]; player.playbackRate = Number(document.getElementById('rate').value);
  status.textContent = '正在播放：' + item.text;
  player.play().catch(() => { queue = []; clearActive(); status.textContent = '播放未成功，请再次点击发音按钮，或检查浏览器的音频设置。'; });
}
document.querySelectorAll('[data-id]').forEach(button => button.addEventListener('click', () => { stop(); queue = [button.dataset.id]; playNext(); }));
document.getElementById('play-all').addEventListener('click', () => { stop(); queue = items.slice(0, 10).map(i => i.id); playNext(); });
document.getElementById('stop').addEventListener('click', stop);
document.getElementById('rate').addEventListener('change', event => { player.playbackRate = Number(event.target.value); });
player.addEventListener('ended', playNext);
player.addEventListener('error', () => { queue = []; clearActive(); status.textContent = '音频读取失败，请重新打开完整的HTML文件。'; });
'''.replace('CLIPS', json.dumps(audio_data)).replace('ITEMS', json.dumps(ITEMS, ensure_ascii=False))
css = '''.cover{width:100%;height:auto;border-radius:12px;margin:0 0 18px}*{box-sizing:border-box}body{margin:0;background:#faf6ee;color:#332d27;font:17px/1.95 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif}main{max-width:740px;margin:auto;background:#fffdf8;padding:46px 42px 70px}header{padding-bottom:26px;border-bottom:2px solid #c16c39;margin-bottom:30px}h1{font-size:32px;line-height:1.55;margin:16px 0}h2{font-size:23px;line-height:1.6;margin:44px 0 22px;color:#94491f}h3{margin:0;font-size:25px;line-height:1.45;overflow-wrap:anywhere}.eyebrow{color:#99552e;letter-spacing:3px;font-size:14px}.dek,.source,footer{color:#766859;font-size:14px}.word{padding:23px;margin:20px 0;border:1px solid #eadfcb;border-radius:15px;background:#fff}.wordhead{display:flex;justify-content:space-between;align-items:center;gap:14px}.wordhead>div{min-width:0}.ipa{font-family:"Segoe UI","Arial",sans-serif;color:#766859;overflow-wrap:anywhere}.meaning{font-weight:650;margin:14px 0 8px}.word p:last-child{margin:8px 0 0}.playing{border-color:#a65022;box-shadow:0 0 0 2px #e6cbb5}button{border:0;border-radius:24px;background:#98502b;color:white;padding:11px 17px;cursor:pointer;font:inherit;font-size:14px;white-space:nowrap}button:hover{background:#713919}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #3375b9;outline-offset:4px}.secondary{background:#ece3d5;color:#573e2a}.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#f5ecdd;padding:16px;border-radius:12px}.toolbar label{font-size:14px}select{font:inherit;padding:5px;border:1px solid #c9b99f;border-radius:6px}#status{font-size:14px;color:#80522e;min-height:28px}a{color:#965026}footer{margin-top:40px;padding-top:22px;border-top:1px solid #e3d6c4}@media(max-width:520px){main{padding:28px 20px 45px}h1{font-size:26px}h2{font-size:21px}.word{padding:18px 15px}h3{font-size:22px}.wordhead{align-items:flex-start;flex-wrap:wrap}.wordhead button{margin-top:3px}}'''
page = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + esc(TITLE) + '</title><style>' + css + '</style></head><body><main>' + body + '</main><script>' + script + '</script></body></html>'
(ROOT / 'read-and-listen.html').write_text(page, encoding='utf-8')
(ROOT / 'player-check.js').write_text(script, encoding='utf-8')

# Keep the official-account copy free of scripts and misleading play buttons.
publish = f'<h1 style="font-size:25px;line-height:1.6">{esc(TITLE)}</h1>'
publish += ''.join(map(p, INTRO)) + '<h2>日期怎么算？</h2>' + p(DATE)
publish += history_html()
for heading, subset in [('节日与餐桌', ITEMS[:6]), ('把感谢说出来', ITEMS[6:10]), ('学会两句祝福与感谢', ITEMS[10:])]:
    publish += '<h2>' + heading + '</h2>'
    if subset == ITEMS[10:]:
        publish += p('整句音标是便于跟读的参考读法，实际语流中会有弱读和连读。')
    for item in subset:
        publish += f'<h3>{picture(item)}{esc(item["text"])}</h3><p style="color:#766859">/{esc(item["ipa"])}/</p><p><strong>{esc(item["meaning"])}</strong></p>'
        publish += p(item['tip']) + f'<p style="font-size:14px;color:#80522e;margin:12px 0 4px">发音：{esc(item["text"])}</p>' + f'<p style="color:#99663d;font-size:13px">【在此插入音频：{esc(Path(item["file"]).name)}】</p>' + WORD_DIVIDER
publish += '<h2>说一句具体的感谢</h2>' + ''.join(map(p, END))
publish += '<p style="font-size:13px;color:#766859">词汇释义及读音参考剑桥词典[6]。 美式英语音频由 Microsoft Zira 合成；封面与词汇插画为AI生成。</p>' + references_html()
(ROOT / 'wechat-copy.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>公众号排版稿</title><body><article style="max-width:680px;margin:24px auto;padding:20px;font-family:Arial,Microsoft YaHei,sans-serif;font-size:16px;line-height:1.95;color:#332d27">' + publish + '</article></body></html>', encoding='utf-8')

with zipfile.ZipFile(ROOT / 'thanksgiving-publish-kit.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in ['index.md', 'wechat-copy.html', 'read-and-listen.html', 'publishing-guide.md', 'audio-manifest.json']:
        if (ROOT / name).exists():
            archive.write(ROOT / name, name)
    for path in [ROOT / item['file'] for item in ITEMS] + [ROOT / 'audio/00-vocabulary-all.wav']:
        archive.write(path, path.relative_to(ROOT))
    selected_assets = [ROOT / item['picture'] for item in ITEMS if item['picture']]
    selected_assets += [ROOT / name for name in ['assets/cover.png', 'assets/cover.prompt.txt', 'assets/vocabulary/prompts.json']]
    for path in selected_assets:
        archive.write(path, path.relative_to(ROOT))
print(f'Built article, 12 verified audio clips, combined vocabulary track, and offline HTML ({len(page):,} chars).')
