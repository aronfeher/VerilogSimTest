module fifo #(
  parameter integer DATA_WIDTH = 32,
  parameter integer FIFO_DEPTH = 4
)(
  input logic i_clk,
  input logic i_rst_n,
  input logic i_read,
  input logic i_write,
  output reg o_full,
  output reg o_empty,
  input logic [DATA_WIDTH-1:0] i_data,
  output reg [DATA_WIDTH-1:0] o_data
);

  reg [DATA_WIDTH-1:0] memory [0:FIFO_DEPTH];
  reg [$clog2(FIFO_DEPTH)-1:0] write_ptr, read_ptr;

  assign o_empty = (write_ptr == read_ptr);
  assign o_full = (write_ptr + 1 == read_ptr);

  integer i = 0;

  always @(posedge i_clk) begin
    if(!i_rst_n) begin
      write_ptr <= 0;
      read_ptr <= 0;
      for(i = 0; i < FIFO_DEPTH; i=i+1) begin
        memory[i] <= 0;
      end
    else begin
      if(i_write & ~o_full) begin
        memory[write_ptr] <= i_data;
        write_ptr = write_ptr + 1;
      end
      if(i_read & ~o_empty) begin
        o_data <= memory[read_ptr];
        read_ptr = read_ptr + 1;
      end
    end

  end

endmodule
