module spi_master (
  input wire clk,
  input wire reset,
  output wire cs,
  output wire mosi,
  input wire miso,
  input [7:0] image_byte_data,
  input wire image_data_valid,
  output wire image_transmitted
);

  reg [7:0] tx_data;
  reg [7:0] rx_data;
  reg spi_enable;
  reg spi_done;

  // Initialize SPI signals
  assign cs = 1'b1;    // Chip select (CS) high (inactive)
  assign mosi = 1'b0;  // MOSI data line initially low

  always @(posedge clk or posedge reset) begin
    if (reset) begin
      spi_enable <= 1'b0;
      spi_done <= 1'b0;
      tx_data <= 8'b0;
    end else begin
      if (spi_enable) begin
        // Start SPI transaction
        cs <= 1'b0;  // Activate chip select (CS)
        mosi <= tx_data[7];  // Send most significant bit first

        // Shift out the data and shift in the received data
        // Assuming 8-bit data width
        for (int i = 6; i >= 0; i = i - 1) begin
          @(posedge clk);
          mosi <= tx_data[i];
          rx_data[i+1] <= miso;
        end

        rx_data[0] <= miso;

        // End SPI transaction
        cs <= 1'b1;  // Deactivate chip select (CS)
        spi_done <= 1'b1;
      end else begin
        spi_done <= 1'b0;
      end
    end
  end

  // Control the SPI transaction when image data is valid
  always @(posedge clk) begin
    if (reset) begin
      spi_enable <= 1'b0;
    end else begin
      if (image_data_valid && !spi_enable) begin
        spi_enable <= 1'b1;
        tx_data <= image_byte_data;
        image_transmitted <= 1'b0;
      end else if (spi_done) begin
        spi_enable <= 1'b0;
        image_transmitted <= 1'b1;
      end
    end
  end

  // Other modules and logic in the FPGA design

endmodule
