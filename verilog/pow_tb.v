// pow_tb.v

`timescale 1 ns/10 ps


module pow_tb;

    integer i;

    reg clk = 0;

    reg [127:0] a;
    reg [127:0] b;
    reg [127:0] p;
    reg start;
    reg started;
    reg [15:0] cnt;

    wire valid;
    wire [127:0] res;

    pow pow(
        .clk(clk),
        .start(start),
        .a(a),
        .b(b),
        .p(p),
        .res(res),
        .valid(valid)
    );

    always #5 clk<=~clk;

    initial begin

        a = 25;
        b = 23;
        p = 18;
        started = 0;
        start = 0;
        cnt <= 0;
    end

    always @(posedge clk) begin
        cnt = cnt + 1;
        case (started)
            0: begin
                start = 1;
                started = 1;
            end

            1: begin
                start = 0;
                if (valid) begin
                    $display("res = %d", res);
                    $finish;
                end
            end
        endcase
    end

endmodule