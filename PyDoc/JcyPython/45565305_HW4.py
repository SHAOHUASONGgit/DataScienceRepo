import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode
location = [
    ("黑龙江", [127.9688, 45.368]),
    ("内蒙古", [110.3467, 41.4899]),
    ("吉林", [125.8154, 44.2584]),
    ("辽宁", [123.1238, 42.1216]),
    ("河北", [114.4995, 38.1006]),
    ("天津", [117.4219, 39.4189]),
    ("山西", [112.3352, 37.9413]),
    ("陕西", [109.1162, 34.2004]),
    ("甘肃", [103.5901, 36.3043]),
    ("宁夏", [106.3586, 38.1775]),
    ("青海", [101.4038, 36.8207]),
    ("新疆", [87.9236, 43.5883]),
    ("西藏", [91.11, 29.97]),
    ("四川", [103.9526, 30.7617]),
    ("重庆", [108.384366, 30.439702]),
    ("山东", [117.1582, 36.8701]),
    ("河南", [113.4668, 34.6234]),
    ("江苏", [118.8062, 31.9208]),
    ("安徽", [117.29, 32.0581]),
    ("湖北", [114.3896, 30.6628]),
    ("浙江", [119.5313, 29.8773]),
    ("福建", [119.4543, 25.9222]),
    ("江西", [116.0046, 28.6633]),
    ("湖南", [113.0823, 28.2568]),
    ("贵州", [106.6992, 26.7682]),
    ("广西", [108.479, 23.1152]),
    ("海南", [110.3893, 19.8516]),
    ("上海", [121.4648, 31.2891]),
    ("广东", [113.25, 23.01]),
    ("云南", [102, 24]),
    ("北京", [116.3333, 40])
]
location = dict(location)
input = pd.read_csv("dataset.csv", encoding="utf-8").values[1:]
dataForVisual = []
for data in input:
    province = data[0]
    dataWithLocation = location.get(province)
    dataWithLocation.append(float(data[1].split("万")[0]))
    dataWithLocation.append(float(data[2].split("万")[0]))
    dataWithLocation.append(int(data[3]))
    dataWithLocation.append(int(data[4]))
    dataForVisual.append((province, dataWithLocation))



opt = opts.InitOpts(width="1400px", height="700px")
ItemStyleOpt = opts.ItemStyleOpts(color="rgb(5,101,123)", opacity=1, border_width=0.8, border_color="rgb(62,215,213)")
Map3DLabelOpt = opts.Map3DLabelOpts(is_show=False)
LabelOpt=opts.LabelOpts(is_show=False, color="#fff", font_size=10, background_color="rgba(0,23,11,0)")
Map3DLightOpt=opts.Map3DLightOpts(main_color="#fff", main_intensity=1.2, main_shadow_quality="high", is_main_shadow=False, main_beta=10, ambient_intensity=0.3)
map = Map3D(init_opts=opt).set_global_opts(title_opts=opts.TitleOpts(title="升学数据"))
map.add_schema(
    maptype='china',
    itemstyle_opts=ItemStyleOpt,
    map3d_label=Map3DLabelOpt,
    emphasis_label_opts=LabelOpt,
    light_opts=Map3DLightOpt
)
map.add(
    is_selected=False,
    series_name="(点击显示)17年高考人数",
    data_pair=dataForVisual,
    type_=ChartType.BAR3D,
    bar_size=1,
    label_opts=opts.LabelOpts(is_show=True, formatter=JsCode("function(data){return data.name + ' ' + data.value[2] + '万';}"))
)
map.add(
    is_selected=False,
    series_name="(点击显示)16年高考人数",
    data_pair=dataForVisual,
    type_=ChartType.BAR3D,
    bar_size=1,
    label_opts=opts.LabelOpts(is_show=True, formatter=JsCode("function(data){return data.name + ' ' + data.value[3] + '万';}"))
)
map.add(
    is_selected=False,
    series_name="(点击显示)92高校数量",
    data_pair=dataForVisual,
    type_=ChartType.BAR3D,
    bar_size=1,
    label_opts=opts.LabelOpts(is_show=True, formatter=JsCode("function(data){return data.name + ' ' + data.value[4] + '所';}"))
)
map.add(
    is_selected=False,
    series_name="(点击显示)公办高校数量",
    data_pair=dataForVisual,
    type_=ChartType.BAR3D,
    bar_size=1,
    label_opts=opts.LabelOpts(is_show=True, formatter=JsCode("function(data){return data.name + ' ' + data.value[5] + '所';}"))
)
map.render("作业四.html")