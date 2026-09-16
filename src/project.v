/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_fulladder (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // Full Adder Inputs
    wire A;
    wire B;
    wire Cin;

    // Full Adder Outputs
    wire Sum;
    wire Cout;

    assign A   = ui_in[0];
    assign B   = ui_in[1];
    assign Cin = ui_in[2];

    // Full Adder Logic
    assign Sum  = A ^ B ^ Cin;
    assign Cout = (A & B) | (B & Cin) | (A & Cin);

    // Output mapping
    assign uo_out[0] = Sum;
    assign uo_out[1] = Cout;

    // Unused output pins
    assign uo_out[7:2] = 6'b000000;

    // Bidirectional pins unused
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

    // Prevent unused-input warnings
    wire _unused = &{ena, clk, rst_n, uio_in};

endmodule
