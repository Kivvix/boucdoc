#!/usr/bin/env gnuplot

set terminal epslatex color font "Helvetica,12" standalone
xs = 0.3
xe = 0.7

set yrange [-0.1:1.1]
set samples 1000
set label "$x_s$" at (xs-0.02),-0.05
set label "$x_e$" at (xe-0.02),-0.05
h(x) = ( xs < x && x < xe ) ? 1 : 0

set output "h_gate.tex"
plot [0:1] h(x)

pas = 0.1
xss = xs+pas
xee = xe-pas
set yrange [-0.1:1.1]
set samples 1000
set label "$x_s$" at (xs-0.02),-0.05
set label "$x_e$" at (xe-0.02),-0.05
set label "$x_s^*$" at (xss-0.02),-0.05
set label "$x_e^*$" at (xee-0.02),-0.05
h(x) = ( xss < x && x < xee )? 1 : (xs < x && x<xss )? 1/(pas)*x-(xs)/pas : (xee <x && x<xe) ? -1/pas*x+(xe)/pas : 0
set arrow from xs,0 to xss,0 heads
set label "$\\delta x$" at xs+pas/2,0.05

set output "h_trap.tex"
plot [0:1] h(x)

