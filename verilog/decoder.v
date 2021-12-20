// decoder.v

module decoder(
    input  [71:0]  signed_mes,
    output [9:0]   from_pub,
    output [9:0]   to_pub,
    output [19:0]  amt,
    output [31:0]  sig
);

assign from_pub = signed_mes[71:62];
assign to_pub   = signed_mes[61:52];
assign amt      = signed_mes[51:32];
assign sig      = signed_mes[31:0];

endmodule