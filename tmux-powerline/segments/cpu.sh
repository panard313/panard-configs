# Prints the CPU usage: user% sys% idle.

run_segment() {
	if shell_is_linux; then
		echo CPU: $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]
		return 0
	elif shell_is_osx; then
		cpus_line=$(top -e -l 1 | grep "CPU usage:" | sed 's/CPU usage: //')
		#cpu_user=$(echo "$cpus_line" | awk '{print $1}'  | sed 's/%//' )
		#cpu_system=$(echo "$cpus_line" | awk '{print $3}'| sed 's/%//' )
		cpu_using=$(echo "$cpus_line" | awk '{print $5}'  | sed 's/%//' | awk -F '.' '{print $1}')
		echo CPU: $[100- $cpu_using]
        return 0
	fi
    return -1
}
