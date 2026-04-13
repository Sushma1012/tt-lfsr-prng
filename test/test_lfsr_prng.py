import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

@cocotb.test()
async def test_lfsr_runs(dut):
    """Test that LFSR produces changing output when enabled."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    dut.ui_in.value = 0b00000001   # enable=1
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # Collect 16 consecutive LFSR outputs
    outputs = []
    for _ in range(16):
        await RisingEdge(dut.clk)
        outputs.append(int(dut.uio_out.value))

    unique = len(set(outputs))
    assert unique > 8, f"Expected varied LFSR output, got only {unique} unique values"
    print(f"PASS: {unique} unique values in 16 cycles. Outputs: {outputs}")


@cocotb.test()
async def test_lfsr_pauses(dut):
    """Test that LFSR holds its value when enable=0."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.ui_in.value = 0b00000001
    dut.uio_in.value = 0
    dut.ena.value = 1
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    # Pause
    dut.ui_in.value = 0b00000000
    await RisingEdge(dut.clk)
    val_before = int(dut.uio_out.value)
    await ClockCycles(dut.clk, 5)
    val_after = int(dut.uio_out.value)

    assert val_before == val_after, f"FAIL: LFSR changed while paused! {val_before} -> {val_after}"
    print(f"PASS: LFSR held value {val_before:#04x} for 5 cycles while paused.")
