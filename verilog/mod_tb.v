// mod_tb.v

`timescale 1 ns/10 ps


module mod_tb;

    integer i;

    reg clk = 0;

    reg [127:0] a;
    reg [127:0] b;
    reg start;
    reg started;

    wire valid;
    wire [127:0] res;

    mod m(clk, start, a, b, res, valid);

    always #5 clk<=~clk;

    initial begin

        a = 145;
        b = 13;
        started = 0;
        start = 0;

        $display("expected = %d", a % b);
    end

    always @(posedge clk) begin
        case (started)
            0: begin
                start = 1;
                started = 1;
            end

            1: begin
                start = 0;
                $display("res = %d", res);
                if (valid) begin
                    $finish;
                end
            end
        endcase
    end

endmodule