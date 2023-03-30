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
<message command="EAPFDC_TOOLDATA" from="ML083" to="FDC" timestamp="2023-03-30 14:07:44" EQUIPMENT_ID="ML083" xmlns="http://http://www.wisol.co.kr/schema/eap">
  <params>
    <para name="LOT">NBHC80240^X_55 RANK^B^SX897CHK0F01^R9TCCSP^OP06001010</para>
    <para name="LOT">NAHCN0750^X_15 RANK^A^SRG00AXU0F01^R7WLP_NO_T LIFT^OP06001010</para>
    <para name="TRID">1</para>
    <para name="VID">TEST1^TEST2^TEST3^TEST4^TEST5^TEST6</para>
    <para name="DATA">abcd^1^2^3^4^5</para>
  </params>
</message>'''
    tree = elemTree.fromstring(xml)
    datas = tree[0].find("./{http://http://www.wisol.co.kr/schema/eap}para[@name='DATA']").text.split("^")
    ids = tree[0].find("./{http://http://www.wisol.co.kr/schema/eap}para[@name='VID']").text.split("^")
    data = {}
    data.keys()
    float("10")
    for index, key in enumerate(tree[0].find("./{http://http://www.wisol.co.kr/schema/eap}para[@name='VID']").text.split("^")):
        data.setdefault(key,datas[index])
    case = FdcMpUseCase()
    cases = case.getMLB(1)
    print(cases)
