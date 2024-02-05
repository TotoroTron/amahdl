## Difference in output

## From femtoRV risc_v:
```
Info: Running post-routing legalisation...

Info: Program finished normally.
+ fasm2frames.py --part xc7z020clg400-1 --db-root /usr/share/nextpnr/prjxray-db/zynq7 color_cycle.fasm
+ xc7frames2bit --part_file /usr/share/nextpnr/prjxray-db/zynq7/xc7z020clg400-1/part.yaml --part_name xc7z020clg400-1 --frm_file color_cycle.frames --output_file color_cycle.bit
+ openFPGALoader --board arty_z7_20 color_cycle.bit
empty
Jtag frequency : requested 6.00MHz   -> real 6.00MHz
Open file DONE
Parse file DONE
load program
Load SRAM: [===================================================] 100.00%
Done
```

## From amahdl:

```
Info: Running post-routing legalisation...

Info: Program finished normally.
empty
Jtag frequency : requested 6.00MHz   -> real 6.00MHz
Open file DONE
Parse file DONE
load program
Load SRAM: [===================================================] 100.00%
Done
```

## Remember to make changes in /amaranth_boards/arty_z7.py:
```
# def toolchain_program(self, products, name, **kwargs):
#     xc3sprog = os.environ.get("XC3SPROG", "xc3sprog")
#     with products.extract("{}.bit".format(name)) as bitstream_filename:
#         subprocess.run([xc3sprog, "-c", "jtaghs1_fast", "-p", "1", bitstream_filename], check=True)
```
## Replace above with:
```
def toolchain_program(self, products, name):
    openFPGALoader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
    with products.extract("{}.bit".format(name)) as bitstream_filename:
        subprocess.check_call([openFPGALoader, "-b", "arty_z7_20", bitstream_filename])

```
## Reinstall amaranth-boards after changes
```
pip install .
```