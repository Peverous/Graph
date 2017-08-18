library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity example_fsm is
port (clk	: in std_logic;
	rst	: in std_logic;
	cnt_val	: in std_logic_vector(7 downto 0);
	prod	: in std_logic_vector(15 downto 0);
	en_cnt	: out std_logic;
	finished: out std_logic;
	enable	: out std_logic);
end example_fsm;

architecture fsm of example_fsm is
type dc_state is (init,dc,udp,idle);
constant max1 		: std_logic_vector(15 downto 0):=(others=>'1');
constant max2		: std_logic_vector(7 downto 0):=(others=>'1');
constant max3		: std_logic_vector(15 downto 0):=(15=>'0',others=>'1');
signal current_state 	: dc_state;
signal next_state	: dc_state;
signal en_cnt_o		: std_logic;
signal enable_o		: std_logic;
signal finished_o	: std_logic;

begin
U_clk : process(clk)
	begin
	if(clk'event and clk='1') then
		if (rst='1') then
			current_state	<= init;
			en_cnt		<='0';
			finished	<='0';
			enable		<='0';
		else
			current_state	<= next_state;
			en_cnt		<= en_cnt_o;
			finished	<= finished_o;
			enable		<= enable_o;
		end if;
	end if;
end process U_clk;

U_out_dec : process(current_state)
	begin
	if (current_state=init) then
		en_cnt_o	<= '0';
		finished_o	<= '0';
		enable_o	<= '0';

	elsif (current_state=dc) then
		en_cnt_o	<='0';
		finished_o	<='0';
		enable_o	<='1';

	elsif (current_state=udp) then
		en_cnt_o	<= '1';
		finished_o	<= '0';
		enable_o	<= '0';

	elsif (current_state=idle) then
		en_cnt_o	<= '0';
		finished_o	<= '1';
		enable_o	<= '0';

	end if;
end process U_out_dec;

U_next_state : process(current_state,cnt_val,prod)
	begin
	case(current_state) is
		when init =>
			next_state	<=dc;

		when dc =>
			if (prod=max1) then
				next_state	<=udp;
			else
				next_state	<=dc;
			end if;

		when udp =>
			if (prod=max3) then
				if (cnt_val=max2) then
					next_state	<=idle;
				else
					next_state	<=dc;
				end if;
			else
				next_state		<=udp;
			end if;

		when idle =>
			next_state		<=idle;

		when others =>
			next_state		<=idle;
	end case;
end process U_next_state;

end fsm;
