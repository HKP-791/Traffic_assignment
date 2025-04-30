# 基于Frank-Wolfe算法的用户均衡模型交通分配实现

## 1.项目介绍

本项目基于Frank-wolfe算法,可以将交通分布阶段得出的交通OD分布矩阵按照已知的路网描述,分配到连接各交通节点的具体道路上。其具体实现思路如下:
- 步骤1:初始化。基于零流图的路阻,由dijkstra算法依次搜索每一个OD对r,s所对应的最短路径,并将r,s间的OD流量,全部分配到对应的最短路径上,得到初始路段流量,并令迭代次数n=1。
- 步骤2:更新路阻。根据下图中的阻抗函数,分别代入每个路段的初始流量,求得阻抗
- 步骤3:下降方向。基于阻抗,按照步骤1中的最短路全有全无分配法,将流量重新分配到对应路径上,得到临时路段流量,进而得到更新流量的方向和大小。
- 步骤4:搜索最优步长,并更新流量。采用二分法,得到全局阻抗函数最小时对应的更新步长。依照步长和更新流量的方向和大小,更新各道路的流量。
- 步骤5:结束条件。如果更新步长小于算法阈值tol,则算法结束；否则继续更新迭代,直至满足最大迭代数。
下图是在给定数据上计算出的交通分配结果。
<img src="result/Figure_1.png">

## 2.使用方法

- 输入下面命令完成环境配置
```bash
conda create -n traffic_assignment python=3.8
pip install -r requirements.txt
```
将准备好的交通现状OD分布矩阵、交通现状时间代价矩阵、交通未来OD总量、交通未来时间代价矩阵数据填入.csv格式文件中,表格不需要输入行列的标题。数据文件放置于data目录下。
- 输入下面的命令开始迭代计算
```bash
python main.py --edges <your edges data path> --od <your OD data path> --pos <your data that describe the position of network node> --max_iter <maximum iteration> --tol <tolerance of update step>
```

### 3.作者
- Ica_l
- 邮箱地址 : [desprado233@163.com](desprado233@163.com)
- Github : [HKP-791](https://github.com/HKP-791)