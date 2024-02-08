from amaranth import *
from amaranth.lib import data, enum

class BidirectionalCounter(Elaboratable):
    def __init__(self, width):
        self.op     = Signal()
        self.en     = Signal()
        self.count  = Signal(width)

    def elaborate(self, platform):
        m = Module()
        with m.If(self.op):
            m.d.sync += self.count.eq(self.count + 1) # If op == 1, increment counter
        with m.Else():
            m.d.sync += self.count.eq(self.count - 1) # If op == 0, decrement counter
        return EnableInserter(self.en)(m)

class ColorPhase(enum.Enum, shape=2):
    RED_GREEN = 0
    GREEN_BLUE = 1
    BLUE_RED = 2

class ControlUnit(Elaboratable):
    def __init__(self, width):
        self.rgb_count = self.rgb_layout(8, 8, 8)
        self.duty = Signal(width)
        self.rgb_led = self.rgb_layout(1, 1, 1)
        self.max = Const(2**width - 1)
        return
    
    def rgb_layout(r_bits, g_bits, b_bits):
        return data.StructLayout({
            "red":   unsigned(r_bits),
            "green": unsigned(g_bits),
            "blue":  unsigned(b_bits)
        })

    def elaborate(self, platform):
        m = Module()
        

        with m.If(self.duty < self.rgb_count.red):
            m.d.sync += self.rgb_led[0].eq(1)
        with m.Else():
            m.d.sync += self.rgb_led[0].eq(0)

        with m.If(self.duty < self.rgb_count.green):
            m.d.sync += self.rgb_led[1].eq(1)
        with m.Else():
            m.d.sync += self.rgb_led[1].eq(0)

        with m.If(self.duty < self.rgb_count.blue):
            m.d.sync += self.rgb_led[2].eq(1)
        with m.Else():
            m.d.sync += self.rgb_led[2].eq(0)

        # BEGIN FSM_COLOR_CYCLE
        with m.FSM(domain="sync") as fsm_color_cycle:
            with m.State("INIT"):
                m.d.sync += [
                    self.rgb_count(255, 0, 0),
                    self.duty.eq(0),
                ]
                m.next = "INCR_DUTY"
            with m.State("INCR_DUTY"):
                with m.If(self.duty < self.max):
                    m.d.sync += self.duty.eq(self.duty + 1)
                    m.next = "INCR_DUTY"
                with m.Else():
                    m.d.sync += self.duty.eq(0) # Is this statement necessary?
                    m.next = "SHIFT_COLOR"
                pass
            with m.State("SHIFT_COLOR"):
                pass

        # END FSM_COLOR_CYCLE

        return m

class ColorCycleAHDL(Elaboratable):
    def __init__(self, width=8):
        pass

    def elaborate(self, platform):
        m = Module()
        return m


from amaranth_boards.arty_z7 import ArtyZ720Platform
# ArtyZ720Platform().build(LEDBlinker(), do_program=True)

# Using PRJXRAY instead of default Vivado
# Add AMARANTH_ENV_XRAY to environment PATH variables and set to prjxray directory
# Also add PYTHONPATH and set to same prjxray directory
platform = ArtyZ720Platform()
platform.toolchain="Xray"
platform.build(ColorCycleAHDL(), do_program=True)
