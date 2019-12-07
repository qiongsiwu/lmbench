set(LIBLIST lib_mem.c lib_timing.c lib_sched.c getopt.c)

add_executable(lat_mem_rd ${LIBLIST} lat_mem_rd.c)
add_executable(bw_mem ${LIBLIST} bw_mem.c)
