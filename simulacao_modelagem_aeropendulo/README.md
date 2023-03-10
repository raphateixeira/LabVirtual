
# Modelagem e Simulação Aeropêndulo

<center>
<div class="figure" >
  <img src="utils/aeropendulo.png">
  <p>Figura 1 - Diagrama esquemático do Aeropêndulo.</p>
</div>
</center>

Usando as leis de Newton e momentos angulares podemos encontrar o modelo matemático que descreve a dinâmica do aeropêndulo, assim, temos a equação $(1)$ que modela o sistema em questão.

$$
    T = J\ddot{\theta} + c\dot{\theta} +mgd\sin{\theta}
$$


Onde:

>> + $T$: Empuxo gerado pela hélice;
>> + $J$: Momento de inércia;
>> + $\theta$: posição angular do Aeropêndulo;
>> + $c$: coeficiente de amortecimento viscoso;
>> + $m$: peso do Aeropêndulo;
>> + $d$: a distância entre o centro de massa e o ponto de pivô;

#### Linearizando o sistema

Uma das técnicas de linearização quando se tem sistemas não lineares que a componente não linear é o seno ou cosseno é  considerar o seno ou cosseno sendo o valor do próprio ângulo, isso funciona bem para pequenas variações em torno do ângulo, aplicando essa técnica ao modelo do aeropêndulo, temos a equação $(2)$.

$$
    T = J\ddot{\theta} + c\dot{\theta} +mgd\theta
$$

Aplicando a transformada de Laplace, temos:

$$
    T(s) = s^2J\theta(s) + sc\theta(s) +mgd\theta(s)
    T(s) = (s^2J + sc +mgd)\theta(s)
    \frac{\theta(s)}{T(s)} = \frac{1}{s^2J + sc +mgd}
    \frac{\theta(s)}{T(s)} = \frac{1/J}{s^2 + sc/J +mgd/J}
$$

Queremos controlar o ângulo do braço do aeropêndulo  a partir da tensão aplicada aos terminais do motor, assim,devemos encontrar uma relação entre a tensão $V$ nos terminais do motor e o empuxo $T$ gerado pela hélice, essa relação é não linear, porém é possível aproximar por uma relação linear, como mostra a expressão $(7)$.

$$
    T \approx K_mV
$$

Aplicando a transformada de Laplace, temos:

$$
    T(s) \approx K_mV(s)
$$

Agora podemos substituir $(8)$ em $(6)$,

$$
    \frac{\theta(s)}{K_mV(s)} = \frac{1/J}{s^2 + sc/J +mgd/J}
    \frac{\theta(s)}{V(s)} = \frac{K_m/J}{s^2 + sc/J +mgd/J}
$$


### Sistema no Espaço de Estados

##### Forma Canônica de Controlador

$$
    x_1=\theta \quad x_2=\dot{\theta} \quad x_2 = \dot{x_1}
$$


$$
\begin{bmatrix}
    \dot{x}_1 \\
    \dot{x}_2
\end{bmatrix}=
\begin{bmatrix}
    0             & 1\\
    -\frac{mgd}{J} & -\frac{c}{J}
\end{bmatrix}\cdot 
\begin{bmatrix}
    x_1 \\
    x_2
\end{bmatrix}+
\begin{bmatrix}
    0 \\
    \frac{K_m}{J}
\end{bmatrix}\cdot u
$$

$$
Y= \begin{bmatrix}
    1 & 0
\end{bmatrix} \cdot
\begin{bmatrix}
    0 \\
    \frac{K_m}{J}
\end{bmatrix} + 0
$$


#### Parâmetros para Simulação

$$
\begin{align}
\begin{array}{|c|c|}                                        \hline
\text { Parâmetros do Aeropêndulo } & \text{Valores}      \\ \hline
K_m     &   0,0296                                        \\ \hline
d       &   0,03m                                         \\ \hline
J       &   0,0106 Kgm^2                                  \\ \hline
m       &   0,36 m                                        \\ \hline
g       &   9,8 m/s^2                                     \\ \hline
c       &   0,0076 Nms/rad                                \\ \hline
\end{array}
\end{align}
$$

---

### Simulação usando Python


```
import numpy as np
import matplotlib.pyplot as plt
import control as ct

plt.style.use("ggplot")
```

Parâmetros

```
K_m = 0.0296
m = 0.36
d = 0.03
J = 0.0106
g = 9.8
c = 0.0076
```

Matrizes do sistema no espaço de estados

```
A = np.array([[0, 1],
              [-(m*g*d)/J, -(c/J)]])

B = np.array([[0, K_m/J]]).T

C = np.array([1, 0])

D = 0
```

### Sistema no Espaço de Estados

```
sys = ct.ss(A, B, C, D)
print(sys)
```

Função de Transferência a partir do espaço de estados

```
Gs = ct.ss2tf(sys)
Gs
```

Informações do sistema em malha aberta

```
ct.step_info(sys)
```

```
ct.damp(sys);
```

```
ct.poles(sys)
```

```
ct.zeros(sys)
```

Resposta ao Degrau Unitário

```
t, yout = ct.step_response(Gs)

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.set_title("Aeropêndulo em Malha Aberta")
ax.set_ylabel("Ângulo (Graus°)")
ax.set_xlabel("Tempo (s)")
ax.plot(t, np.rad2deg(yout))
plt.show()
```

---

