#!/usr/bin/env python
# coding: utf-8
# %%
import model_card_toolkit as mct
import base64
import requests
import datetime
response = requests.get("https://i.gyazo.com/dc04eaf10fa1e527b567261dd516d0e9.png")
file_data = response.content
openbmi_mitask_image = base64.b64encode(file_data).decode('utf-8')


# %%
toolkit = mct.ModelCardToolkit()
model_card = toolkit.scaffold_assets()
#
#　概要
#
details = model_card.model_details
details.version = mct.Version("001",str(datetime.datetime.now()),diff="初期バージョン")
details.name = 'Decoder 1号'
details.overview = (
    "このモデルは、左手・右手の運動イメージをマルチチャネルEEGデータを入力として判別します。\n"
    "学習データにはOpenBMIによって測定された54人の公開データを使用します。")
details.documentation = ("前処理としてEEGLABを通し、アーチファクトの影響の多いデータの除去、ダウンサンプリング(1000hz->500hz)、バンドパスフィルターの適用(1hzから30hz)を行っています。\n"
                         "EEGLABを通した後、標準化とバンドパスフィルタ(8hzから30hz)を適用しています。")
details.owners = [
    mct.Owner(name = 'BCI研究グループ', contact= '静岡理工科大学大学院')
]
details.references = [mct.Reference(
    'https://iopscience.iop.org/article/10.1088/1741-2552/aace8c/meta'
),mct.Reference(
    'https://academic.oup.com/gigascience/article/8/5/giz002/5304369'
)]
#
#技術的パラメータ
#
#データセットについて
dataset = mct.Dataset(name="OpenBMIデータセット(3パラダイム)",
                     description="ERP・MI・SSVEPのタスクを行った54名の被験者データ(MIデータのみ使用)",
                     graphics=mct.GraphicsCollection(("MIタスク図"),[mct.Graphic("",openbmi_mitask_image)]))
model_card.model_parameters = mct.ModelParameters(
    model_architecture="EEGNet",
    data=[dataset],
    input_format= "(16ch,750sample,1)※fs:500hz",
    output_format="2値(左:0,右:1)、シグモイド出力"
)
#
#評価
#
model_card.quantitative_analysis.graphics.description = ('正解率(Acc),再現率(Recall),特異度(Specificity),')
#model_card.quantitative_analysis.graphics.collection =[mct.Graphic("",openbmi_mitask_image)]

toolkit.update_model_card(model_card)

# Return the model card document as an HTML page
html = toolkit.export_format()


# %%


from IPython.display import HTML
with open("./test.html", "w") as f:
    f.write(html)
HTML(html)





