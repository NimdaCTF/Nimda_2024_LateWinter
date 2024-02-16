<?php

function generate_flag($user_id) {
    $flag_config = array(
        'prefix' => "nimda_S0_B@d_Md5_COmpAr$1oN_",
        'secret' => "apple-mountain-guitar-ocean-galaxy-finance-harmony",
        'salt_size' => 12
    );

    $PREFIX = $flag_config['prefix'];
    $SECRET = $flag_config['secret'];
    $SALT_SIZE = $flag_config['salt_size'];

    return $PREFIX . substr(hash_hmac("sha256", strval($user_id), $SECRET), 0, $SALT_SIZE);
}