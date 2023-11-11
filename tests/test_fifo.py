import os
from pathlib import Path

import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb.runner import get_runner

import numpy as np

@cocotb.test()
    dut.data_in.value = 0
    dut.rst_n.value = 0

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk)
    val = 0
    result = []
    exp = [0, 0]
    maf = moving_average_filter(8)

    for i in range(20):
        if i <= 1:
            dut.rst_n.value = 0
        else:
            dut.rst_n.value = 1
        if i < 4:
            val = 0
        else: 
            val = 500
    
        dut.data_in.value = val  
        expected = maf.filter(val)
        await RisingEdge(dut.clk)
        result.append(int(dut.data_out.value))
        exp.append(int(expected))

    # Check the final input on the next clock
    await RisingEdge(dut.clk)

    print(f" The HDL result: {result}")
    print(f" The python result: {exp}")
    plt.figure(1)
    plt.title("Moving average filter")
    plt.plot(result)
    plt.plot(exp)
    plt.xlabel("Samples (1)")
    plt.ylabel("Value (1)")
    plt.grid(True)
    plt.legend(["Verilog", "Python"])
    plt.savefig('foo.png')




def test_simple_shifter_runner():
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent

    verilog_sources = []
    vhdl_sources = []

    if hdl_toplevel_lang == "verilog":
        verilog_sources = [proj_path / "shifter.sv"]
    else:
        vhdl_sources = [proj_path / "shifter.vhdl"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="shifter",
        always=True,
    )

    runner.test(hdl_toplevel="shifter", test_module="test_shifter,")


if __name__ == "__main__":
    test_simple_shifter_runner()
