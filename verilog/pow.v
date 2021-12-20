// pow.v

module pow (
    input clk,
    input start,
    input [127:0] a,
    input [127:0] b,
    input [127:0] p,
    output reg [127:0] res,
    output reg valid
);

/*
    FSM states:
        IDLE == 2b00
        WAIT == 2b01
        WAIT_FOR_MOD == 2b10 
*/

reg [1:0] state;
reg [15:0] cnt;
reg [127:0] a_copy;
reg [127:0] b_copy;
reg [127:0] p_copy;

reg start_mod;
reg [127:0] mod_a;
reg [127:0] mod_b;
reg mod_started;
wire [127:0] mod_res;
wire mod_valid;

mod mod(
    .clk(clk),
    .start(start_mod),
    .a(mod_a),
    .b(p_copy),
    .res(mod_res),
    .valid(mod_valid)
);

always @(posedge start) begin
    cnt <= 0;
    valid <= 0;
end

always @(posedge clk) begin
    // $display("Pow state: %d", state);
    // $display("Pow res: %d", res);
    // $display("Pow b: %b", b_copy);
    // $display("Mod res: %d", mod_res);
    // $display("\n####\n");
    case (state)

        2'b00: begin // IDLE
            if (start == 1'b1) begin
                a_copy <= a;
                b_copy <= b;
                p_copy <= p;
                mod_b <= p;
                res <= 128'b1;
            end
            state <= start;
        end

        2'b01: begin // WAIT
            if (start == 1'b1) begin
                state <= 1'b0;
            end
            else if (~valid) begin
                res = res * res;
                if (b_copy != 128'b0) begin
                    if (b_copy[127] == 1'b1) begin
                        res = res * a_copy;
                    end
                end
                mod_a = res;
                b_copy[127:0] = {b_copy[126:0], 1'b0};
                cnt = cnt + 1;
                state <= 2'b10;
                start_mod <= 1'b1;
            end
        end

        2'b10: begin // WAIT_FOR_MOD
            start_mod <= 1'b0;
            if (mod_valid == 1'b1) begin
                res <= mod_res;
                state <= 2'b01;
                if (cnt == 128) begin
                    valid <= 1;
                end
                // $display("%d mod %d = %d", mod_a, mod_b, mod_res);
            end
        end

        default: begin
            state <= 2'b00;
        end
    endcase
end

endmodule
