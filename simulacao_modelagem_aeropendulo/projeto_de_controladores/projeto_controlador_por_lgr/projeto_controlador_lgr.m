% Projeto de controlador por LGR
clear all; close all; clc

num = [2.792]
den = [1, 0.717, 9.985]

Gs = tf(num, den)

rlocus(Gs)
grid on

% projeto por lgr

% sisotool(Gs)
