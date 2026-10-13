# 方解石 C–O 同位素图件与数据核对

本次已完成 4 张基于上传数据的描述性图件。**尚未完成上传 skills 的读取，以及不少于 10 个顶刊绘图实例的独立核查**：ZIP 超过 32 MiB 工具传输上限；文献网站被当前网络代理拒绝（403）。这些图件不标称为已依据 10 个顶刊核查后的最终论文图。

## 数据与坐标

- 样品：`222.csv`，28 个方解石样品，全部保留；没有剔除离群点，也没有添加模拟样品。
- 参考端元：`111.csv`，14 类用户收集的参考资料。所列数值及引文为用户提供，本次未独立核验原文。
- C–O 散点图：横坐标为方解石 δ¹⁸O（‰ VSMOW），纵坐标为方解石 δ¹³C（‰ VPDB）。
- 氧坐标直接使用上传的 `d18O_VSMOW_permil_converted` 列。其数值与 δ¹⁸O(VSMOW) = 1.03092 × δ¹⁸O(VPDB) + 30.92 一致，最大舍入残差小于 0.00005‰。这只是对输入的一致性核对，换算公式来源尚待原文确认。
- 样品 δ¹³C：−7.284 至 +0.952‰；δ¹⁸O(VSMOW)：+10.7016 至 +21.3458‰；δ¹⁸O(VPDB)：−19.612 至 −9.287‰。
- 分析误差、测量温度、流体组成和正式方解石期次未提供，不绘制误差棒、流体分馏轨迹或定量混合曲线。

## 4 张图的用途与图注

### 图 1：产出位置分组及碳酸盐参考范围

`01_CO_occurrence`：按围岩、矿体、矿化带、矿化带边和未注明分组。围岩括号中的不同岩性在本图合为“Host rock”，原始岩性仍保留在数据表。样品数依次为 5、5、8、2、8。

叠加水口山灰岩、康家湾矿石方解石、Cocos Ridge 钙质沉积物和原生火成碳酸盐参考范围。前三者的矩形来自**分别给出的 C、O 边际范围**，矩形内每个坐标并不是已测量的配对样品；原生火成碳酸盐矩形按输入表中的参考场范围绘制。

Suggested caption: Carbon and oxygen isotope compositions of 28 calcites, grouped by recorded occurrence. User-supplied carbonate reference ranges are shown for context. Except for the supplied primary igneous carbonate field, dashed rectangles represent independent marginal ranges and do not represent paired reference measurements. Reference overlap alone does not identify the source of carbon or oxygen.

### 图 2：样品编号系列及重点样品

`02_CO_sample_series`：按 BF5、BF8、BF9、BF10、BF11 和其他编号分组，样品数为 4、6、9、1、6、2；这不是地质期次划分。标注 BF9-8-1、BF9-8-2、BF9-2-2 等低 δ¹³C 样品，并显示水口山灰岩与康家湾方解石的参考范围。

Suggested caption: Calcite C–O compositions grouped by sample ID series, with selected samples labeled. Series are derived from sample identifiers and are not interpreted as chronological mineralization stages. Two carbonate comparison boxes represent separate published C and O ranges supplied by the user.

### 图 3：外观分组及边际分布

`03_CO_appearance_marginals`：分为白色（14）、肉红色（6）、棕褐/深色（4）以及混色/浅黄（4）。棕褐/深色由红褐色、黑褐色、深褐色合并；混色/浅黄由白-红褐色、白黄方解石、白-棕色合并。上下/侧边直方图展示全部 28 个实测值，不使用小样本核密度云图或推断置信椭圆。

Suggested caption: Calcite C–O compositions grouped by observed appearance, with marginal histograms of all 28 observations. Appearance categories are descriptive and do not establish separate calcite generations. Analytical uncertainties were unavailable and are not shown.

### 图 4：全体参考端元的独立 C、O 对比

`04_CO_endmember_comparison`：碳参考全范围、碳参考放大范围和氧参考范围三联图，涵盖输入的全部 14 类参考。碳数据和氧数据分别绘制，没有为单同位素端元补造另一坐标。

蓝点为实测方解石；蓝色竖带为实测范围；绿色为碳酸盐参考；灰色为水、气体、有机物或岩石等不同物质。大气 CO₂ 的 −6.5‰、−8‰是两个时期的代表值，以两个点表示，不连成连续来源范围。上地幔岩石 +5.7±0.3‰按提供的区间展示；其 ± 定义未核验，不能解释为本图样品的分析误差。

Suggested caption: Separate comparisons of calcite carbon and oxygen isotope compositions with user-supplied reference values. Blue dots show individual calcites and blue shading their observed range. Green references are carbonates; gray references are other materials. Atmospheric CO₂ values are time-specific points. Carbon and oxygen entries are independent comparisons, not paired C–O endmembers. Mineral–fluid fractionation and phase differences must be evaluated before assigning sources.

## 可以描述的现象与不能推出的结论

- 三个明显较低的 δ¹³C 值为 BF9-8-1（−7.284‰）、BF9-8-2（−5.828‰）和 BF9-2-2（−3.934‰），其 δ¹⁸O(VSMOW) 为 +19.0057、+21.3458、+18.0490‰。
- 全样品 C、O Pearson 相关系数约 −0.258，为描述性统计；不据此拟合或命名单一成因趋势。
- 不能把海水氧、MORB 气体碳、全岩氧、有机碳与方解石直接作为同一矿物相的二维端元。
- 海水 → 方解石氧同位素需要温度与分馏关系；有机物/甲烷 → 方解石碳同位素需要反应路径及碳预算。没有这些信息，混合比例和来源轨迹不可识别。
- 参考灰岩来自水口山；在样品地点未确认前，不能称为本矿床的实测围岩端元。康家湾矿石方解石为对比资料，也不能当作本矿床的唯一矿化端元。
- 没有重释 Cc、Bg、Py 等缩写，也没有按穿切关系自行划定成矿期次。

## 待完成的文献与 skills 工作

要满足原请求，需要读取精简上传的 skills，并独立查阅不少于 10 个符合研究方向的顶刊绘图实例，记录完整引文、实际图号、矿物/物质相、参考尺度、分组方式、端元来源、是否使用误差或过程模型以及适用限制。目前没有把仅有标题或 DOI 的条目算作“已阅读原图”。

后续检索可优先覆盖 Nature Geoscience、Nature Communications、Science Advances、Geology、Geochimica et Cosmochimica Acta、Earth and Planetary Science Letters、Chemical Geology、Economic Geology、Journal of Petrology、Geochemistry, Geophysics, Geosystems 等相关期刊；这只是检索方向，不是已完成的文献列表，也不预先断言这些期刊的每篇文章都有合适的方解石 C–O 图。

检索所需域名已写入环境网络配置草稿，包括 Crossref、OpenAlex、DOI 和相关出版商网站。草稿保存不等于当前网络已生效；需要在环境设置中保存/启用后，重新测试访问再继续核查。其他论文托管域名若出现具体需求，再按需补充。

## 文件与复现

- 每张图提供 600 dpi PNG、矢量 PDF、可编辑 SVG；英文图内文字方便后续英文稿排版。
- `samples_222.csv` 与 `references_111.csv` 是上传 CSV 的副本；原文件未修改。
- `samples_audited.csv` 保留原始列，并附加分组与氧换算残差。
- `references_plot_values.csv` 明确记录作图使用的每个单同位素参考值/范围，独立核验状态全部为 False。
- `reference_source_audit.csv` 与 `reference_source_audit.md` 逐条列出用户提供的引文及当前核查状态。
- 在本目录执行 `python3 plot_co.py` 可重现 4 张图。依赖为 Python、numpy、pandas、matplotlib；当前环境已具备。
- 图件、数据副本和复现代码现保存于 GitHub 仓库 `tp320621/123` 的 `co_isotope_figures/` 目录。上传的原始 CSV 未修改。
