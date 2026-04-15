set_units -time ns -capacitance pF -current mA -voltage V -resistance kOhm

create_clock -name clk -period 20.0 [get_ports clk]
set_clock_transition 0.15 [get_clocks clk]
set_clock_uncertainty 0.5  [get_clocks clk]

set_input_delay  2.0 -clock clk [get_ports {ui_in[*]}]
set_input_delay  2.0 -clock clk [get_ports {uio_in[*]}]
set_input_delay  2.0 -clock clk [get_ports {ena rst_n}]

set_output_delay 2.0 -clock clk [get_ports {uo_out[*]}]
set_output_delay 2.0 -clock clk [get_ports {uio_oe[*]}]
set_output_delay 2.0 -clock clk [get_ports {uio_out[*]}]

set_driving_cell -lib_cell sky130_fd_sc_hd__inv_2 [get_ports {ui_in[*] uio_in[*] ena rst_n}]
set_load 0.5 [get_ports {uo_out[*] uio_out[*] uio_oe[*]}]

set_false_path -hold -from [get_ports rst_n]
