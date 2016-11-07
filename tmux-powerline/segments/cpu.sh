# Prints the CPU usage: user% sys% idle.

run_segment() {
	if shell_is_linux; then
		#cpu_line=$(top -b -n 1 | head | grep "Cpu(s)" )
		#cpu_user=$(echo "$cpu_line" | grep -Po "(\d+(.\d+)?)(?=%?\s?(us(er)?))")
		#cpu_system=$(echo "$cpu_line" | grep -Po "(\d+(.\d+)?)(?=%?\s?(sys?))")
		#cpu_idle=$(echo "$cpu_line" | grep -Po "(\d+(.\d+)?)(?=%?\s?(id(le)?))")
		#cpu_idle=$(vmstat |awk 'NR==3 {print $15}')
		cpu_idle=0
	elif shell_is_osx; then 
		cpus_line=$(top -e -l 1 | grep "CPU usage:" | sed 's/CPU usage: //')
		cpu_user=$(echo "$cpus_line" | awk '{print $1}'  | sed 's/%//' )
		cpu_system=$(echo "$cpus_line" | awk '{print $3}'| sed 's/%//' )
		cpu_idle=$(echo "$cpus_line" | awk '{print $5}'  | sed 's/%//' )
	fi

	#if [ -n "$cpu_user" ] && [ -n "$cpu_system" ] && [ -n "$cpu_idle" ]; then
		#echo "${cpu_user}, ${cpu_system}, ${cpu_idle}" | awk -F', ' '{printf("%5.1f,%5.1f,%5.1f",$1,$2,$3)}'
	if [ -n "$cpu_idle" ]; then
		#echo "${cpu_idle}"
		  echo CPU: $[100-$(vmstat 1 2|tail -1|awk '{print $15}')]
		return 0
	else
		return 1
	fi
}
