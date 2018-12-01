#!/bin/bash

(for K in {1..140}; do cat puzzle_input; done;) | awk '{sum += $0; if (map[sum]) {print sum; exit} map[sum]=1}'
