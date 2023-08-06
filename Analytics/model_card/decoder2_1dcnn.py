#!/usr/bin/env python
# coding: utf-8
# %%
import model_card_toolkit as mct
import base64
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import utils
#学習履歴の取得
history = pd.read_csv("c:/lab/models/dec2/history.csv")
history
# %%
epochs = len(history["binary_accuracy"])
history_base64_list = []
for item in ["binary_accuracy","loss","recall_5","specificity"]:
    plt.plot(range(1,epochs+1),history[item],label="train_"+item)
    plt.plot(range(1,epochs+1),history["val_"+item],label="valid_"+item)
    plt.legend(loc="upper left",bbox_to_anchor=(1,1))
    img_in_memory = BytesIO()
    plt.savefig(img_in_memory,format='png', bbox_inches='tight')
    img_in_memory.seek(0)
    plt.show()
    history_base64_list.append(base64.b64encode(img_in_memory.getvalue()))
# %%
#　概要
#
toolkit,model_card = utils.build_base_card('Decoder 1号',"001")
details = model_card.model_details
details.version.diff="初期バージョン"
details.overview = (
    "1DCNNを使用し、マルチチャネルEEGデータ(左手・右手の運動イメージ)を2値分類します。\n"
    "学習データにはOpenBMIによって測定された54人の公開データを使用します。")
details.documentation = ("前処理としてEEGLABを通し、アーチファクトの影響の多いデータの除去、ダウンサンプリング(1000hz->500hz)、バンドパスフィルターの適用(1hzから30hz)を行っています。\n"
                         "EEGLABを通した後、標準化とバンドパスフィルタ(8hzから30hz)を適用しています。\n"
                         "['FC5','FC1','FC2','FC6','C3','C1','Cz','C2','C4','CP5','CP1','CP2','CP6']電極(fs=500hz)を使用。[54, 34, 21, 35, 1]番の被験者を検証データ、それ以外を学習データにしました。")
#
#技術的パラメータ
#
#データセットについて
parameters = model_card.model_parameters
parameters.model_architecture="1DCNN"
parameters.input_format= "生波形を入力しています。形式は2階テンソル(バッチサイズを含むと3階)です。750サンプルはランダム区間で選択"
parameters.input_format_map = [mct.KeyVal("1","750 samples"),
                               mct.KeyVal("2","16ch")]
parameters.output_format="シグモイドによる2値(左:0,右:1)出力"

#
#評価
#
model_card.quantitative_analysis.graphics.description = "正解率(Accuracy),損失(Loss),再現率(Recall),特異度(Specificity)。23エポックのモデルを選択。"
model_card.quantitative_analysis.graphics.collection =[mct.Graphic("",h64) for h64 in history_base64_list]

# %%
utils.save_and_display("../../docs/model_cards/decoder2.html",toolkit,model_card)

