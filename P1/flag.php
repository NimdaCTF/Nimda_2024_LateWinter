<?php

function generate_flag($user_id) {
    $flag_config = array(
        'prefix' => "nimda_H0w_D03s_17_w0rK_",
        'secret' => "elephant-waterfall-telescope-adventure-pineapple-algorithm-sunshine",
        'salt_size' => 12
    );

    $PREFIX = $flag_config['prefix'];
    $SECRET = $flag_config['secret'];
    $SALT_SIZE = $flag_config['salt_size'];

    return $PREFIX . substr(hash_hmac("sha256", strval($user_id), $SECRET), 0, $SALT_SIZE);
}