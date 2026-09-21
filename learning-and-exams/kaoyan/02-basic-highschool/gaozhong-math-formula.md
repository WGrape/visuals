# 高中数学常用公式手册

> 按知识点分类 · 层次清晰 · LaTeX 公式速查

## 一、集合与常用逻辑用语

### 集合运算
- **交集**：$A \cap B = \{ x \mid x \in A\ \text{且}\ x \in B \}$
- **并集**：$A \cup B = \{ x \mid x \in A\ \text{或}\ x \in B \}$
- **补集**：$\complement_U A = \{ x \mid x \in U\ \text{且}\ x \notin A \}$

### 子集元素个数
- **子集数**：含 $n$ 个元素的集合有 $2^n$ 个子集，$2^n-1$ 个真子集

### 充要条件
- **关系**：$A \Rightarrow B:\ A\ \text{充分},\ B\ \text{必要};\quad A \Leftrightarrow B:\ \text{充要}$

## 二、函数

### 二次函数
- **顶点**：$y = ax^2 + bx + c,\ \text{顶点 } \left(-\dfrac{b}{2a},\ -\dfrac{\Delta}{4a}\right)$
- **判别式**：$\Delta = b^2 - 4ac$

### 指数与对数
- **指数运算**：$a^m \cdot a^n = a^{m+n};\quad (a^m)^n = a^{mn};\quad (ab)^n = a^n b^n$
- **对数运算**：$\log_a(MN) = \log_a M + \log_a N;\quad \log_a\dfrac{M}{N} = \log_a M - \log_a N;\quad \log_a M^n = n\log_a M$
- **换底**：$\log_a b = \dfrac{\log_c b}{\log_c a};\quad a^{\log_a N} = N$

### 函数性质
- **奇偶性**：$\text{偶}:\ f(-x)=f(x);\quad \text{奇}:\ f(-x)=-f(x)$
- **周期性**：$f(x+T)=f(x),\ T\ \text{为周期}$

### 零点
- **存在定理**：$f(a)\cdot f(b) < 0 \ \Rightarrow\ (a,b)\ \text{内至少一零点}$

## 三、导数

### 基本公式
- **定义**：$f'(x) = \lim_{\Delta x \to 0} \dfrac{f(x+\Delta x)-f(x)}{\Delta x}$
- **常·幂**：$C' = 0;\quad (x^a)' = a x^{a-1};\quad (x)' = 1$
- **指数·对数**：$(e^x)' = e^x;\quad (a^x)' = a^x \ln a;\quad (\ln x)' = \dfrac{1}{x}$

### 运算法则
- **四则**：$(u \pm v)' = u' \pm v';\quad (uv)' = u'v + uv';\quad \left(\dfrac{u}{v}\right)' = \dfrac{u'v - uv'}{v^2}$
- **复合**：$[f(g(x))]' = f'(g(x)) \cdot g'(x)$

### 几何
- **切线**：$y - f(x_0) = f'(x_0)(x - x_0)$

> 💡 $f'(x)>0$ 增，$f'(x)<0$ 减；$f'(x)=0$ 且变号 $\Rightarrow$ 极值点。

## 四、三角函数

### 同角关系
- **平方**：$\sin^2\alpha + \cos^2\alpha = 1$
- **商**：$\tan\alpha = \dfrac{\sin\alpha}{\cos\alpha}$

### 诱导公式
- **口诀**：奇变偶不变，符号看象限

### 和差公式
- **正弦**：$\sin(\alpha \pm \beta) = \sin\alpha\cos\beta \pm \cos\alpha\sin\beta$
- **余弦**：$\cos(\alpha \pm \beta) = \cos\alpha\cos\beta \mp \sin\alpha\sin\beta$
- **正切**：$\tan(\alpha \pm \beta) = \dfrac{\tan\alpha \pm \tan\beta}{1 \mp \tan\alpha\tan\beta}$

### 二倍角
- **正弦**：$\sin 2\alpha = 2\sin\alpha\cos\alpha$
- **余弦**：$\cos 2\alpha = \cos^2\alpha - \sin^2\alpha = 2\cos^2\alpha - 1 = 1 - 2\sin^2\alpha$

### 降幂
- $\sin^2\alpha = \dfrac{1-\cos 2\alpha}{2};\quad \cos^2\alpha = \dfrac{1+\cos 2\alpha}{2}$

### 辅助角
- **合一**：$a\sin x + b\cos x = \sqrt{a^2+b^2}\,\sin(x+\varphi)$

### 图象变换
- **周期**：$y = A\sin(\omega x + \varphi),\ T = \dfrac{2\pi}{|\omega|}$

> 💡 二倍角余弦三个形式要会互相转化，降幂公式是解三角题的常客。

## 五、解三角形

### 正弦定理
- $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C} = 2R$

### 余弦定理
- **余弦**：$c^2 = a^2 + b^2 - 2ab\cos C$
- **求角**：$\cos C = \dfrac{a^2+b^2-c^2}{2ab}$

### 面积
- $S = \dfrac{1}{2}ab\sin C = \dfrac{1}{2}bc\sin A = \dfrac{1}{2}ac\sin B$

## 六、数列

### 通项与前 n 项和
- **关系**：$a_n = S_n - S_{n-1}\ (n\ge 2);\quad a_1 = S_1$

### 等差数列
- **通项**：$a_n = a_1 + (n-1)d$
- **求和**：$S_n = \dfrac{n(a_1+a_n)}{2} = na_1 + \dfrac{n(n-1)d}{2}$
- **中项**：$2b = a + c$
- **性质**：$m+n=p+q \ \Rightarrow\ a_m + a_n = a_p + a_q$

### 等比数列
- **通项**：$a_n = a_1 q^{n-1}$
- **求和**：$S_n = \dfrac{a_1(1-q^n)}{1-q}\ (q\neq 1)$
- **中项**：$b^2 = ac$
- **性质**：$m+n=p+q \ \Rightarrow\ a_m \cdot a_n = a_p \cdot a_q$

### 裂项
- $\dfrac{1}{n(n+1)} = \dfrac{1}{n} - \dfrac{1}{n+1}$

## 七、不等式

### 一元二次
- **解集**：$ax^2+bx+c > 0:\ \text{大于取两边，小于取中间}$

### 基本不等式
- **均值**：$\dfrac{a+b}{2} \ge \sqrt{ab}\ (a,b>0)$
- **平方均值**：$\dfrac{a^2+b^2}{2} \ge \left(\dfrac{a+b}{2}\right)^2 \ge ab$

### 绝对值
- **三角不等**：$|a| - |b| \le |a \pm b| \le |a| + |b|$

> 💡 基本不等式三字诀：一正、二定、三相等。

## 八、立体几何

### 体积
- **柱**：$V = Sh$
- **锥**：$V = \dfrac{1}{3}Sh$
- **台**：$V = \dfrac{1}{3}h(S + \sqrt{SS'} + S')$
- **球**：$V = \dfrac{4}{3}\pi R^3;\quad S = 4\pi R^2$

### 空间角
- **线线角**：$\cos\theta = \dfrac{|\vec a \cdot \vec b|}{|\vec a|\,|\vec b|}$
- **线面角**：$\sin\theta = \dfrac{|\vec a \cdot \vec n|}{|\vec a|\,|\vec n|}\ (\vec n\ \text{为面法向量})$
- **二面角**：$\cos\theta = \dfrac{|\vec n_1 \cdot \vec n_2|}{|\vec n_1|\,|\vec n_2|}$

### 距离
- **点线距**：$d = \dfrac{|\vec a \times \vec b|}{|\vec a|}\ (\text{向量叉乘})$

## 九、解析几何

### 直线
- **斜率**：$k = \dfrac{y_2-y_1}{x_2-x_1}$
- **点斜式**：$y - y_0 = k(x - x_0)$
- **平行·垂直**：$\text{平行 } k_1=k_2;\quad \text{垂直 } k_1 k_2 = -1$
- **距离**：$\text{点}(x_0,y_0)\text{到直线 } Ax+By+C=0:\ d = \dfrac{|Ax_0+By_0+C|}{\sqrt{A^2+B^2}}$

### 圆
- **标准方程**：$(x-a)^2 + (y-b)^2 = r^2$
- **一般方程**：$x^2 + y^2 + Dx + Ey + F = 0\ (D^2+E^2-4F>0)$

### 椭圆
- **方程**：$\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1\ (a>b>0);\quad c^2 = a^2 - b^2$
- **离心率**：$e = \dfrac{c}{a} < 1$

### 双曲线
- **方程**：$\dfrac{x^2}{a^2} - \dfrac{y^2}{b^2} = 1;\quad c^2 = a^2 + b^2$
- **离心率**：$e = \dfrac{c}{a} > 1;\quad \text{渐近线 } y = \pm\dfrac{b}{a}x$

### 抛物线
- **方程**：$y^2 = 2px\ (p>0);\quad \text{焦点}\left(\dfrac{p}{2},0\right),\ \text{准线 } x = -\dfrac{p}{2}$

### 弦长
- **弦长**：$|AB| = \sqrt{1+k^2}\,|x_1 - x_2|$

> 💡 圆锥曲线大题固定套路：设直线 → 联立 → Δ>0 → 韦达定理 → 代入目标。

## 十、平面向量

### 基本量
- **模**：$|\vec a| = \sqrt{x^2+y^2}$
- **数量积**：$\vec a \cdot \vec b = |\vec a|\,|\vec b|\cos\theta = x_1 x_2 + y_1 y_2$

### 位置关系
- **平行**：$x_1 y_2 - x_2 y_1 = 0$
- **垂直**：$x_1 x_2 + y_1 y_2 = 0$
- **夹角**：$\cos\theta = \dfrac{x_1 x_2 + y_1 y_2}{\sqrt{x_1^2+y_1^2}\,\sqrt{x_2^2+y_2^2}}$
- **投影**：$\vec a\ \text{在}\ \vec b\ \text{上投影} = |\vec a|\cos\theta = \dfrac{\vec a \cdot \vec b}{|\vec b|}$

## 十一、复数

- **形式**：$z = a + bi\ (i^2 = -1),\ a\ \text{实部},\ b\ \text{虚部}$
- **模**：$|z| = \sqrt{a^2+b^2}$
- **共轭**：$\bar z = a - bi;\quad z \cdot \bar z = |z|^2$
- **除法**：$\dfrac{a+bi}{c+di} = \dfrac{(a+bi)(c-di)}{c^2+d^2}$

## 十二、概率与统计

### 排列组合
- **排列**：$A_n^m = \dfrac{n!}{(n-m)!}$
- **组合**：$C_n^m = \dfrac{n!}{m!(n-m)!};\quad C_n^m = C_n^{n-m}$

### 概率
- **古典**：$P(A) = \dfrac{m}{n}$
- **对立**：$P(\bar A) = 1 - P(A)$
- **独立**：$P(AB) = P(A)P(B)$
- **条件**：$P(B \mid A) = \dfrac{P(AB)}{P(A)}$

### 分布
- **二项**：$X \sim B(n,p):\ P(X=k) = C_n^k p^k (1-p)^{n-k};\quad E = np,\ D = np(1-p)$
- **期望方差**：$E(aX+b) = aE(X)+b;\quad D(aX+b) = a^2 D(X)$

### 统计
- **均值**：$\bar x = \dfrac{x_1+\dots+x_n}{n}$
- **方差**：$s^2 = \dfrac{1}{n}\sum_{i=1}^n (x_i - \bar x)^2;\quad s = \sqrt{s^2}$
