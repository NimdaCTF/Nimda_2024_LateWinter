<?php

if (!isset($_GET['next'])){
    echo 'I wrote new cool router between pages<br>';
    echo 'Check it out, here\'s available pages (use \'next\' get query variable):<br>';
    echo '- news.php<br>';
    echo '- users.php<br>';
    echo '- articles.php<br>';
    echo '<!-- flag.php !-->';
    exit();
}

include ($_GET['next']);