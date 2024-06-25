<?php
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
		$qi = $_POST['qi'];
		$qo = $_POST['qo'];
		$al = $_POST['al'];
		$ei = $_POST['ei'];
		$eo = $_POST['eo'];
		$im = $_POST['im'];

		// Prepare the command to execute the Python script with the numbers as arguments
		$command = escapeshellcmd("cd multiples_classify; python3 classify_trip.py -qi $qi -qo $qo -al $al -ei $ei -eo $eo -im $im; cd ../");
		$output = shell_exec($command);

		echo $output;
	}
?>
