/*
 * tt_um_lfsr_prng.v
 *
 * 16-bit Fibonacci LFSR Pseudo-Random Number Generator
 * with 7-segment display output.
 *
 * Taps: bits 16, 15, 13, 4 (maximal-length polynomial x^16+x^15+x^13+x^4+1)
 *
 * Inputs:
 *   ui_in[0]  - enable (run when high, pause when low)
 *   ui_in[1]  - load seed (loads ui_in[7:2] as partial seed when pulsed high)
 *
 * Outputs:
 *   uo_out[6:0] - 7-segment encoded lower nibble of LFSR (segments a-g)
 *   uio_out[7:0] - raw LFSR[7:0] for inspection
 */

`default_nettype none

module tt_um_lfsr_prng (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // -------------------------------------------------------
    // 16-bit LFSR register
    // -------------------------------------------------------
    reg [15:0] lfsr;

    // Feedback taps: positions 16,15,13,4 (1-indexed from LSB)
    // In 0-indexed: bits 15, 14, 12, 3
    wire feedback = lfsr[15] ^ lfsr[14] ^ lfsr[12] ^ lfsr[3];

    wire enable    = ui_in[0];
    wire load_seed = ui_in[1];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lfsr <= 16'hACE1;          // non-zero seed on reset
        end else if (load_seed) begin
            // Load a custom seed from upper 6 bits of ui_in, padded
            lfsr <= {ui_in[7:2], 10'b1010101010};
        end else if (enable) begin
            lfsr <= {lfsr[14:0], feedback};
        end
        // else: hold current value
    end

    // -------------------------------------------------------
    // 7-segment encoder for lower nibble of LFSR
    // Segments: [6]=g [5]=f [4]=e [3]=d [2]=c [1]=b [0]=a
    // -------------------------------------------------------
    reg [6:0] seg;
    always @(*) begin
        case (lfsr[3:0])
            4'h0: seg = 7'b0111111; // 0
            4'h1: seg = 7'b0000110; // 1
            4'h2: seg = 7'b1011011; // 2
            4'h3: seg = 7'b1001111; // 3
            4'h4: seg = 7'b1100110; // 4
            4'h5: seg = 7'b1101101; // 5
            4'h6: seg = 7'b1111101; // 6
            4'h7: seg = 7'b0000111; // 7
            4'h8: seg = 7'b1111111; // 8
            4'h9: seg = 7'b1101111; // 9
            4'hA: seg = 7'b1110111; // A
            4'hB: seg = 7'b1111100; // b
            4'hC: seg = 7'b0111001; // C
            4'hD: seg = 7'b1011110; // d
            4'hE: seg = 7'b1111001; // E
            4'hF: seg = 7'b1110001; // F
            default: seg = 7'b0000000;
        endcase
    end

    assign uo_out  = {1'b0, seg};     // bit 7 unused, bits 6:0 = segments
    assign uio_out = lfsr[7:0];       // expose lower byte of LFSR
    assign uio_oe  = 8'hFF;           // all bidir pins as output

endmodule
