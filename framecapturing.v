module VideoDecoder (
  input wire clk,
  input wire reset,
  input wire compressed_video,
  output wire [7:0] decoded_video,
  output wire frame_capture_trigger
);

  // ...

  reg [31:0] frame_counter;
  reg frame_capture_trigger;

  always @(posedge clk or posedge reset) begin
    if (reset) begin
      // Reset frame counter and trigger
      frame_counter <= 0;
      frame_capture_trigger <= 0;
      // Reset other signals and registers
    end else begin
      // State machine
      case (state)
        // ...

        MOTION_COMPENSATION: begin
          // ...

          if (motion_compensation_finished) begin
            // ...

            // Increment frame counter
            frame_counter <= frame_counter + 1;

            // Check if it's time to capture a frame
            if (frame_counter == 5 * FRAME_RATE) begin
              frame_counter <= 0;
              frame_capture_trigger <= 1; // Set frame capture trigger high
            end else begin
              frame_capture_trigger <= 0; // Set frame capture trigger low
            end

            // ...
          end
        end

        // ...

      endcase
    end
  end

  // ...

endmodule
