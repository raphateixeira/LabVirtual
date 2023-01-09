# **Modelagem e simulação de um Motor DC com Python**

Este projeto tem por objetivo servir como auxílio para a compreensão da dinâmica de um motor de corrente contínua. Através de controles interativos será possível observar o comportamento do sistema, no qual os dados serão fornecidos pelo usúario, o que torna a experiência mais livre e didática.


# Motor DC
## **Introdução**

Um motor é uma máquina que converte energia elétrica em energia mecânica de rotação.O funcionamento dos motores CC baseia-se no princípio do eletromagnetismo clássico pelo qual um condutor carregando uma corrente e mergulhado em um fluxo magnético fica submetido a uma força eletromagnética.

Realizaremos uma simulação de um sistema contendo um motor DC:

<br/>

<div align="center">
   <img src="motordc.png" width="400" />
</div>
<div align="center">
  <span> Figura 1: Circuito do Motor DC </span>
</div>

## **Modelagem do Motor**
Usando a Lei de Kirchhoff, a tensão contra eletromotriz pode ser descrita por:


$$
E_{emf}=K_m \ddot{\theta }
$$

No eixo do motor é conectado um redutor, com relação de redução $Kg$ e eficiência
$\eta_g$. Assim, aplicando a segunda lei de Newton no eixo do motor, temos:
$$
J_m\ddot{\theta }=T_m-\frac{T_l}{\eta_g K_g}
$$

Aplicando a segunda lei de Newton na carga conectada ao redutor, temos:

$$ J_l\ddot{\theta_l }=T_l-B_{eq}\dot{\theta_l}
$$

Combinando as três equações acima :

$$
\left ( J_l+\eta_g K^2_g J_m \right )R_m\ddot{\theta } + \left ( B_{eq}R_m+\eta_g \eta_m K_m K_l K^2_g  \right )R_m\dot{\theta } = \eta_g \eta_m K_g K_t V_m
$$

 Aplicando a transformada de Laplace, chegamos à seguinte função transferência:

$$
\frac{\theta_l(s)}{V_m(s)}=\frac{\eta_g \eta_m K_g K_t}{J_{eq} R_m s^2 + \left ( B_{eq}R_m + \eta_g \eta_m K_m K_t K^2_g J_m \right )s}
$$
Sendo $J_{eq}=J_l + \eta_g K^2_g J_m$ o momento de inércia equivalente do motor.

Assumindo os seguintes valores para as constantes acima:


Eficiência da redução
$\eta_g = 0.9$

Eficiência do motor 
$\eta_g = 0.69$

Fator de redução 
$K_g = 70$

Constante de torque do motor
 $K_t = 0,00767$

Constante de força contra 
eletromotriz 
$K_m=0,00767$

Momento de inércia do motor 
$J_{m} = 3.87\cdot 10^{-7}$

Momento de inércia equivalente do sistema
$J_{eq} = 2\cdot 10^{-3}$



Resistência de armadura 
$R_m=2.6$

Fator de amortecimento viscose 
$B_{eq} = 4\cdot 10^{-3}$

A função transferência do motor é dada por:

$$
\frac{\theta_l(s)}{V_m(s)}=\frac{0.3334}{0.00512 s^2 + 0.1894s}=\frac{65}{ s^2 + 37s}
$$
