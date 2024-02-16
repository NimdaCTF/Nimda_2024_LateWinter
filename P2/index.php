<?php
	error_reporting(E_ERROR | E_PARSE);
	
    if (!isset($_GET['key']))
        highlight_file(__FILE__) && exit();
	
	if ( md5($_GET['key']) == md5(240610708)) {
        require_once 'flag.php';
        echo generate_flag($_COOKIE['id']);
	}
	else {
		echo 'not ok';
	}