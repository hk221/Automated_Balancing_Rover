module decision(

    // global clock & reset
    input	clk;
    input	reset_n;

    // mm slave
    input							s_chipselect;
    input							s_read;
    input							s_write;
    output	reg	[31:0]	            s_readdata;
    input	[31:0]				    s_writedata;
    input	[2:0]					s_address;


    // streaming sink
    input	[23:0]                	sink_data;
    input						    sink_valid;
    output							sink_ready;
    input							sink_sop;
    input						    sink_eop;

    // streaming source
    output	[23:0]			  	   source_data;
    output						   source_valid;
    input						   source_ready;
    output						   source_sop;
    output						   source_eop;

    // conduit export
    input                         mode;
);


endmodule