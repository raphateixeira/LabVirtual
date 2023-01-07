# **Modelagem e simulação de um levitador eletromagnético (MAGLEV) com Python**

Este projeto tem por objetivo servir como auxílio para a compreensão da dinâmica de um MAGLEV. Através de controles interativos será possível observar o comportamento do sistema, no qual os dados serão fornecidos pelo usúario, o que torna a experiência mais livre e didática.

## **Equação de movimento (Entrada: corrente, Saída: posição)**

Considerando que o objetivo do sistema MAGLEV é sustentar um corpo metálico levitando no ar, é importante analisar as forças que atuam sobre o corpo. Sendo o corpo influenciado pela ação do campo gravitacional da Terra, a força peso $p$ será proporcional à massa do corpo $m$ e à aceleração da gravidade $g$, atuando na direção do centro da Terra. 

Com o propósito de compensar a força peso, uma força magnética $F(x,I)$ de sentido oposto, é aplicada sobre o corpo. Esta força de atração é provocada por um campo magnético gerado a partir da circulação de uma corrente $I(t)$ na bobina do eletroímã, desta forma, atraindo o corpo e mantendo-o a uma distância $x(t)$ do núcleo. A distância $x(t)$ é considerada entre o centro de massa do corpo e a base do núcleo do eletroímã.

$\ddot{x} = g - \dfrac{F(x,I)}{m}$

onde $F(x,I)$ é a força magnética exercida pela bobina sobre o imã/cilindro. 

Nosso melhor modelo para $F$ hoje é:

$F(x,I)=\dfrac{k\,I^2}{(x+\mu)^2}$

## **Amplificador**

Se a entrada for tensão, substituir:

$I = Gv$

onde $G$ é o ganho do amplificador.

## **Sensor**

Se a posição for a saída do sensor (em Volts), então usar $y = f(x)$, onde $f$ é a função do sensor.

## **Espaço de Estados**

O modelo de espaço de estados não-linear, considerando $x_1$ a posição e $x_2$ a velocidade, fica:

$\dot{x}_1 = x_2$

$\dot{x}_2 = g - \dfrac{kI^2}{m(x_1-\mu)^2}$

## **Equilíbrio**

O sistema está em equilíbrio quando todas as derivadas em relação ao tempo são nulas. Assim:

$0 = x_2^*$ 

$mg = \dfrac{kI_0^2}{(x_1^*+\mu)^2}$

Desta forma, dada  uma posição de equilíbrio $x_1^*=x_0$ podemos achar a corrente de equilíbrio $I_0$ ou vice-versa. 

## **Linearização**

Seja:
$\Delta x_1 = x_1 - x_1^*$

$\Delta x_2 = x_2 - x_2^*$

$\Delta I = I - I_0$

Calculando o Jacobiano no ponto de equilíbrio e organizando a notação, temos:

$\Delta \dot{x}_1 = \Delta x_2$

$\Delta \dot{x}_2 = -a\,\Delta I +\lambda^2 \Delta x_1$

$y = x_1$


onde:

$a = \dfrac{1}{m}\,\left.\dfrac{\partial F}{\partial I}\right|_{x_0,I_0} = \dfrac{2kI_0}{m(x_0+\mu)^2}$

$-\lambda^2 = \dfrac{1}{m}\,\left.\dfrac{\partial F}{\partial x}\right|_{x_0,I_0} = \dfrac{-2kI_0^2}{(x_0+\mu)^3} \Rightarrow \lambda = \displaystyle\sqrt{\dfrac{2kI_0^2}{m(x_0+\mu)^3}}$

## **Simulação**

**[Simulação de sistema dinâmico com python](ManimEDO.html)**

