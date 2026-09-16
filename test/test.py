# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1

    dut._log.info("Testing Full Adder")

    # Full adder truth table
    test_cases = [
        (0, 0, 0, 0, 0),
        (0, 0, 1, 1, 0),
        (0, 1, 0, 1, 0),
        (0, 1, 1, 0, 1),
        (1, 0, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (1, 1, 0, 0, 1),
        (1, 1, 1, 1, 1),
    ]

    for A, B, Cin, expected_sum, expected_cout in test_cases:

        # A -> ui_in[0]
        # B -> ui_in[1]
        # Cin -> ui_in[2]
        dut.ui_in.value = A | (B << 1) | (Cin << 2)

        await ClockCycles(dut.clk, 1)

        # uo_out[0] = Sum
        # uo_out[1] = Cout
        actual_sum = dut.uo_out.value.integer & 1
        actual_cout = (dut.uo_out.value.integer >> 1) & 1

        assert actual_sum == expected_sum, (
            f"Sum error: A={A}, B={B}, Cin={Cin}, "
            f"Expected={expected_sum}, Got={actual_sum}"
        )

        assert actual_cout == expected_cout, (
            f"Cout error: A={A}, B={B}, Cin={Cin}, "
            f"Expected={expected_cout}, Got={actual_cout}"
        )

        dut._log.info(
            f"A={A} B={B} Cin={Cin} -> "
            f"Sum={actual_sum} Cout={actual_cout}"
        )

    dut._log.info("All Full Adder tests passed!")
