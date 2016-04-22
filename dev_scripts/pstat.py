import pstats
p = pstats.Stats('file.prof')
p.sort_stats('calls')
p.print_stats(10)
