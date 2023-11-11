import os
from pathlib import Path

import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb.runner import get_runner

import numpy as np

@cocotb.test()
async def fifo_test(dut):
    dut.i_data.value = 0
    dut.i_rst_n.value = 0

    clock = Clock(dut.i_clk, 10, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.i_clk)

    result_data = []
    result_full = []
    result_empty = []

    for i in range(15):
        if i <= 1:
            dut.i_rst_n.value = 0
        else:
            dut.i_rst_n.value = 1
        if 2 <= i <= 5:
            dut.i_write.value = 1
            dut.i_read.value = 0
            dut.i_data.value = i
        else:
            if 6 <= i <= 9: 
                dut.i_write.value = 0
                dut.i_read.value = 1
                temp = dut.o_data.value
            else:
                dut.i_write.value = 1
                dut.i_read.value = 1
                dut.i_data.value = i
                temp = dut.o_data.value
    
        await RisingEdge(dut.i_clk)
        result_data.append(temp)
        result_full.append(int(dut.o_full))
        result_empty.append(int(dut.o_empty))

    # Check the final input on the next clock
    await RisingEdge(dut.i_clk)

    print(f" The HDL result: {result_data}")
    print(f" The HDL full result: {result_full}")
    print(f" The HDL empty result: {result_empty}")




def test_simple_fifo_runner():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent

    verilog_sources = []

    if hdl_toplevel_lang == "verilog":
        verilog_sources = [proj_path / "fifo.sv"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="fifo",
        always=True,
    )

    runner.test(hdl_toplevel="fifo", test_module="test_fifo,")


if __name__ == "__main__":
    test_simple_fifo_runner()
