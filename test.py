import environ
from pathlib import Path

from bFdcAPI.MP.UseCase import FdcMpUseCase

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env('.env.local')

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


if __name__ == '__main__':
    import xml.etree.ElementTree as elemTree
    xml = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<message command="EAPFDC_TOOLDATA" from="ML006" to="FDC" timestamp="2023-06-22 13:09:28" EQUIPMENT_ID="ML006" xmlns="http://http://www.wisol.co.kr/schema/eap">
  <params>
    <para name="LOT">NBHF80840^05^B^SX897EYTRF09^R9TCCSP_Passi_2_V1^OP0D001010</para>
    <para name="LOT">NBHF80870^05^B^SX897EYTRF09^R9TCCSP_Passi_2_V1^OP0D001010</para>
    <para name="LOT">NAHFE0580^05^A^SX897EYTRF08^R9TCCSP_Passi_2_V1^OP0D001010</para>
    <para name="LOT">NAHFD0B60^05^A^SX897EYTRF08^R9TCCSP_Passi_2_V1^OP06002030</para>
    <para name="TRID">107</para>
    <para name="VID">32^64^65^66^67^68^69^70^71^72^73^74^75^76^77^78^79^80^81^82^83</para>
    <para name="DATA">1,32,230,0,0,L1:{L2:NBHF80870,6}^2,64,231,0,0,L2:{L2:NBHF80840,20},{L2:NBHF80870,1}^0,65,48,1,0,L0:^1,66,32,15,9,L1:{L2:NBHF80840,21}^0,67,32,16,1,L0:^1,68,64,3,3,L1:{L2:NBHF80870,5}^0,69,97,9,0,L0:^0,70,97,9,0,L0:^1,71,81,4,0,L1:{L2:NBHF80870,2}^1,72,64,3,0,L1:{L2:NBHF80870,4}^0,73,97,38,0,L0:^0,74,97,9,0,L0:^1,75,81,4,1,L1:{L2:NBHF80870,3}^0,76,96,41,0,L0:^0,77,97,38,0,L0:^1,78,97,11,0,L1:{L2:NBHF80840,18}^0,79,81,0,0,L0:^0,80,96,41,0,L0:^1,81,97,11,1,L1:{L2:NBHF80840,19}^1,82,97,11,1,L1:{L2:NBHF80840,17}^0,83,81,40,0,L0:</para>
  </params>
</message>'''
    tree = elemTree.fromstring(xml)
    lots = tree[0].findall("./{http://http://www.wisol.co.kr/schema/eap}para[@name='LOT']")
    # ids = tree[0].find("./{http://http://www.wisol.co.kr/schema/eap}para[@name='VID']").text.split("^")
    data = {}
    data.keys()
    float("10")

