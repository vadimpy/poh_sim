// mod.v

module mod(
    input clk,
    input start,
    input [127:0] a,
    input [127:0] b,
    output reg [127:0] res,
    output reg valid
);


reg state;
reg [127:0] b_copy;
assign lower = res < b_copy;

always @(posedge start) begin
    valid <= 0;
end

always @(posedge clk) begin
    case (start)
        1'b1: begin
            res <= a;
            b_copy <= b;
            valid <= 0;
        end

        1'b0: begin
            if (~lower) begin
                res <= res - b_copy;
                valid <= 0;
            end
            else begin
                valid <= 1;
            end
        end
    endcase
end

endmodule