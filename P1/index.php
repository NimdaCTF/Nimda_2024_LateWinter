<?php
	error_reporting(E_ERROR | E_PARSE);
	
    if (!isset($_GET['key']))
        highlight_file(__FILE__) && exit();
	
	if (intval($_GET['key']) == '0e11111111111111' && !str_contains($_GET['key'], '0e') ) {
        require_once 'flag.php';
        echo generate_flag($_COOKIE['id']);
	}
	else {
		echo 'not ok';
	}
	