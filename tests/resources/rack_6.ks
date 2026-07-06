import cast_ons;
import bind_offs;
// adaptation of the simple thing pattern

with Gauge as 2, Carrier as 1, length as 25:{
// setup
	cast_ons.alt_tuck_cast_on(6);
	// RS = Leftward, front bed
	in Leftward direction:{
		knit Loops[0:3];
	}
	xfer Loops across;
	// WS = Rightward, back bed for garter
	in reverse direction:{
		knit Loops[3:6];
	}
	xfer Loops across;
	// set up increases and racking in this line 3
	// xfer stitches away from increase - this will probably be a loop
	xfer Loops[1:6] across;
	xfer Loops[1:3] 1 to Rightward to Front Bed;
	xfer Loops[3:5] 2 to Rightward to Front Bed;
	xfer Loops[5] 3 to Rightward to Front Bed;
	// split either the loop left on front bed or back bed - RS
	in reverse direction:{
		split Loops[0];
		split Loops[2];
		split Loops[4];
	}
	// rack and transfer back
	xfer Back_Loops 1 to Rightward to Front Bed;
	in Leftward direction:{
		knit Loops[0:6];
	}
	xfer Loops across; //all back loops here
	// a row of WS knit with i-cord
	in reverse direction:{
		knit Loops[3:9];
	}
}
