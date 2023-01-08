# **Modelagem e simulação de um levitador eletromagnético (MAGLEV) com Python**

Este projeto tem por objetivo servir como auxílio para a compreensão da dinâmica de um MAGLEV. Através de controles interativos será possível observar o comportamento do sistema, no qual os dados serão fornecidos pelo usúario, o que torna a experiência mais livre e didática.

## **Introdução**

Considerando que o objetivo do sistema MAGLEV é sustentar um corpo metálico levitando no ar, é importante analisar as forças que atuam sobre o corpo. Sendo o corpo influenciado pela ação do campo gravitacional da Terra, a força peso $p$ será proporcional à massa do corpo $m$ e à aceleração da gravidade $g$, atuando na direção do centro da Terra. 

Com o propósito de compensar a força peso, uma força magnética $F(x,I)$ de sentido oposto, é aplicada sobre o corpo. Esta força de atração é provocada por um campo magnético gerado a partir da circulação de uma corrente $I(t)$ na bobina do eletroímã, desta forma, atraindo o corpo e mantendo-o a uma distância $x(t)$ do núcleo. A distância $x(t)$ é considerada entre o centro de massa do corpo e a base do núcleo do eletroímã.
