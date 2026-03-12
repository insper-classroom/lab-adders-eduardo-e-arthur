#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b
        pass

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]  # (1)

    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, vaiUm):

    @always_comb
    def comb():

        # Bit 0
        soma[0].next = x[0] ^ y[0]
        c1 = x[0] & y[0]

        # Bit 1
        soma[1].next = x[1] ^ y[1] ^ c1

        vaiUm.next = (x[1] & y[1]) | (x[1] & c1) | (y[1] & c1)

    return instances()
    



@block
def adder(x, y, soma, carry):

    n = len(x)

    # lista para armazenar os full adders
    faList = [None for _ in range(n)]

    # lista de carries intermediários
    carryList = [Signal(bool(0)) for _ in range(n)]

    for i in range(n):

        if i == 0:
            # primeiro FA recebe carry 0
            faList[i] = fullAdder(
                x[i],
                y[i],
                0,
                soma[i],
                carryList[i]
            )
        else:
            faList[i] = fullAdder(
                x[i],
                y[i],
                carryList[i-1],
                soma[i],
                carryList[i]
            )

    # carry final
    @always_comb
    def assignCarry():
        carry.next = carryList[n-1]

    return instances()


@block
def addervb(x, y, soma, carry):

    @always_comb
    def comb():
        total = int(x) + int(y)

        soma.next = total & 0xFF        # 8 bits
        carry.next = (total >> 8) & 1   # bit 8

    return comb