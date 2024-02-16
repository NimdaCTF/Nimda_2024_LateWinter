<?php
require_once 'flag.php';

if ($_SERVER["REQUEST_METHOD"] != "POST")
    highlight_file(__FILE__) && exit();

$flag = generate_flag($_COOKIE['id']);

$_403 = "Access Denied";
$_200 = "Welcome Admin";

 if ( !isset($_POST["flag"]) )
 	die($_403);

foreach ($_GET as $key => $value)
    $$key = $$value;

foreach ($_POST as $key => $value)
 	$$key = $value;

if ( $_POST["flag"] !== $flag )
 	die($_403);

echo "This is your flag : ". $flag . "\n";
die($_200);