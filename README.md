# LFSR Pseudo-Random Number Generator — Tiny Tapeout TTSKY26a

## What does it do?
This design implements a **16-bit Fibonacci Linear Feedback Shift Register (LFSR)** 
using the maximal-length polynomial x^16 + x^15 + x^13 + x^4 + 1. It generates 
a pseudo-random sequence of 65,535 unique values before repeating.

The lower nibble (4 bits) of the LFSR drives a **7-segment display decoder**, 
cycling through hex digits 0–F. The raw lower byte is also exposed on the 
bidirectional pins for external inspection.

## How to use it
| Pin        | Function                                      |
|------------|-----------------------------------------------|
| `ui_in[0]` | Enable — LFSR advances on each clock when high |
| `ui_in[1]` | Load seed — loads custom seed when pulsed high |
| `ui_in[7:2]`| Seed bits (upper 6 bits used when loading)   |
| `uo_out[6:0]`| 7-segment encoded lower nibble of LFSR     |
| `uio_out[7:0]`| Raw LFSR[7:0]                             |
| `clk`      | System clock (up to 50 MHz)                   |
| `rst_n`    | Active-low reset (seeds LFSR to 0xACE1)       |

## Theory
An LFSR shifts bits through a register and XORs selected taps to produce the 
feedback bit. With the correct tap polynomial, this achieves the maximum possible 
period of 2^n - 1 states for an n-bit register.

## Tools Used
- Icarus Verilog (simulation)
- GTKWave (waveform viewing)
- Yosys (synthesis check)
- cocotb (Python testbench)
- OpenLane / SKY130 PDK (via GitHub Actions)
