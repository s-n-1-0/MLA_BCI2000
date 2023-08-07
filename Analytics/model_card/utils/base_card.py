#
# TODO: 今後データセット等を追加する場合、コードを分割すること
#
import model_card_toolkit as mct
import datetime
import requests
import base64
from IPython.display import HTML
# 画像データの取得
response = requests.get("https://i.gyazo.com/dc04eaf10fa1e527b567261dd516d0e9.png")
file_data = response.content
openbmi_mitask_image = base64.b64encode(file_data).decode('utf-8')

def build_base_card(model_name:str,
                    version:str):
    toolkit = mct.ModelCardToolkit()
    model_card = toolkit.scaffold_assets()
    details = model_card.model_details
    details.name = model_name
    details.owners = [
    mct.Owner(name = 'BCI研究グループ', contact= '静岡理工科大学大学院')
    ]
    details.references = [mct.Reference(
        'https://academic.oup.com/gigascience/article/8/5/giz002/5304369'
    )]
    v = details.version
    v.name = version
    v.date = str(datetime.datetime.now())
    model_card.model_parameters.data = [mct.Dataset(name="OpenBMIデータセット(3パラダイム)",
                    description="ERP・MI・SSVEPのタスクを行った54名の被験者データ(MIデータのみ使用)",
                    graphics=mct.GraphicsCollection(("MIタスク図"),[mct.Graphic("",openbmi_mitask_image)]))]
    
    return toolkit,model_card


def save_and_display(ex_path:str,toolkit,card):
    toolkit.update_model_card(card)
    html = toolkit.export_format()
    with open(ex_path, "w") as f:
        f.write(html)
    return HTML(html)