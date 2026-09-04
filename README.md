# minitestframework

A small compiler test harness: it runs every test case across a matrix of
toolchains and compiler flags, then emits one comparison report.

It exists because comparing "does this code still build and behave the same on
GCC vs Clang, RV32 vs RV64, at -O0 through -O3" by hand does not scale — the
interesting result is the *diff* between cells of the matrix, not any single run.

## What it does

1. Generates test cases into `testfolder/` (one directory per case).
2. Compiles each case with every configured toolchain × compiler × cflag set.
3. Inspects the resulting ELF (`elf.py`) for size and section metrics.
4. Validates behaviour and records pass/fail per cell (`validate.py`).
5. Writes a styled spreadsheet report (`report.py` → `output_styled.xlsx`).

## Configuration

The matrix lives in `test.cfg`:

```ini
[validate]
toolchain_path_list = {
        "900_RV32" : "./toolchain/900/32",
        "900_RV64" : "./toolchain/900/64",
        "910_RV32" : "./toolchain/910/32",
        "910_RV64" : "./toolchain/910/64"
        }
compiler_list = [
        "gcc",
        "clang"
        ]
```

Point `toolchain_path_list` at your own toolchain installs; the keys become the
column labels in the report.

## Usage

```bash
# generate test cases
python ./testfolder/test.py

# run the matrix and produce the report
python3 test.py
```

Results land in `output.xlsx` (raw) and `output_styled.xlsx` (highlighted).

## Layout

| Path | Purpose |
|---|---|
| `test.py` | driver — walks the matrix and collects results |
| `testcasestruct.py` | test case model |
| `elf.py` | ELF size/section extraction |
| `validate.py` | pass/fail rules |
| `report.py` | spreadsheet output |
| `vresult_types.py` | result value types |
| `crawler.py` | collects cases from a source tree |
| `toolchain/` | expected location of the toolchains under test |

## License

Apache-2.0. See [LICENSE](LICENSE).
