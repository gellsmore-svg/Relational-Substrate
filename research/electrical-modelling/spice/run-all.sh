#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

for circuit in *.cir; do
  printf '== %s ==\n' "$circuit"
  ngspice -b "$circuit" | tail -n 8
done

printf '\nGenerated CSV files:\n'
ls -1 *.csv

