// tb.v

module tb;

    reg a, b;
    wire sum, carry;

    // duration for each bit = 20 * timescale = 20 * 1 ns  = 20ns
    localparam period = 20;  

    half_adder UUT (.a(a), .b(b), .sum(sum), .carry(carry));
    
    initial // initial block executes only once
        begin
            // values for a and b
            a = 0;
            b = 0;
            #period; // wait for period
            $monitor("At time %t, value = %h (%0d)", $time, sum, sum);

            a = 0;
            b = 1;
            #period;
            $monitor("At time %t, value = %h (%0d)", $time, sum, sum);

            a = 1;
            b = 0;
            #period;
            $monitor("At time %t, value = %h (%0d)", $time, sum, sum);

            a = 1;
            b = 1;
            #period;
            $monitor("At time %t, value = %h (%0d)", $time, sum, sum);

        end
endmodule
