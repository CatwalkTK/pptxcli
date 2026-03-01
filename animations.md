# アニメーション詳細ガイド

PptxGenJSにはアニメーションAPIがないため、PPTX生成後にXML直接操作でアニメーションを追加する。

## 技術的アプローチ

### 方法: PPTX → Unpack → XML編集 → Repack

```bash
# 1. PptxGenJSで静的なPPTXを生成
node generate.js

# 2. アンパック
python /mnt/skills/public/pptx/scripts/office/unpack.py output.pptx unpacked/

# 3. Pythonスクリプトでアニメーション追加
python add_animations.py unpacked/

# 4. クリーン & リパック
python /mnt/skills/public/pptx/scripts/clean.py unpacked/
python /mnt/skills/public/pptx/scripts/office/pack.py unpacked/ final_output.pptx --original output.pptx
```

## スライド間トランジション

### Fade（推奨・最もビジネスに適切）

各 `slideN.xml` の `<p:sld>` 直下に追加：

```xml
<p:transition spd="med" advClick="1">
  <p:fade />
</p:transition>
```

### Push（方向付きトランジション）

```xml
<p:transition spd="med" advClick="1">
  <p:push dir="l"/>
</p:transition>
```
- dir: "l"(左), "r"(右), "u"(上), "d"(下)

### Wipe

```xml
<p:transition spd="med" advClick="1">
  <p:wipe dir="d"/>
</p:transition>
```

### 速度設定
- `spd="slow"` — 1秒（重要なスライドの区切りに）
- `spd="med"` — 0.75秒（通常使用）
- `spd="fast"` — 0.5秒（テンポよく進める時）

### ビジネスでのトランジション選択ルール
- **全スライド統一**: 異なるトランジションを混在させない
- **Fadeが最も安全**: どんなビジネスシーンにも合う
- **セクション区切りだけ変える**: タイトル→コンテンツ移行時のみ別トランジションもOK

---

## 要素アニメーション（Entrance Effects）

要素アニメーションは `slideN.xml` 内の `<p:timing>` セクションで制御する。

### 基本構造

```xml
<p:timing>
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
        <p:childTnLst>
          <!-- クリックでトリガー -->
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                <!-- アニメーションステップをここに追加 -->
              </p:childTnLst>
            </p:cTn>
            <p:prevCondLst>
              <p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>
            </p:prevCondLst>
            <p:nextCondLst>
              <p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>
            </p:nextCondLst>
          </p:seq>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>
```

### Fade In（推奨）

各要素のアニメーションステップ：

```xml
<p:par>
  <p:cTn id="3" fill="hold">
    <p:stCondLst>
      <p:cond delay="0"/>
    </p:stCondLst>
    <p:childTnLst>
      <p:par>
        <p:cTn id="4" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="clickEffect">
          <p:stCondLst>
            <p:cond delay="0"/>
          </p:stCondLst>
          <p:childTnLst>
            <p:set>
              <p:cBhvr>
                <p:cTn id="5" dur="1" fill="hold">
                  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                </p:cTn>
                <p:tgtEl>
                  <p:spTgt spid="TARGET_SHAPE_ID"/>
                </p:tgtEl>
                <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
              </p:cBhvr>
              <p:to><p:strVal val="visible"/></p:to>
            </p:set>
            <p:animEffect transition="in" filter="fade">
              <p:cBhvr>
                <p:cTn id="6" dur="500"/>
                <p:tgtEl>
                  <p:spTgt spid="TARGET_SHAPE_ID"/>
                </p:tgtEl>
              </p:cBhvr>
            </p:animEffect>
          </p:childTnLst>
        </p:cTn>
      </p:par>
    </p:childTnLst>
  </p:cTn>
</p:par>
```

- `presetID="10"` = Fade
- `dur="500"` = 0.5秒（ミリ秒単位）
- `TARGET_SHAPE_ID` をスライド内の要素IDに置換する

### Appear（最もシンプル）

```xml
<p:par>
  <p:cTn id="3" fill="hold">
    <p:stCondLst><p:cond delay="0"/></p:stCondLst>
    <p:childTnLst>
      <p:par>
        <p:cTn id="4" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" nodeType="clickEffect">
          <p:stCondLst><p:cond delay="0"/></p:stCondLst>
          <p:childTnLst>
            <p:set>
              <p:cBhvr>
                <p:cTn id="5" dur="1" fill="hold">
                  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                </p:cTn>
                <p:tgtEl><p:spTgt spid="TARGET_SHAPE_ID"/></p:tgtEl>
                <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
              </p:cBhvr>
              <p:to><p:strVal val="visible"/></p:to>
            </p:set>
          </p:childTnLst>
        </p:cTn>
      </p:par>
    </p:childTnLst>
  </p:cTn>
</p:par>
```

- `presetID="1"` = Appear

### Wipe（方向付きの登場）

```xml
<p:animEffect transition="in" filter="wipe(down)">
  <p:cBhvr>
    <p:cTn id="6" dur="750"/>
    <p:tgtEl><p:spTgt spid="TARGET_SHAPE_ID"/></p:tgtEl>
  </p:cBhvr>
</p:animEffect>
```

- `filter="wipe(down)"` — 上から下へ
- `filter="wipe(right)"` — 左から右へ
- `presetID="22"` を使用

---

## よく使うPreset ID一覧

| presetID | 効果名 | ビジネス適正 |
|----------|--------|------------|
| 1 | Appear | ◎ 最も控えめ |
| 10 | Fade | ◎ 最もビジネス向き |
| 22 | Wipe | ○ チャートの段階表示に |
| 2 | Fly In | △ 控えめに使えばOK |
| 53 | Grow & Turn | ✗ ビジネスNG |
| 26 | Bounce | ✗ ビジネスNG |

---

## Progressive Reveal パターン

ビジネスで最も効果的な「段階的表示」の実装。

### 使い方
1. まずタイトルとキーメッセージを表示（スライド表示時に自動）
2. クリックで根拠データ/チャートを表示
3. クリックで結論/次のアクションを表示

### 実装のコツ

Shape IDの取得方法：
```python
import xml.etree.ElementTree as ET

tree = ET.parse('unpacked/ppt/slides/slide1.xml')
ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

# スライド内の全シェイプのIDを取得
for sp in tree.findall('.//p:cSld/p:spTree/p:sp', ns):
    nvSpPr = sp.find('.//p:nvSpPr/p:cNvPr', {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
    if nvSpPr is None:
        # PptxGenJS生成の場合、名前空間が異なることがある
        for elem in sp.iter():
            if elem.tag.endswith('cNvPr'):
                print(f"ID: {elem.get('id')}, Name: {elem.get('name')}")
                break
```

### 自動アニメーション追加スクリプトテンプレート

```python
#!/usr/bin/env python3
"""
スライドにFadeアニメーションとトランジションを追加する
"""
import xml.etree.ElementTree as ET
import os
import glob
import re

# 名前空間の登録
namespaces = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

for prefix, uri in namespaces.items():
    ET.register_namespace(prefix, uri)


def add_fade_transition(slide_path, speed="med"):
    """スライドにFadeトランジションを追加"""
    tree = ET.parse(slide_path)
    root = tree.getroot()
    
    # 既存のtransitionを削除
    for trans in root.findall('{http://schemas.openxmlformats.org/presentationml/2006/main}transition'):
        root.remove(trans)
    
    # Fadeトランジションを追加
    transition = ET.SubElement(root, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    transition.set('spd', speed)
    transition.set('advClick', '1')
    fade = ET.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}fade')
    
    tree.write(slide_path, xml_declaration=True, encoding='UTF-8')


def add_transitions_to_all(unpacked_dir, speed="med"):
    """全スライドにトランジションを追加"""
    slides_dir = os.path.join(unpacked_dir, 'ppt', 'slides')
    for slide_file in sorted(glob.glob(os.path.join(slides_dir, 'slide*.xml'))):
        add_fade_transition(slide_file, speed)
        print(f"Added fade transition to {os.path.basename(slide_file)}")


if __name__ == '__main__':
    import sys
    unpacked_dir = sys.argv[1] if len(sys.argv) > 1 else 'unpacked'
    add_transitions_to_all(unpacked_dir)
```

---

## 注意事項

- アニメーションXMLは複雑なため、まずトランジションだけ追加し、要素アニメーションは必要に応じて追加する
- IDは連番で管理し、重複させない
- アニメーション追加後は必ずPowerPointで開いて動作確認する
- LibreOfficeではアニメーションの一部が正しく再生されない場合がある
