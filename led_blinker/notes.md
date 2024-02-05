## Difference in output

## From femtoRV risc_v:
```
Info: Running post-routing legalisation...

Info: Program finished normally.
+ fasm2frames.py --part xc7z020clg400-1 --db-root /usr/share/nextpnr/prjxray-db/zynq7 color_cycle.fasm
/usr/local/lib/python3.10/dist-packages/fasm-0.0.2.post88-py3.10-linux-x86_64.egg/fasm/parser/__init__.py:30: RuntimeWarning: Unable to import fast Antlr4 parser implementation.
  ImportError: cannot import name 'antlr_to_tuple' from partially initialized module 'fasm.parser' (most likely due to a circular import) (/usr/local/lib/python3.10/dist-packages/fasm-0.0.2.post88-py3.10-linux-x86_64.egg/fasm/parser/__init__.py)

  Falling back to the much slower pure Python textX based parser
  implementation.

  Getting the faster antlr parser can normally be done by installing the
  required dependencies and then reinstalling the fasm package with:
    pip uninstall
    pip install -v fasm

  warn(
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
Traceback (most recent call last):
  File "/home/bcheng/dev/amahdl/led_blinker/led_blinker.py", line 29, in <module>
    platform.build(LEDBlinker(), do_program=True)
  File "/home/bcheng/.local/lib/python3.10/site-packages/amaranth/build/plat.py", line 113, in build
    self.toolchain_program(products, name, **(program_opts or {}))
  File "/home/bcheng/.local/lib/python3.10/site-packages/amaranth_boards/arty_z7.py", line 170, in toolchain_program
    subprocess.run([xc3sprog, "-c", "jtaghs1_fast", "-p", "1", bitstream_filename], check=True)
  File "/usr/lib/python3.10/subprocess.py", line 503, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib/python3.10/subprocess.py", line 971, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/usr/lib/python3.10/subprocess.py", line 1863, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'xc3sprog'
```
